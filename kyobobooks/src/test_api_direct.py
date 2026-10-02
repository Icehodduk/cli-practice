import httpx

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1",
}

# Request #8 URL
url = "https://store.kyobobook.co.kr/api/gw/best/best-seller/online?page=1&per=20&period=001&dsplDvsnCode=001&dsplTrgtDvsnCode=004&saleCmdtClstCode=33"

res = httpx.get(url, headers=headers)
print("Status without x-api-gw-key:", res.status_code)
if res.status_code == 200:
    data = res.json()
    print("Success! Total items:", len(data.get("data", {}).get("bestSeller", [])))
    print("First Book:", data["data"]["bestSeller"][0]["cmdtName"])
else:
    print(res.text[:200])
