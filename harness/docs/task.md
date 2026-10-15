# 📋 하네스(Harness) 시스템 구축 태스크 목록

본 문서는 전혀 다른 사이트를 엔드투엔드로 크롤링·EDA·리포트·대시보드까지 완전 자동화할 수 있는 하네스(Harness) 커스터마이징 시스템(Rules, Skills, Workflows, Hooks, Agents) 구축 진행 상황을 관리합니다.

## 마일스톤 및 세부 태스크

### 1. 룰 (Workspace Rules)
- [x] `.agents/rules/data-pipeline-rules.md` 작성
  - 폴더 구조 (`data/`, `docs/`, `images/`, `src/`) 및 uv 공통 `.venv` 원칙
  - Network API 우선 캡처 및 수집 데이터 분리 (`raw.json`, `cleaned.csv`)
  - 20년차 분석가 표준 EDA 5단계 & 10개 이상 차트 & TF-IDF 텍스트 마이닝 원칙
  - Chart.js 기반 Standalone 대시보드 및 UTF-8 BOM CSV 내보내기 원칙

### 2. 스킬 (Skills & Reusable Templates)
- [x] `.agents/skills/site-scraping-analysis-dashboard/SKILL.md` 작성
- [x] `.agents/skills/site-scraping-analysis-dashboard/scripts/normalizer.py` 구현
- [x] `.agents/skills/site-scraping-analysis-dashboard/scripts/template_scraper.py` 구현
- [x] `.agents/skills/site-scraping-analysis-dashboard/scripts/template_eda.py` 구현
- [x] `.agents/skills/site-scraping-analysis-dashboard/scripts/template_build_dashboard.py` 구현
- [x] `.agents/skills/site-scraping-analysis-dashboard/resources/dashboard_template.html` 구현

### 3. 워크플로우 (Workflows)
- [x] `.agents/workflows/analytics_pipeline.py` 오케스트레이터 구현
- [x] `.agents/workflows/analytics_pipeline.json` 파라미터 매니페스트 작성

### 4. 라이프사이클 훅 (Lifecycle Hooks)
- [x] `.agents/hooks.json` 설정 (PreToolUse, PostToolUse, Stop)
- [x] `.agents/hooks/scripts/env_guard.py` (가상환경 위반 차단 가드)
- [x] `.agents/hooks/scripts/post_validator.py` (대시보드 무결성 자동 검증기)
- [x] `.agents/hooks/scripts/stop_guard.py` (작업 미완성 시 조기종료 방지기)

### 5. 전문 서브에이전트 (Subagents)
- [x] `.agents/agents/web-scraper.md` (스크래핑 & 리버스 엔지니어링 에이전트)
- [x] `.agents/agents/eda-analyst.md` (20년차 EDA 및 통계 리포트 에이전트)
- [x] `.agents/agents/dashboard-engineer.md` (Chart.js 대시보드 프론트엔드 에이전트)
- [x] `define_subagent` 런타임 3대 서브에이전트 등록 완료

### 6. 자동화 검증 및 워크스루
- [x] 문법 및 훅 유효성 자동 검증 스크립트 실행
- [x] 가상 더미 데이터셋 대상 엔드투엔드 파이프라인 드라이런 테스트
- [x] `harness/docs/walkthrough.md` 작성 및 최종 완료 보고

### 7. 5대 핵심 보완 고도화 태스크
- [x] 봇 차단 대응 (Playwright-Stealth 헤더 스푸핑 & 랜덤 지터 & 지수 백오프)
- [x] 범용 데이터 정규화기 (통화기호, 쉼표, 상대시간, 결측치 자동 클리너)
- [x] 대용량 2-Tier 아키텍처 (차트용 사전 집계 & 산점도 샘플링 & 가상화 테이블)
- [x] 다국어 하이브리드 토크나이저 (문자셋 감지 및 영문/한글 불용어 자동 전환)
- [x] 파일 기반 체크포인트 엔진 (단계별 복구 및 스마트 재개 플래그)
