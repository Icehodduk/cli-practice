---
name: marp-slide
description: 마크다운 기반의 프레젠테이션(Marp) 발표 장표 및 슬라이드를 생성하거나 리팩토링할 때 사용하는 스킬입니다. 사용자가 Marp 슬라이드, 발표 자료 마크다운, 스피치 스크립트가 포함된 프레젠테이션 작성을 요청하거나, 30장 이상의 대량 발표 장표가 필요한 경우 반드시 활성화하여 이 가이드를 준수하십시오.
---

# Marp 발표 자료 생성 및 튜닝 워크플로우

이 스킬은 마크다운 기반의 발표 도구인 Marp를 활용하여 가독성이 극대화된 세련된 디자인의 슬라이드와 실전 발표용 2분 분량 스피커 노트를 완벽하게 생성하기 위한 지침서입니다.

---

## 1. 프론트매터 및 디자인 시스템 구성

Marp 슬라이드를 작성할 때, 문서의 가장 첫머리(Frontmatter)에는 반드시 다음 설정을 기입해야 합니다.

```yaml
---
marp: true
theme: gaia
paginate: false
_class: lead
style: |
  section {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    color: #333333;
    padding: 40px;
    background-color: #F8F9FA;
  }
  h1 {
    color: #1B365D;
    font-size: 1.6em;
    border-bottom: 2px solid #4682B4;
    padding-bottom: 8px;
  }
  h2 {
    color: #4682B4;
    font-size: 1.2em;
  }
  footer {
    font-size: 0.5em;
    color: #777777;
  }
  .lead h1 {
    font-size: 2.2em;
    color: #FFFFFF;
    border-bottom: none;
  }
  .lead {
    background-color: #1B365D;
    color: #FFFFFF;
    text-align: center;
  }
  blockquote {
    background: #F0F4F8;
    border-left: 5px solid #1B365D;
    padding: 10px;
    font-size: 0.85em;
  }
  table {
    font-size: 0.65em;
    width: 100%;
    margin-top: 10px;
  }
  th {
    background-color: #4682B4;
    color: white;
  }
  ul {
    font-size: 0.85em;
  }
---
```

---

## 2. 레이아웃 및 본문 구성 규칙

* **간지(Break Slide) 추가**:
  * 세션이나 대주제가 전환될 때 흐름을 환기하기 위해 간지 슬라이드를 배치하십시오.
  * 간지 슬라이드 상단에는 `<!-- _class: lead -->`를 적어 짙은 네이비 단색 배경을 적용하고, 세션 타이틀과 서브 설명문구만을 중앙 정렬하여 구조적 편안함을 제공하십시오.
* **이미지 겹침 방지 (우측 분할 레이아웃)**:
  * 그래프 차트 이미지나 핵심 이미지가 포함되는 장표는 Marp 전용 우측 분할 배경 문법인 `![bg right:45% fit](상대경로)`를 활용하십시오.
  * 슬라이드의 오른쪽 45% 영역에는 이미지를 맞춤형(fit)으로 적재하고, 왼쪽 55% 영역에는 텍스트 및 표 데이터를 기재하여 텍스트와 이미지가 겹치지 않게 철저히 통제하십시오.
* **제목 내 일련번호(수치 레이블) 제외**:
  * 각 장표의 제목(`h1`, `h2`)을 지을 때 순서나 순위를 뜻하는 수치 번호(`1.`, `[시각화 01]`, `[인사이트 02]`)를 절대 쓰지 마십시오. 세련되고 단정한 요약 한글 텍스트만으로 제목을 작성해야 합니다.

---

## 3. 정밀한 발표자 대본(Speaker Notes) 수록 규칙

* **2분 스피치 분량의 완성도 확보**:
  * 모든 슬라이드의 본문 아래에는 반드시 `<!-- [발표자 대본 - 2분 분량] ... -->` 주석 영역을 만드십시오.
  * 대본의 분량은 **슬라이드당 공백 포함 최소 550자 ~ 700자 이상**의 풍부한 스토리를 담아야 합니다.
  * 단순 장표 요약이 아니라, 발표자가 청중과 아이컨택을 하며 구어체 격식형 한국어(`안녕하십니까...`, `이 지표가 시사하는 비즈니스 요점은...`)로 조리 있게 살을 붙여 설명하는 수준 높은 연설문을 제공해야 합니다.

---

## 4. 컴파일 오류 예방 가이드

* **로컬 파일 리소스 읽기 정책 우회**:
  * 마크다운을 HTML이나 PDF 파일로 변환하여 내보낼 때, 로컬 이미지 접근 차단으로 인한 엑박 현상을 막기 위해 Marp 변환 설정이나 CLI 옵션에서 `--allow-local-files` 설정을 활성화해야 함을 안내하십시오.
* **상대경로 일관성 유지**:
  * 프레젠테이션 파일이 위치한 디렉토리(예: `docs/`)를 기준으로 이미지는 항상 상대경로(예: `../images/`)로 정확하게 가리키게 하여 정합성을 검증받으십시오.
