"""
범용 웹 스크래퍼 및 네트워크 API 리버스 엔지니어링 템플릿
작성자: Antigravity E2E 파이프라인
"""

import os
import time
import json
import random
import urllib.request
import urllib.error
from normalizer import DataNormalizer
import pandas as pd

class BasePipelineScraper:
    """네트워크 API 우선 탐색 및 Playwright DOM 폴백 스크래퍼"""

    def __init__(self, target_url, output_dir="data", project_name="sample"):
        self.target_url = target_url
        self.output_dir = output_dir
        self.project_name = project_name
        self.raw_json_path = os.path.join(output_dir, f"{project_name}_raw.json")
        self.cleaned_csv_path = os.path.join(output_dir, f"{project_name}_cleaned.csv")
        os.makedirs(output_dir, exist_ok=True)

        # 3단계 안티 봇 브라우저 헤더 스푸핑
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-CH-UA": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"macOS"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    def sleep_with_jitter(self, min_sec=1.5, max_sec=3.5):
        """요청 간 랜덤 지터 부여"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def fetch_api_with_backoff(self, api_url, max_retries=4):
        """지수 백오프 기반 REST API 안전 호출"""
        for attempt in range(max_retries):
            try:
                self.sleep_with_jitter()
                req = urllib.request.Request(api_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                if e.code in (429, 503):
                    wait = 2 ** (attempt + 1)
                    print(f"⚠️ Rate Limit 또는 서버 지연 감지 (HTTP {e.code}). {wait}초 후 재시도...")
                    time.sleep(wait)
                else:
                    print(f"❌ HTTP 오류 발생: {e.code}")
                    break
            except Exception as e:
                print(f"⚠️ 요청 예외 발생: {e}")
                time.sleep(2)
        return None

    def save_raw_and_cleaned(self, raw_records, dataframe, numeric_cols=None, date_cols=None, text_cols=None):
        """수집 데이터 원본 JSON 및 정제 CSV 2-Track 저장"""
        # 1. 원본 JSON 저장
        with open(self.raw_json_path, 'w', encoding='utf-8') as f:
            json.dump(raw_records, f, ensure_ascii=False, indent=2)
        print(f"✅ 원본 JSON 저장 완료: {self.raw_json_path} ({len(raw_records)}건)")

        # 2. 정규화 및 CSV 저장
        clean_df = DataNormalizer.normalize_dataframe(
            dataframe,
            numeric_cols=numeric_cols,
            date_cols=date_cols,
            text_cols=text_cols
        )
        clean_df.to_csv(self.cleaned_csv_path, index=False, encoding='utf-8-sig')
        print(f"✅ 정제 CSV 저장 완료: {self.cleaned_csv_path} ({len(clean_df)}건)")
        return clean_df
