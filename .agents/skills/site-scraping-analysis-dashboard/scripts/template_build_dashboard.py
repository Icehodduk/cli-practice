"""
범용 Chart.js Standalone 웹앱 대시보드 자동 빌더
작성자: Antigravity E2E 파이프라인
"""

import os
import json
import pandas as pd
import numpy as np

class AdaptiveDashboardBuilder:
    """정제된 CSV 데이터셋을 분석하여 스키마를 추론하고 독립형 HTML 대시보드를 생성하는 빌더"""

    def __init__(self, csv_path, output_html_path="dashboard.html", template_path=None):
        self.csv_path = csv_path
        self.output_html_path = output_html_path
        self.template_path = template_path or os.path.join(
            os.path.dirname(__file__), "..", "resources", "dashboard_template.html"
        )
        self.df = pd.read_csv(csv_path)

    def infer_schema(self):
        """데이터셋의 수치형, 범주형, 날짜형 컬럼 자동 추론"""
        numeric_candidates = []
        category_candidates = []
        date_candidates = []

        for col in self.df.columns:
            # 1. 날짜형 감지
            if 'date' in col.lower() or '일' in col or '연도' in col or 'year' in col.lower():
                date_candidates.append(col)
                continue

            # 2. 수치형 감지
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if self.df[col].nunique() > 5:
                    numeric_candidates.append(col)
                else:
                    category_candidates.append(col)
                continue

            # 3. 범주형 감지
            if self.df[col].nunique() < 50:
                category_candidates.append(col)

        return {
            'numericKey': numeric_candidates[0] if numeric_candidates else None,
            'categoryKey': category_candidates[0] if category_candidates else None,
            'dateKey': date_candidates[0] if date_candidates else None
        }

    def build(self, title="비즈니스 애널리틱스 대시보드", subtitle="데이터 기반 인터랙티브 분석"):
        schema = self.infer_schema()
        num_key = schema['numericKey']
        cat_key = schema['categoryKey']

        metadata = {
            'numericKey': num_key,
            'categoryKey': cat_key,
            'dateKey': schema['dateKey'],
            'totalCount': len(self.df),
            'displayColumns': self.df.columns.tolist()[:7]
        }

        # 카테고리 목록 추출
        if cat_key:
            metadata['categories'] = self.df[cat_key].dropna().value_counts().head(15).index.tolist()

        # 수치형 구간 계산 (Bar Chart용 사전 집계)
        if num_key:
            s = self.df[num_key].dropna()
            try:
                cuts, bins = pd.qcut(s, q=4, retbins=True, duplicates='drop')
                labels = [f"{int(bins[i]):,}~{int(bins[i+1]):,}" for i in range(len(bins)-1)]
                counts = pd.cut(s, bins=bins, labels=labels).value_counts().sort_index().tolist()
                metadata['rangeLabels'] = labels
                metadata['rangeCounts'] = counts
            except Exception:
                metadata['rangeLabels'] = ['하위 25%', '중위 50%', '상위 25%']
                metadata['rangeCounts'] = [len(s)//4, len(s)//2, len(s)//4]

        # 데이터 직렬화
        items = self.df.to_dict(orient='records')
        payload = {
            'metadata': metadata,
            'items': items
        }

        payload_json = json.dumps(payload, ensure_ascii=False)

        # 템플릿 로드 및 치환
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        html_out = template.replace('{{TITLE}}', title)
        html_out = html_out.replace('{{SUBTITLE}}', subtitle)
        html_out = html_out.replace('{{INLINE_JSON}}', payload_json)

        with open(self.output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_out)

        file_size_kb = os.path.getsize(self.output_html_path) / 1024
        print(f"✅ 대시보드 HTML 빌드 완료: {self.output_html_path} ({file_size_kb:.1f} KB)")
        return self.output_html_path
