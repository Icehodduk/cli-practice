import httpx
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1",
}

api_urls = [
    "https://store.kyobobook.co.kr/gw/pub/api/ord/best/best-seller/detail",
    "https://store.kyobobook.co.kr/api/gw/pub/api/ord/best/best-seller",
    "https://serviceapi.kyobobook.co.kr/api/gw/pub/api/ord/best/best-seller/detail",
]

params = {
    "page": 1,
    "per": 20,
    "saleCmdtDvcode": "01",
    "cmdtGroupDvcode": "01",
    "pbctDvcode": "01",
    "sortDvcode": "01",
    "storeCode": "001"
}

for url in api_urls:
    print(f"Testing URL: {url}")
    try:
        res = httpx.get(url, headers=headers, params=params, timeout=5.0)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print("Response:", json.dumps(res.json(), ensure_ascii=False)[:300])
        else:
            print("Response text:", res.text[:150])
    except Exception as e:
        print("Error:", e)
    print("-" * 50)
