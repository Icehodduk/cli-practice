# 📖 CLI Practice: 도서 이커머스 데이터 엔지니어링 & 애널리틱스 허브

본 저장소(`cli-practice`)는 국내 주요 대형 온라인 서점(**교보문고**, **YES24**)의 베스트셀러 도서 데이터를 수집(Scraping)·정제(Cleaning)하고, 심층 탐색적 데이터 분석(EDA), 멀티 포맷 비즈니스 리포팅(Markdown/DOCX/PDF/PPTX), 그리고 인터랙티브 웹 대시보드를 구축 및 자동 배포하는 통합 데이터 실습 프로젝트입니다.

---

## 🌐 교보문고 IT 베스트셀러 대시보드 라이브 웹앱

교보문고 IT/컴퓨터 분야 479권의 베스트셀러 데이터를 실시간으로 검색, 필터링 및 다변량 차트로 탐색할 수 있는 반응형 웹 애플리케이션입니다:

👉 **[https://icehodduk.github.io/cli-practice/](https://icehodduk.github.io/cli-practice/)**  
*(서브 경로: [https://icehodduk.github.io/cli-practice/kyobobooks/dashboard.html](https://icehodduk.github.io/cli-practice/kyobobooks/dashboard.html))*

> **CI/CD 자동 배포**: GitHub Actions (`.github/workflows/deploy-pages.yml`)를 통해 `main` 브랜치 변경 시 GitHub Pages로 무중단 배포됩니다.

---

## 🗂️ 저장소 전체 프로젝트 구조

```plaintext
cli-practice/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml          # GitHub Pages 자동 배포 CI/CD 파이프라인
│
├── kyobobooks/                       # 📘 [프로젝트 1] 교보문고 IT 베스트셀러 프로젝트
│   ├── dashboard.html                # Chart.js 기반 인터랙티브 독립 실행형 웹앱 대시보드
│   ├── data/
│   │   ├── bestseller_raw.json       # 원본 수집 JSON 데이터
│   │   └── bestseller_cleaned.csv    # 479건 정제 데이터셋
│   ├── docs/
│   │   ├── eda_report.md             # 20년차 데이터 분석가 관점의 심층 EDA 보고서
│   │   ├── implementation_plan.md    # 대시보드 초정밀 구현 계획서 (v2.0)
│   │   └── walkthrough.md            # 대시보드 구현 및 검증 결과 워크스루
│   ├── images/                       # EDA 정적 시각화 이미지 11종
│   └── src/
│       ├── build_dashboard.py        # 데이터 전처리 & 대시보드 HTML 자동 빌더
│       ├── eda_analysis.py           # EDA 시각화 차트 11종 생성 스크립트
│       └── scraper.py                # 교보문고 네트워크 API 기반 데이터 수집기
│
├── yes24/                            # 📕 [프로젝트 2] YES24 베스트셀러 데이터 분석 프로젝트
│   ├── data/                         # YES24 원본 및 정제 데이터
│   ├── docs/                         # EDA 보고서, Marp 슬라이드, DOCX/PDF 문서
│   ├── images/                       # YES24 분석 시각화 차트 이미지군
│   ├── src/                          # 스크래퍼, EDA 분석 및 보고서/발표자료 생성기
│   └── yes24_dashboard.xlsx          # 엑셀 기반 인터랙티브 분석 대시보드
│
├── index.html                        # 루트 웹 서빙을 위한 대시보드 엔트리포인트
├── pyproject.toml                    # uv 기반 통합 파이썬 패키지 의존성 관리
├── uv.lock                           # 패키지 락 파일
└── README.md                         # 본 통합 프로젝트 안내서
```

---

## 🚀 서브 프로젝트 상세 소개

### 1. 교보문고 IT/컴퓨터 베스트셀러 프로젝트 (`kyobobooks/`)
- **분석 대상**: 교보문고 IT/컴퓨터 분야 479개 베스트셀러 도서 데이터.
- **핵심 인사이트**:
  - `AI`(52.07점) 키워드가 출판 시장을 지배하는 압도적 메가트렌드로 확인.
  - 2만~3만원대 가격대가 전체의 47.2%를 차지하며 가장 높은 평균 순위를 기록하는 골든 스위트스팟.
  - 한빛미디어, 길벗, 영진닷컴 3사가 전체 베스트셀러의 37.4%를 과점.
- **Chart.js 웹앱 대시보드 (`dashboard.html`)**:
  - 별도 백엔드 없이 브라우저에서 직접 열리는 Standalone 구조.
  - **4대 KPI 요약 카드**: 실시간 도서 수, 평균/중앙값 가격, 2026년 신간 비중, TF-IDF 1위 키워드.
  - **Chart.js 6종 반응형 차트**: 가격대 분포(Bar), 출판사 점유율(Doughnut), 연도별 추이(Line), 상위 출판사 평균가(Horizontal Bar), 순위-가격 산점도(Scatter), TF-IDF 키워드 Top 20(Horizontal Bar).
  - **인터랙티브 기능**: 실시간 도서/저자 검색, 출판사·가격·연도 다차원 필터, 정렬, 페이지네이션, 엑셀 호환 UTF-8 BOM CSV 내보내기.

### 2. YES24 베스트셀러 종합 분석 프로젝트 (`yes24/`)
- **분석 대상**: YES24 베스트셀러 도서 데이터.
- **주요 산출물**:
  - **심층 EDA 보고서**: Markdown, DOCX, PDF 등 다양한 형식의 분석 문서.
  - **프레젠테이션 슬라이드**: Marp 및 PptxGenJS 기반의 네오브루탈(Neo-Brutalism), 노르딕(Nordic) 스타일 PPTX 및 HTML 발표 자료.
  - **엑셀 대시보드 (`yes24_dashboard.xlsx`)**: 비즈니스 보고용 스프레드시트 대시보드.

---

## 💻 로컬 환경 설정 및 실행 가이드

### 1. 가상환경 및 의존성 구성
본 저장소는 초고속 패키지 관리자 `uv`를 사용하며, 워크스페이스 공통 가상환경(`.venv`)을 공유합니다:
```bash
# 가상환경 동기화 및 라이브러리 설치
uv sync
```

### 2. 교보문고 대시보드 재생성 (빌드)
CSV 데이터를 재가공하고 TF-IDF 키워드를 새로 추출하여 대시보드 HTML을 빌드할 수 있습니다:
```bash
uv run python kyobobooks/src/build_dashboard.py
```

### 3. 로컬 브라우저에서 바로 열기
웹 서버 설치 없이 로컬 파일 탐색기에서 파일을 더블 클릭하거나 CLI로 바로 열 수 있습니다:
```bash
open kyobobooks/dashboard.html
# 또는 루트 엔트리포인트 열기
open index.html
```

---

## 🔗 주요 링크 모음
- **🌐 교보문고 웹앱 대시보드 라이브**: [https://icehodduk.github.io/cli-practice/](https://icehodduk.github.io/cli-practice/)
- **🐙 GitHub 리포지토리**: [https://github.com/Icehodduk/cli-practice](https://github.com/Icehodduk/cli-practice)
- **📑 교보문고 심층 EDA 분석 보고서**: [kyobobooks/docs/eda_report.md](kyobobooks/docs/eda_report.md)
- **📋 대시보드 구현 워크스루**: [kyobobooks/docs/walkthrough.md](kyobobooks/docs/walkthrough.md)
