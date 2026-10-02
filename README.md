# 📚 교보문고 IT 베스트셀러 비즈니스 애널리틱스 대시보드

교보문고 IT/컴퓨터 베스트셀러 정제 데이터셋(479권)을 바탕으로 탐색적 데이터 분석(EDA)을 수행하고, 별도의 백엔드 없이 브라우저에서 즉시 인터랙티브하게 데이터를 탐색할 수 있도록 구축한 **독립 실행형(Standalone) 웹앱 대시보드** 프로젝트입니다.

---

## 🌐 라이브 웹앱 대시보드 (Live Demo)

현재 GitHub Pages를 통해 전 세계 어디서나 웹 브라우저로 대시보드에 접속하실 수 있습니다:

👉 **[https://icehodduk.github.io/cli-practice/](https://icehodduk.github.io/cli-practice/)**

*(서브 경로: [https://icehodduk.github.io/cli-practice/kyobobooks/dashboard.html](https://icehodduk.github.io/cli-practice/kyobobooks/dashboard.html))*

> **배포 아키텍처**: GitHub Actions CI/CD (`.github/workflows/deploy-pages.yml`)를 통해 `main` 브랜치 변경 사항이 GitHub Pages로 자동 무중단 배포됩니다.

---

## ✨ 대시보드 주요 기능 (Key Features)

1. **📊 4대 핵심 비즈니스 KPI 카드 (실시간 연동)**
   - **조회 도서 수**: 전체 479권 중 현재 필터링된 도서 수 및 점유 비율(%)
   - **평균 판매가**: 필터 적용 도서의 평균 가격 및 중앙값(Median)
   - **2026년 신간 비중**: 최신간 비중 및 등재 권수
   - **최상위 키워드**: TF-IDF 텍스트 마이닝 기반 1위 핵심 키워드 (`AI`, 52.07점)

2. **📈 Chart.js v4 기반 6종 반응형 시각화 차트**
   - **가격대 구간별 도서 수 분포 (Bar Chart)**: 2만~3만원대 중심의 가격 스위트스팟 밀집도 시각화
   - **주요 출판사별 점유율 (Doughnut Chart)**: 한빛미디어, 길벗, 영진닷컴 등 메이저 출판사 과점 구조 파악
   - **출간 연도별 등재 도서 수 추이 (Line Chart)**: 2018~2026년 시계열 트렌드 및 최신간 집중 현황 분석
   - **상위 10대 출판사 평균 판매가 비교 (Horizontal Bar Chart)**: 출판사별 단가 포지셔닝(전문 번역서 vs 수험서/실용서)
   - **순위 vs 판매가 다변량 산점도 (Scatter Plot)**: 1위부터 479위까지의 가격 산포도 및 포인트 호버 시 도서 상세 정보(도서명, 저자, 출판사, 가격) 노출
   - **도서명·소개글 TF-IDF 핵심 키워드 Top 20 (Horizontal Bar Chart)**: AI, 최신, 실무, 실전, 데이터 등 핵심 수요 테마 순위

3. **🔍 실시간 다차원 필터 컨트롤러**
   - 도서명 / 저자명 실시간 검색 (Debounce 적용)
   - 상위 15대 출판사 드롭다운 필터
   - 6개 가격대 구간 필터 (1.5만원 미만 ~ 4만원 이상)
   - 출간 연도 필터 (2026년, 2025년, 2024년, 2023년 이전)
   - 필터 즉시 초기화 버튼
   - *모든 필터 조작 시 상단 KPI 카드, 6개 차트, 하단 데이터 테이블이 실시간으로 동시 리렌더링됩니다.*

4. **📋 상세 도서 데이터 그리드 & CSV 다운로드**
   - 필터링된 도서의 순위, 도서명, 저자, 출판사, 출간일, 판매가 표출
   - 컬럼 정렬 (순위 오름차순, 가격 높은순/낮은순, 최신 출간일순)
   - 페이지네이션 (10 / 25 / 50건 단위 보기)
   - **CSV 내보내기**: 엑셀 한글 깨짐을 방지하는 `UTF-8 with BOM` 인코딩 기반 즉시 다운로드 지원

---

## 📁 프로젝트 폴더 구조

```plaintext
cli-practice/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml          # GitHub Pages 자동 배포 CI/CD 워크플로
├── kyobobooks/
│   ├── dashboard.html                # [핵심] Chart.js 독립 실행형 웹앱 대시보드
│   ├── data/
│   │   ├── bestseller_raw.json       # 수집된 원본 베스트셀러 JSON 데이터
│   │   └── bestseller_cleaned.csv    # 479건 정제 데이터셋
│   ├── docs/
│   │   ├── eda_report.md             # 20년차 데이터 분석가 관점의 심층 EDA 분석 보고서
│   │   ├── implementation_plan.md    # 대시보드 구축 초정밀 구현 계획서 (v2.0)
│   │   └── walkthrough.md            # 대시보드 구현 및 검증 결과 워크스루
│   ├── images/                       # EDA 정적 시각화 이미지 11종
│   └── src/
│       ├── build_dashboard.py        # 데이터 전처리 및 대시보드 HTML 자동 빌더
│       ├── eda_analysis.py           # 11개 EDA 차트 생성 파이썬 스크립트
│       └── scraper.py                # 교보문고 베스트셀러 데이터 수집 스크립트
├── index.html                        # 루트 접속 시 대시보드를 서빙하기 위한 파일
├── pyproject.toml                    # 프로젝트 의존성 관리 설정 (uv 기반)
└── README.md                         # 본 프로젝트 안내 문서
```

---

## 💻 로컬 실행 및 빌드 가이드

### 1. 가상환경 및 의존성 설치
본 프로젝트는 `uv` 패키지 관리자를 사용합니다:
```bash
# 가상환경 동기화
uv sync
```

### 2. 대시보드 빌드
CSV 데이터셋을 바탕으로 최신 통계와 TF-IDF 키워드를 추출하여 `kyobobooks/dashboard.html`을 생성합니다:
```bash
uv run python kyobobooks/src/build_dashboard.py
```

### 3. 브라우저에서 대시보드 열기
별도의 웹 서버 설치 없이 브라우저에서 파일을 직접 열어 즉시 탐색할 수 있습니다:
```bash
open kyobobooks/dashboard.html
# 또는
open index.html
```

---

## 📊 주요 분석 인사이트 요약
- **초거대 AI 실무서의 부상**: TF-IDF 분석 결과 `AI`(52.07점)가 압도적 1위를 기록하며 시장을 견인하고 있습니다.
- **2만~3만원대 가격 스위트스팟**: 전체 도서의 47.2%가 2만~3만원대에 집중되어 있으며, 이 구간의 도서들이 평균 순위 212~215위로 가장 뛰어난 판매 성과를 보였습니다.
- **빅3 출판사의 과점 구조**: 한빛미디어(71권), 길벗(63권), 영진닷컴(45권)이 전체 베스트셀러의 37.4%를 점유하고 있습니다.

상세한 통계표와 분석 결과는 [kyobobooks/docs/eda_report.md](kyobobooks/docs/eda_report.md)에서 확인하실 수 있습니다.
