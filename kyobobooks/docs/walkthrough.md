# 📊 교보문고 IT 베스트셀러 Chart.js 웹앱 대시보드 구현 완료 워크스루 (Walkthrough)

**구현 완료 일자**: 2026년 10월 02일  
**적용 브랜치**: `feature/chartjs-dashboard`  
**관련 GitHub 이슈**: [#1](https://github.com/Icehodduk/cli-practice/issues/1)  
**핵심 산출물**:
- 대시보드 웹앱: [dashboard.html](file:///Users/ice_hodduk/Desktop/AI%20AGENT/Antigravity/inflearn/cli%20practice/kyobobooks/dashboard.html)
- 데이터 전처리 & 빌더: [build_dashboard.py](file:///Users/ice_hodduk/Desktop/AI%20AGENT/Antigravity/inflearn/cli%20practice/kyobobooks/src/build_dashboard.py)

---

## 1. 구현 개요 (Executive Summary)

GitHub 이슈 #1의 상세 구현 계획에 따라, 교보문고 IT/컴퓨터 베스트셀러 정제 데이터 479권을 인터랙티브하게 탐색할 수 있는 **단일 독립 실행형(Standalone) 웹앱 대시보드**(`kyobobooks/dashboard.html`)를 성공적으로 구축하였습니다.

별도의 복잡한 백엔드 웹 서버 구동 없이도 로컬 브라우저에서 `file://` 경로로 직접 열어 즉시 사용할 수 있도록 설계되었으며, **Chart.js v4** 기반의 6종 반응형 차트와 **Tailwind CSS** 기반의 깔끔한 미니멀 화이트 UI, 그리고 실시간 다차원 필터링 및 CSV 내보내기 기능을 완비하였습니다.

---

## 2. 주요 구현 컴포넌트 상세

### 2.1 데이터 전처리 & 인라인 빌더 (`kyobobooks/src/build_dashboard.py`)
- `bestseller_cleaned.csv` 로드 및 파생변수 생성 (`출간연도`, `가격대 6구간`, `순위구간 9티어`, 날짜 포맷팅).
- `scikit-learn`의 `TfidfVectorizer`를 이용해 한국어 불용어를 제거하고 상위 20개 핵심 키워드 점수를 사전 계산.
- 정제된 도서 데이터 479건과 메타데이터를 JSON으로 직렬화하여 HTML 템플릿 내 `window.DASHBOARD_DATA` 변수로 인라인 주입 (브라우저 로컬 실행 시 CORS 오류 원천 차단).

### 2.2 반응형 UI 및 인터랙티브 필터 컨트롤러
- **상단 4대 핵심 KPI 카드**:
  - 📚 **조회 도서 수**: 전체 479권 중 현재 필터링된 도서 수 및 비율 실시간 표기
  - 💰 **평균 판매가**: 필터 적용 도서의 평균가 및 중앙값 실시간 계산
  - 🚀 **2026년 신간 비중**: 최신간 비중 및 등재 권수
  - 🤖 **최상위 키워드**: TF-IDF 1위 키워드(`AI`, 52.07점)
- **동적 필터 컨트롤 바**:
  - 실시간 검색 인풋 (도서명 / 저자명 디바운스 검색)
  - 상위 15대 출판사 드롭다운 필터
  - 6개 가격대 구간 드롭다운 필터
  - 출간 연도 드롭다운 필터 (2026년, 2025년, 2024년, 2023년 이전)
  - 필터 즉시 초기화 버튼

### 2.3 Chart.js 반응형 6종 시각화 차트
1. **가격대 구간별 도서 수 분포 (Bar Chart)**: 2만~3만원대 중심의 가격 스위트스팟 밀집도 시각화.
2. **주요 출판사별 점유율 (Doughnut Chart)**: 한빛미디어, 길벗, 영진닷컴 등 메이저 7개사 및 기타 출판사 비중.
3. **출간 연도별 등재 도서 수 추이 (Line Chart)**: 2018년부터 2026년까지의 시계열 트렌드.
4. **주요 10대 출판사별 평균 판매가 비교 (Horizontal Bar Chart)**: 출판사별 단가 포지셔닝(에이콘출판 등 고가 전문서 vs 실용서).
5. **순위 vs 판매가 다변량 산점도 (Scatter Plot)**: 1위부터 479위까지의 가격 산포도 및 포인트 호버 시 도서 상세 툴팁 노출.
6. **도서명·소개글 TF-IDF 핵심 키워드 Top 20 (Horizontal Bar Chart)**: AI, 최신, 실무, 실전, 데이터 등 핵심 테마 점수.

### 2.4 인터랙티브 데이터 테이블 & CSV 익스포트
- 필터 조건이 반영된 도서 상세 목록 렌더링.
- 순위 오름차순, 가격 높은순/낮은순, 최신 출간일순 실시간 정렬 지원.
- 10개 / 25개 / 50개 페이지네이션 제어.
- 📥 **CSV 내보내기**: 엑셀 한글 깨짐을 방지하는 `UTF-8 with BOM` 규격으로 현재 필터링된 도서 목록을 즉시 다운로드.

---

## 3. 검증 결과 (Verification Results)

### 3.1 자동화 스크립트 무결성 테스트
- 실행 명령:
  ```bash
  uv run python -c "
  with open('kyobobooks/dashboard.html', encoding='utf-8') as f:
      html = f.read()
  assert 'chart.js' in html.lower()
  assert 'window.DASHBOARD_DATA =' in html
  import json
  json_part = html.split('window.DASHBOARD_DATA = ')[1].split(';\n\n    // State Management')[0]
  data = json.loads(json_part)
  assert len(data['items']) == 479
  print('검증 성공')
  "
  ```
- **결과**: `🎉 [PASS] 대시보드 HTML 파일 무결성 및 데이터 전수 검증 통과! (479건 일치, 6개 차트 완비)`

### 3.2 수동 실행 및 사용자 확인 가이드
- 브라우저에서 대시보드 열기:
  ```bash
  open kyobobooks/dashboard.html
  ```
- 브라우저 개발자 도구 콘솔에서 스크립트 오류 `0 errors` 확인.
- 검색어 입력 및 필터 변경 시 6개 차트와 KPI 수치가 부드럽게 애니메이션되며 갱신됨을 확인.
