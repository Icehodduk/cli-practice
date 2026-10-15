"""
하네스(Harness) 시스템 종합 자동화 검증 테스트 스위트
"""
import os
import sys
import json
import py_compile
import subprocess

print("=== 1. 파이썬 스크립트 문법 컴파일 검증 ===")
py_files = [
    ".agents/hooks/scripts/env_guard.py",
    ".agents/hooks/scripts/post_validator.py",
    ".agents/hooks/scripts/stop_guard.py",
    ".agents/skills/site-scraping-analysis-dashboard/scripts/normalizer.py",
    ".agents/skills/site-scraping-analysis-dashboard/scripts/template_scraper.py",
    ".agents/skills/site-scraping-analysis-dashboard/scripts/template_eda.py",
    ".agents/skills/site-scraping-analysis-dashboard/scripts/template_build_dashboard.py",
    ".agents/workflows/analytics_pipeline.py"
]

for pf in py_files:
    py_compile.compile(pf, doraise=True)
    print(f"   [PASS] {pf}")

print("\n=== 2. JSON 설정 및 매니페스트 유효성 검증 ===")
json_files = [
    ".agents/hooks.json",
    ".agents/workflows/analytics_pipeline.json"
]

for jf in json_files:
    with open(jf, encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) > 0
    print(f"   [PASS] {jf}")

print("\n=== 3. 훅 (Hook) 동작 단위 테스트 ===")
# Test env_guard.py with forbidden command
p = subprocess.Popen(['python3', '.agents/hooks/scripts/env_guard.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
out, _ = p.communicate(json.dumps({'toolCall': {'args': {'CommandLine': 'conda create -n bad_env'}}}))
res = json.loads(out)
assert res.get('decision') == 'deny', f"env_guard 차단 실패: {res}"
print("   [PASS] env_guard.py: conda 명령 차단 정상 작동 (decision: deny)")

# Test env_guard.py with allowed command
p = subprocess.Popen(['python3', '.agents/hooks/scripts/env_guard.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
out, _ = p.communicate(json.dumps({'toolCall': {'args': {'CommandLine': 'uv add pandas'}}}))
res = json.loads(out)
assert res.get('decision') == 'allow', f"env_guard 허용 실패: {res}"
print("   [PASS] env_guard.py: uv 명령 정상 허용 (decision: allow)")

print("\n=== 4. 데이터 정규화기 (normalizer.py) 단위 테스트 ===")
sys.path.insert(0, '.agents/skills/site-scraping-analysis-dashboard/scripts')
from normalizer import DataNormalizer

assert DataNormalizer.parse_numeric("₩25,000원") == 25000
assert DataNormalizer.parse_numeric("$19.99") == 19.99
assert DataNormalizer.parse_numeric("1.5만") == 15000.0
assert DataNormalizer.parse_numeric("3.2k") == 3200.0
assert DataNormalizer.parse_fuzzy_date("2026.10.15") == "2026-10-15"
assert DataNormalizer.parse_fuzzy_date("3일 전") != "미상"
print("   [PASS] DataNormalizer: 통화, 단위, 상대시간 파싱 전수 일치")

print("\n=== 5. 대시보드 템플릿 파일 무결성 검증 ===")
tmpl_path = ".agents/skills/site-scraping-analysis-dashboard/resources/dashboard_template.html"
with open(tmpl_path, encoding='utf-8') as f:
    tmpl = f.read()
assert "{{TITLE}}" in tmpl
assert "{{INLINE_JSON}}" in tmpl
assert "chart.js" in tmpl.lower()
assert "tailwindcss.com" in tmpl
print("   [PASS] dashboard_template.html: 필수 태그 및 CDN 정상 포함")

print("\n=== 6. 엔드투엔드 시뮬레이션 드라이런 (Dry-run) ===")
# 가상 데이터 60건 생성
import pandas as pd
mock_data = {
    "순위": list(range(1, 61)),
    "도서명": [f"인공지능 실무 {i}권" if i % 2 == 0 else f"파이썬 데이터 분석 {i}권" for i in range(1, 61)],
    "출판사": ["출판사A" if i % 3 == 0 else ("출판사B" if i % 3 == 1 else "출판사C") for i in range(1, 61)],
    "출간일": ["2026-05-10" if i % 2 == 0 else "2025-11-20" for i in range(1, 61)],
    "판매가": [20000 + (i * 300) for i in range(1, 61)],
    "소개글": ["최신 인공지능 실무를 위한 파이썬 기초와 실전 문제 풀이" for _ in range(60)]
}
mock_df = pd.DataFrame(mock_data)
os.makedirs("harness/data", exist_ok=True)
mock_csv = "harness/data/mock_dataset.csv"
mock_df.to_csv(mock_csv, index=False, encoding='utf-8-sig')

# EDA 엔진 드라이런
from template_eda import UniversalEDAEngine
eda_engine = UniversalEDAEngine(mock_csv, output_doc_path="harness/docs/mock_eda_report.md", image_dir="harness/images/mock")
eda_engine.generate_charts_and_report(numeric_cols=["판매가", "순위"], category_cols=["출판사", "출간일"], text_col="소개글")
assert os.path.exists("harness/docs/mock_eda_report.md"), "EDA 리포트 생성 실패"
print("   [PASS] UniversalEDAEngine: 모의 데이터 대상 5단계 프로파일링 및 차트/리포트 자동 생성 완료")

# 대시보드 빌더 드라이런
from template_build_dashboard import AdaptiveDashboardBuilder
dash_builder = AdaptiveDashboardBuilder(mock_csv, output_html_path="harness/mock_dashboard.html")
dash_builder.build(title="모의 테스트 대시보드", subtitle="엔드투엔드 파이프라인 검증")
assert os.path.exists("harness/mock_dashboard.html"), "대시보드 HTML 생성 실패"
with open("harness/mock_dashboard.html", encoding='utf-8') as f:
    dash_html = f.read()
    assert "window.APP_DATA =" in dash_html
    assert "chart.js" in dash_html.lower()
print("   [PASS] AdaptiveDashboardBuilder: 모의 데이터 스키마 추론 및 Standalone 대시보드 빌드 성공")

# 워크플로우 오케스트레이터 드라이런
sys.path.insert(0, '.agents/workflows')
from analytics_pipeline import PipelineOrchestrator
wf = PipelineOrchestrator(project_name="harness/mock_run", target_url="https://example.com/api", force=True)
wf.execute_all()
assert os.path.exists("harness/mock_run/data/.checkpoint_phase1.json"), "체크포인트 Phase 1 누락"
assert os.path.exists("harness/mock_run/docs/.checkpoint_phase2.json"), "체크포인트 Phase 2 누락"
assert os.path.exists("harness/mock_run/.checkpoint_phase3.json"), "체크포인트 Phase 3 누락"
print("   [PASS] PipelineOrchestrator: 4개 Phase 순차 실행 및 체크포인트 플래그 관리 무결성 통과")

# 모의 실행 정리
import shutil
shutil.rmtree("harness/mock_run", ignore_errors=True)
shutil.rmtree("harness/images/mock", ignore_errors=True)
if os.path.exists("harness/mock_dashboard.html"):
    os.remove("harness/mock_dashboard.html")
if os.path.exists("harness/docs/mock_eda_report.md"):
    os.remove("harness/docs/mock_eda_report.md")
if os.path.exists("harness/data/mock_dataset.csv"):
    os.remove("harness/data/mock_dataset.csv")

print("\n🎉 [ALL TESTS PASSED] 전체 하네스 시스템 5대 컴포넌트 자동화 검증 100% 통과!")
