"""
교보문고 베스트셀러 데이터 크롤러 모듈

이 모듈은 Playwright 헤드리스 브라우저를 이용하여 교보문고 온라인 베스트셀러 
페이지의 네트워크 통신을 캡처하고, 전체 페이지(처음부터 끝까지)의 API 응답 데이터를 
자동으로 감지/수집하여 JSON 및 CSV 파일로 저장하는 기능을 수행합니다.

주요 기능:
- Playwright를 통한 교보문고 베스트셀러 API(x-api-gw-key 인증 포함) 데이터 자동 수집
- 전체 페이지 자동 순회 (더 이상 새로운 항목이 없을 때까지 동적 처리)
- Raw JSON(bestseller_raw.json) 및 정제 CSV(bestseller_cleaned.csv) 저장
"""
import asyncio
import json
import pandas as pd
from pathlib import Path
from playwright.async_api import async_playwright

async def run_scraper():
    print("=== 교보문고 베스트셀러 전체 데이터 크롤링 시작 ===")
    
    raw_books = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        last_captured_count = 0

        async def handle_response(response):
            nonlocal last_captured_count
            if "best-seller/online" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    bestsellers = data.get("data", {}).get("bestSeller", [])
                    last_captured_count = len(bestsellers)
                    print(f"[API Capturing] {response.url} 에서 {last_captured_count}개 항목 수집")
                    raw_books.extend(bestsellers)
                except Exception as e:
                    print(f"API 응답 파싱 에러: {e}")

        page.on("response", handle_response)

        page_num = 1
        max_limit = 50  # 무한루프 방지 안전장치 (최대 50페이지=1000권)

        while page_num <= max_limit:
            last_captured_count = 0
            page_url = f"https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page={page_num}"
            print(f"페이지 이동: {page_url}")
            await page.goto(page_url, wait_until="networkidle")
            await asyncio.sleep(1.5)

            # 더 이상 항목이 수집되지 않거나 마지막 페이지인 경우 중단
            if last_captured_count == 0:
                print(f"페이지 {page_num}에서 더 이상 수집할 데이터가 없습니다. 전체 수집을 종료합니다.")
                break

            page_num += 1

        await browser.close()

    print(f"\n총 수집된 원본 항목 수: {len(raw_books)}")

    # 중복 제거 (saleCmdtid 기준)
    seen_ids = set()
    unique_books = []
    for item in raw_books:
        book_id = item.get("saleCmdtid")
        if book_id and book_id not in seen_ids:
            seen_ids.add(book_id)
            unique_books.append(item)

    print(f"중복 제거 후 최종 도서 수: {len(unique_books)}")

    # 데이터 저장 경로 설정
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Raw JSON 저장
    raw_json_path = data_dir / "bestseller_raw.json"
    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(unique_books, f, ensure_ascii=False, indent=2)
    print(f"원본 데이터 저장 완료: {raw_json_path}")

    # 가공 데이터 DataFrame 변환 및 저장
    extracted_data = []
    for item in unique_books:
        extracted_data.append({
            "순위": item.get("prstRnkn"),
            "상품ID": item.get("saleCmdtid"),
            "도서명": item.get("cmdtName"),
            "저자": item.get("chrcName"),
            "출판사": item.get("pbcmName"),
            "출간일": item.get("rlseDate"),
            "평점": item.get("revwRvspPnt"),
            "리뷰수": item.get("revwNum"),
            "정가": item.get("salePrc"),
            "판매가": item.get("sapr"),
            "소개글": item.get("inbukCntt"),
        })

    df = pd.DataFrame(extracted_data)
    csv_path = data_dir / "bestseller_cleaned.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"정제 데이터 저장 완료: {csv_path}")
    print("\n--- 수집 요약 ---")
    print(f"총 {len(df)} 권의 베스트셀러 데이터 수집 완료")
    print(df[["순위", "도서명", "저자", "출판사", "판매가"]].tail(5))

if __name__ == "__main__":
    asyncio.run(run_scraper())
