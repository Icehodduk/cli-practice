"""
범용 데이터 정규화 및 결측치 자동 클리너 (Universal Data Normalizer)
작성자: Antigravity E2E 파이프라인
"""

import re
import datetime
import pandas as pd
import numpy as np

class DataNormalizer:
    """임의의 웹 수집 데이터를 정제하고 표준 수치/날짜/텍스트로 정규화하는 클래스"""

    @staticmethod
    def parse_numeric(val):
        """통화기호, 쉼표, 단위('만', '억', 'k')를 감지하여 순수 실수형/정수형으로 변환"""
        if pd.isna(val) or val is None:
            return np.nan
        val_str = str(val).strip().replace(',', '')
        
        # 1. 한글 단위 '억', '만' 처리
        man_match = re.search(r'([\d.]+)\s*만', val_str)
        eok_match = re.search(r'([\d.]+)\s*억', val_str)
        if eok_match:
            try:
                base = float(eok_match.group(1)) * 100_000_000
                return base
            except ValueError:
                pass
        if man_match:
            try:
                base = float(man_match.group(1)) * 10_000
                return base
            except ValueError:
                pass

        # 2. 영문 단위 'k', 'm' 처리
        k_match = re.search(r'([\d.]+)\s*[kK]', val_str)
        m_match = re.search(r'([\d.]+)\s*[mM]', val_str)
        if k_match:
            try:
                return float(k_match.group(1)) * 1_000
            except ValueError:
                pass
        if m_match:
            try:
                return float(m_match.group(1)) * 1_000_000
            except ValueError:
                pass

        # 3. 통화기호(₩, $, €, ¥, 원 등) 제거 후 순수 숫자 추출
        clean_num = re.sub(r'[^\d.-]', '', val_str)
        try:
            return float(clean_num) if '.' in clean_num else int(clean_num)
        except ValueError:
            return np.nan

    @staticmethod
    def parse_fuzzy_date(val, base_date=None):
        """다양한 날짜 표기(YYYY-MM-DD, YYYY.MM.DD) 및 상대시간('3일 전', '어제')을 YYYY-MM-DD로 변환"""
        if pd.isna(val) or val is None:
            return '미상'
        val_str = str(val).strip()
        base = base_date or datetime.date.today()

        # 1. 상대 시간 표현 파싱
        if '방금' in val_str or '초 전' in val_str or '분 전' in val_str or '시간 전' in val_str:
            return base.strftime('%Y-%m-%d')
        if '어제' in val_str:
            return (base - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if '그저께' in val_str or '그제' in val_str:
            return (base - datetime.timedelta(days=2)).strftime('%Y-%m-%d')

        days_ago = re.search(r'(\d+)\s*일\s*전', val_str)
        if days_ago:
            return (base - datetime.timedelta(days=int(days_ago.group(1)))).strftime('%Y-%m-%d')

        weeks_ago = re.search(r'(\d+)\s*주\s*전', val_str)
        if weeks_ago:
            return (base - datetime.timedelta(days=int(weeks_ago.group(1)) * 7)).strftime('%Y-%m-%d')

        months_ago = re.search(r'(\d+)\s*개월\s*전', val_str)
        if months_ago:
            return (base - datetime.timedelta(days=int(months_ago.group(1)) * 30)).strftime('%Y-%m-%d')

        # 2. 절대 날짜 추출 (8자리 숫자: 20261015)
        m8 = re.search(r'(\d{4})(\d{2})(\d{2})', val_str)
        if m8:
            return f"{m8.group(1)}-{m8.group(2)}-{m8.group(3)}"

        # 3. 구분자 표기 (2026-10-15, 2026.10.15, 2026/10/15)
        m_sep = re.search(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', val_str)
        if m_sep:
            return f"{m_sep.group(1)}-{int(m_sep.group(2)):02d}-{int(m_sep.group(3)):02d}"

        return val_str[:10]

    @staticmethod
    def clean_html_text(val):
        """HTML 태그 제거 및 공백 정규화"""
        if pd.isna(val) or val is None:
            return ''
        text = re.sub(r'<[^>]+>', ' ', str(val))
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @classmethod
    def normalize_dataframe(cls, df, numeric_cols=None, date_cols=None, text_cols=None):
        """데이터프레임 전반을 검사하여 자동 정규화 수행"""
        df = df.copy()

        # 수치형 후보 컬럼 정규화
        if numeric_cols:
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = df[col].apply(cls.parse_numeric)

        # 날짜 후보 컬럼 정규화
        if date_cols:
            for col in date_cols:
                if col in df.columns:
                    df[col] = df[col].apply(cls.parse_fuzzy_date)

        # 텍스트 후보 컬럼 정규화
        if text_cols:
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].apply(cls.clean_html_text)

        return df
