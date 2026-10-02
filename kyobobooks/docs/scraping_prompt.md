# 1. 수집 관련 정보

### 네트워크 메뉴를 통해 실제 데이터를 가져오는 URL
- 베스트셀러 목록 API: `https://store.kyobobook.co.kr/api/gw/best/best-seller/online`
- 도서 실시간 정보/가격/위시 API: `https://store.kyobobook.co.kr/api/gw/pdt/category/wish`

### 해당 Request에 대한 Header 정보
- `User-Agent`: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
- `Referer`: `https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1`
- `Accept`: `application/json, text/plain, */*`
- `x-api-gw-key`: `eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0...` (동적 API Gateway 인증 토큰)

### Payload (Query Parameters)
- `page`: 페이지 번호 (예: 1, 2, 3...)
- `per`: 페이지당 출력 항목 수 (기본: 20)
- `period`: `001` (일간 베스트)
- `dsplDvsnCode`: `001` (온라인)
- `dsplTrgtDvsnCode`: `004` (국내도서)
- `saleCmdtClstCode`: `33` (컴퓨터/IT 분야 코드)

### 응답 예시 (JSON 의 일부 정보)
```json
{
  "data": {
    "bestSeller": [
      {
        "prstRnkn": 1,
        "saleCmdtid": "S000218736039",
        "cmdtName": "2026 이지패스 ADsP 데이터분석 준전문가",
        "chrcName": "박현민 외",
        "pbcmName": "위키북스",
        "rlseDate": "20260102",
        "inbukCntt": "미어캣 2026 최신 기출문제 수록 앱 제공...",
        "revwRvspPnt": 9.8
      }
    ],
    "totalCount": 100
  }
}
```
