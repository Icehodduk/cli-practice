---
name: site-scraping-analysis-dashboard
description: >-
  임의의 새로운 웹사이트를 입력받아 네트워크 API 리버스 엔지니어링 스크래핑, 데이터 정제,
  20년차 분석가 수준의 심층 EDA(10종 이상 시각화, 통계표, TF-IDF 텍스트 마이닝),
  마크다운 종합 리포트, 그리고 Chart.js 기반 인터랙티브 Standalone 웹앱 대시보드 구축까지
  원스톱으로 수행하는 엔드투엔드 파이프라인 스킬입니다.
---

# 🌐 범용 웹 스크래핑·심층 EDA·웹앱 대시보드 자동화 런북 (SKILL Guide)

이 스킬은 사용자가 새로운 대상 웹사이트 URL이나 비즈니스 목표를 제시했을 때, 고성능 데이터 파이프라인과 대화형 Chart.js 대시보드를 신속하고 정확하게 구축하기 위한 실행 가이드와 재사용 가능한 템플릿 스크립트 모음을 제공합니다.

---

## 1. 4단계 엔드투엔드 파이프라인 구조

```
[입력: 타깃 URL]
      │
      ▼
┌────────────────────────────────────────────────────────┐
│ Phase 1: 사이트 조사, 네트워크 API 캡처 및 고속 스크래핑 │
│ (scripts/template_scraper.py & scripts/normalizer.py)   │
└────────────────────────────────────────────────────────┘
      │ 산출물: data/*_raw.json & data/*_cleaned.csv
      ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: 20년차 데이터 분석가 표준 심층 EDA 및 리포팅    │
│ (scripts/template_eda.py)                              │
└────────────────────────────────────────────────────────┘
      │ 산출물: images/*.png (10종+) & docs/eda_report.md
      ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: 스키마 추론 및 Chart.js 독립 웹앱 대시보드 빌드  │
│ (scripts/template_build_dashboard.py)                  │
└────────────────────────────────────────────────────────┘
      │ 산출물: dashboard.html & index.html
      ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: 품질 전수 검증 및 배포                         │
│ (자동화 검증 스크립트 & GitHub Pages 배포 연동)          │
└────────────────────────────────────────────────────────┘
```

---

## 2. 세부 실행 절차 가이드 (Phase-by-Phase Runbook)

### Phase 1: 네트워크 리버스 엔지니어링 & 스크래핑
1. **타깃 사이트 네트워크 리스닝**:
   - `playwright`를 사용하여 대상 페이지 접속 후 내부 XHR/Fetch 트래픽 리스닝:
     ```python
     page.on("response", lambda res: print(res.url) if "api" in res.url or "json" in res.headers.get("content-type", "") else None)
     ```
   - 내부 REST API 엔드포인트가 확인되면, 브라우저 DOM 렌더링 대신 `urllib` 또는 `requests`로 JSON 직접 대량 호출.
   - 내부 API가 없거나 차단된 경우에만 Playwright DOM 파서(`page.locator(...)`)로 폴백.
2. **3단계 안티 봇 우회 탑재**:
   - 브라우저 헤더 스푸핑(`User-Agent`, `Sec-CH-UA`, `Referer`).
   - 요청 간 $1.5\text{s} \sim 3.5\text{s}$ 랜덤 지터(Jitter) 적용.
   - HTTP 429/503 발생 시 지수 백오프(Exponential Backoff, $2^n$초) 재시도.
3. **데이터 정제 (`scripts/normalizer.py`)**:
   - 통화 기호, 쉼표, 한글 단위(`만`, `억`), `k` 축약어 자동 제거 후 수치형 변환.
   - 상대 시간(`3일 전`, `어제`)을 `YYYY-MM-DD` 절대 날짜로 변환.
   - `data/<project>_raw.json` 및 `data/<project>_cleaned.csv` 저장.

### Phase 2: 심층 EDA 및 비즈니스 리포트 작성
1. **필수 프로파일링 5단계**:
   - `head(5)`, `tail(5)`, `info()`, `shape`, `duplicated().sum()`, `describe(include='all')` 전수 출력 및 기록.
2. **시각화 엄격 규정 준수**:
   - 반드시 `koreanize-matplotlib` 임포트.
   - `sns.set_theme()`, `sns.set_style()` 금지 (순수 Matplotlib 스타일로 깔끔하게 커스터마이징).
   - 최소 **10개 이상의 다각도 차트**(일변량, 이변량, 다변량)를 `images/`에 PNG로 저장.
   - 모든 그래프 아래에 대응하는 **기술통계표/교차표/피봇테이블**을 마크다운 표로 동반.
   - 모든 그래프마다 **50자 이상의 비즈니스 해석문** 서술.
3. **언어 적응형 TF-IDF 텍스트 마이닝**:
   - scikit-learn `TfidfVectorizer`를 사용하여 텍스트 컬럼(제목, 설명글 등)에서 상위 20~30개 키워드 추출 및 수평 막대 차트 생성.
4. **리포트 완성**:
   - `docs/eda_report.md` 단일 마크다운 보고서로 작성.

### Phase 3: Chart.js 독립 실행형 대시보드 구축
1. **스키마 자동 추론 (`scripts/template_build_dashboard.py`)**:
   - 데이터 컬럼의 Dtype과 유니크 값 수를 분석하여 수치형/범주형/시계열/텍스트 컬럼 자동 판별.
   - 6대 표준 차트(수치분포 막대, 점유율 도넛, 시계열 추이 선, 카테고리별 평균 수치, 순위/수치 산점도, TF-IDF 키워드)와 4대 KPI를 동적 매핑.
2. **대용량 2-Tier 스마트 최적화**:
   - 데이터가 1,000건을 초과할 경우 산점도는 최대 1,000개 표본을 샘플링하여 렌더링 렉 원천 방지.
3. **인라인 바인딩 & Standalone HTML 생성**:
   - `resources/dashboard_template.html` 골격에 전처리된 JSON 데이터를 인라인으로 삽입하여 `dashboard.html` 생성.
   - 브라우저 로컬 `file://` 환경에서도 CORS 오류 없이 100% 정상 작동 보장.
   - 실시간 다차원 필터, 검색, 정렬, 페이지네이션, `UTF-8 with BOM` CSV 다운로드 지원.

### Phase 4: 무결성 검증 및 배포
1. **자동 검증 스크립트 실행**:
   - HTML 구문 오류 확인, Chart.js 캔버스 6개 존재 확인, 데이터 전수 건수 일치 확인.
2. **배포 및 형상 관리**:
   - 루트 `index.html` 갱신 및 GitHub Pages 자동 배포 확인.
   - 프로젝트 `README.md`에 라이브 링크 및 구조 안내 문서화.

---

## 3. 재사용 가능한 스크립트 도구 모음

- **[scripts/normalizer.py](./scripts/normalizer.py)**: 통화, 단위, 상대 날짜, 결측치를 정규화하는 범용 데이터 클리너.
- **[scripts/template_scraper.py](./scripts/template_scraper.py)**: 네트워크 API 리버스 엔지니어링 및 안티봇 우회 스크래퍼 골격.
- **[scripts/template_eda.py](./scripts/template_eda.py)**: 5단계 프로파일링 및 10종 차트 자동 렌더링 엔진.
- **[scripts/template_build_dashboard.py](./scripts/template_build_dashboard.py)**: 자동 스키마 추론 및 Chart.js 독립형 대시보드 빌더.
- **[resources/dashboard_template.html](./resources/dashboard_template.html)**: Tailwind CSS + Chart.js v4 미니멀 화이트 범용 웹앱 골격.
