"""
교보문고 네트워크 API 패킷 캡처 모듈

이 모듈은 Playwright를 사용하여 교보문고 웹사이트 접속 시 발생하는 
네트워크 요청/응답(URL, Method, Status, Header, Payload 등)을 탐색 및 분석하는 테스트용 스크립트입니다.
"""
import asyncio
import json
from playwright.async_api import async_playwright

async def capture_network():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        captured_requests = []

        async def handle_response(response):
            url = response.url
            if "best" in url or "bestseller" in url or "api" in url:
                try:
                    headers = response.request.headers
                    post_data = response.request.post_data
                    status = response.status
                    content_type = response.headers.get("content-type", "")
                    
                    body_sample = ""
                    if "json" in content_type:
                        json_data = await response.json()
                        body_sample = json.dumps(json_data, ensure_ascii=False)[:300]
                    elif "text" in content_type or "html" in content_type:
                        text_data = await response.text()
                        body_sample = text_data[:150]

                    captured_requests.append({
                        "url": url,
                        "method": response.request.method,
                        "status": status,
                        "headers": headers,
                        "payload": post_data,
                        "response_sample": body_sample
                    })
                except Exception as e:
                    pass

        page.on("response", handle_response)

        target_url = "https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1"
        print(f"Navigating to {target_url} ...")
        await page.goto(target_url, wait_until="networkidle")
        await asyncio.sleep(3)

        await browser.close()

        print(f"\nCaptured {len(captured_requests)} relevant API/Data requests:")
        for idx, req in enumerate(captured_requests[:10]):
            print(f"\n--- Request #{idx+1} ---")
            print(f"URL: {req['url']}")
            print(f"Method: {req['method']} | Status: {req['status']}")
            print(f"Payload: {req['payload']}")
            print(f"Headers: {dict(list(req['headers'].items())[:5])}")
            print(f"Sample: {req['response_sample']}")

if __name__ == "__main__":
    asyncio.run(capture_network())
