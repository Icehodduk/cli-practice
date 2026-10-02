"""
교보문고 IT 베스트셀러 Chart.js 독립 실행형 웹앱 대시보드 빌더
작성자: 20년차 베테랑 비즈니스 애널리틱스 리드
"""

import os
import re
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_PATH = 'kyobobooks/data/bestseller_cleaned.csv'
OUTPUT_HTML_PATH = 'kyobobooks/dashboard.html'

def load_and_preprocess_data():
    df = pd.read_csv(DATA_PATH)
    
    # 1. 출간일 파생변수
    df['출간일_str'] = df['출간일'].astype(str)
    df['출간연도'] = df['출간일_str'].str[:4].astype(int)
    df['출간월'] = df['출간일_str'].str[4:6].astype(int)
    df['출간일_포맷'] = (
        df['출간일_str'].str[:4] + '-' + 
        df['출간일_str'].str[4:6] + '-' + 
        df['출간일_str'].str[6:8]
    )

    # 2. 가격대 구간 분류
    price_bins = [0, 15000, 20000, 25000, 30000, 40000, 100000]
    price_labels = ['1.5만원 미만', '1.5만~2만원', '2만~2.5만원', '2.5만~3만원', '3만~4만원', '4만원 이상']
    df['가격대'] = pd.cut(df['판매가'], bins=price_bins, labels=price_labels)

    # 3. 순위 구간 분류
    rank_bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 500]
    rank_labels = ['1~50위', '51~100위', '101~150위', '151~200위', '201~250위', '251~300위', '301~350위', '351~400위', '401위 이상']
    df['순위구간'] = pd.cut(df['순위'], bins=rank_bins, labels=rank_labels)

    # 4. TF-IDF 키워드 마이닝
    def clean_text(text):
        if not isinstance(text, str):
            return ''
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

    df['텍스트_통합'] = df['도서명'].apply(clean_text) + ' ' + df['소개글'].apply(clean_text)

    stopwords = {
        '있습니다', '있도록', '다양한', '필요한', '쉽게', '방법을', '또한', '실제', '내용을', '어떻게', 
        '모든', '직접', '같은', '책을', '것이다', '바로', '위해', '따라', '빠르게', '통해', '있는', 
        '것이', '따른', '대한', '함께', '가장', '권으로', '있다', '한다', '하는', '제공', '수록', 
        '완성', '이 책은', '책은', '등을', '자신의', '많은', '그것을', '경우', '위한', '그리고',
        '이를', '이에', '도서', '책의', '우리는', '우리가', '등의', '독자', '만든', '되어', '모두',
        '단번에', '지금', '어떤', '누구나', '스스로', '처음', '시작하는', '제대로', '기반으로'
    }

    tfidf = TfidfVectorizer(max_features=100, stop_words=list(stopwords), token_pattern=r'(?u)\b[가-힣a-zA-Z]{2,}\b')
    X = tfidf.fit_transform(df['텍스트_통합'])
    scores = X.sum(axis=0).A1
    top20_keywords = sorted(zip(tfidf.get_feature_names_out(), scores), key=lambda x: x[1], reverse=True)[:20]

    # 5. 전송용 데이터 구조화
    items = []
    for _, row in df.iterrows():
        items.append({
            'rank': int(row['순위']),
            'id': str(row['상품ID']),
            'title': str(row['도서명']),
            'author': str(row['저자']),
            'publisher': str(row['출판사']),
            'pubDate': str(row['출간일_포맷']),
            'pubYear': int(row['출간연도']),
            'price': int(row['판매가']),
            'priceTier': str(row['가격대']),
            'rankTier': str(row['순위구간']),
            'summary': str(row['소개글'])[:180] + '...' if pd.notnull(row['소개글']) else ''
        })

    # 메타데이터 계산
    metadata = {
        'totalBooks': len(df),
        'generatedAt': '2026-10-02',
        'avgPrice': round(float(df['판매가'].mean()), 1),
        'medianPrice': int(df['판매가'].median()),
        'newBookRate2026': round(float((df['출간연도'] == 2026).mean() * 100), 2),
        'topKeyword': top20_keywords[0][0].upper(),
        'topKeywordScore': round(float(top20_keywords[0][1]), 2),
        'publishers': df['출판사'].value_counts().head(15).index.tolist(),
        'years': sorted(df['출간연도'].unique().tolist(), reverse=True),
        'priceTiers': price_labels,
        'keywords': [{'name': kw[0], 'score': round(float(kw[1]), 2)} for kw in top20_keywords]
    }

    return {'metadata': metadata, 'items': items}

def generate_html(data):
    data_json_str = json.dumps(data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>교보문고 IT 베스트셀러 비즈니스 애널리틱스 대시보드</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js v4 CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }}
    .card-shadow {{
      box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05);
    }}
    .card-hover:hover {{
      box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.07);
      transition: all 0.2s ease-in-out;
    }}
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #f1f5f9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94a3b8;
    }}
  </style>
</head>
<body class="min-h-screen bg-slate-50 text-slate-800 antialiased">

  <!-- Header -->
  <header class="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow-sm">
          📊
        </div>
        <div>
          <h1 class="text-xl font-bold text-slate-900 tracking-tight">교보문고 IT 베스트셀러 애널리틱스 대시보드</h1>
          <p class="text-xs text-slate-500 font-medium">데이터 기준일: 2026-10-02 · 정제 표본 479권 · Chart.js 인터랙티브 분석</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button id="btnExportCSV" class="inline-flex items-center px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition">
          <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          CSV 내보내기
        </button>
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
          Standalone WebApp
        </span>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

    <!-- KPI Summary Grid (4 Cards) -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- KPI 1 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow card-hover flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500">
          <span class="text-xs font-semibold uppercase tracking-wider">조회 도서 수</span>
          <span class="p-2 rounded-lg bg-blue-50 text-blue-600 text-sm">📚</span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <span id="kpiTotalBooks" class="text-2xl font-extrabold text-slate-900 tracking-tight">479</span>
          <span id="kpiTotalRatio" class="text-xs font-medium text-slate-400">전체 479권 중 100%</span>
        </div>
      </div>

      <!-- KPI 2 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow card-hover flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500">
          <span class="text-xs font-semibold uppercase tracking-wider">평균 판매가</span>
          <span class="p-2 rounded-lg bg-emerald-50 text-emerald-600 text-sm">💰</span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <span id="kpiAvgPrice" class="text-2xl font-extrabold text-slate-900 tracking-tight">24,500원</span>
          <span id="kpiMedianPrice" class="text-xs font-medium text-slate-500">중앙값: 23,400원</span>
        </div>
      </div>

      <!-- KPI 3 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow card-hover flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500">
          <span class="text-xs font-semibold uppercase tracking-wider">2026년 신간 비중</span>
          <span class="p-2 rounded-lg bg-indigo-50 text-indigo-600 text-sm">🚀</span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <span id="kpiNewBookRate" class="text-2xl font-extrabold text-slate-900 tracking-tight">48.0%</span>
          <span id="kpiNewBookCount" class="text-xs font-medium text-slate-500">230권 등재</span>
        </div>
      </div>

      <!-- KPI 4 -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow card-hover flex flex-col justify-between">
        <div class="flex items-center justify-between text-slate-500">
          <span class="text-xs font-semibold uppercase tracking-wider">최상위 핵심 키워드</span>
          <span class="p-2 rounded-lg bg-amber-50 text-amber-600 text-sm">🤖</span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <span id="kpiTopKeyword" class="text-2xl font-extrabold text-blue-600 tracking-tight">AI</span>
          <span id="kpiKeywordScore" class="text-xs font-medium text-slate-500">TF-IDF: 52.07점</span>
        </div>
      </div>
    </section>

    <!-- Interactive Filter Control Bar -->
    <section class="bg-white rounded-xl p-4 border border-slate-200 card-shadow">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <!-- Search Box -->
        <div class="relative flex-1 min-w-[240px]">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </span>
          <input type="text" id="filterSearch" placeholder="도서명 또는 저자명 실시간 검색..." class="w-full pl-9 pr-4 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition" />
        </div>

        <!-- Filter Selects -->
        <div class="flex flex-wrap items-center gap-3">
          <!-- Publisher Filter -->
          <div class="w-full sm:w-auto">
            <select id="filterPublisher" class="w-full sm:w-44 px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition font-medium text-slate-700">
              <option value="ALL">출판사 전체</option>
            </select>
          </div>

          <!-- Price Tier Filter -->
          <div class="w-full sm:w-auto">
            <select id="filterPriceTier" class="w-full sm:w-40 px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition font-medium text-slate-700">
              <option value="ALL">가격대 전체</option>
            </select>
          </div>

          <!-- Year Filter -->
          <div class="w-full sm:w-auto">
            <select id="filterYear" class="w-full sm:w-36 px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition font-medium text-slate-700">
              <option value="ALL">출간연도 전체</option>
              <option value="2026">2026년</option>
              <option value="2025">2025년</option>
              <option value="2024">2024년</option>
              <option value="PRE_2024">2023년 이전</option>
            </select>
          </div>

          <!-- Reset Button -->
          <button id="btnResetFilter" class="w-full sm:w-auto px-3.5 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
            필터 초기화
          </button>
        </div>
      </div>
    </section>

    <!-- Visual Charts Grid (6 Charts) -->
    <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <!-- Chart 1: Price Distribution (Bar) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">가격대 구간별 도서 수 분포</h2>
            <p class="text-xs text-slate-400">2만~3만원대 스위트스팟 밀집도</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-semibold">Bar Chart</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartPriceDist"></canvas>
        </div>
      </div>

      <!-- Chart 2: Major Publisher Share (Doughnut) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">주요 출판사별 베스트셀러 점유율</h2>
            <p class="text-xs text-slate-400">상위 7개 메이저 출판사 및 과점 구조</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 font-semibold">Doughnut</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartPubShare"></canvas>
        </div>
      </div>

      <!-- Chart 3: Publication Year Trend (Line) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">출간 연도별 등재 도서 수 추이</h2>
            <p class="text-xs text-slate-400">최근 2024~2026년 최신간 집중 현황</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold">Line Chart</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartYearTrend"></canvas>
        </div>
      </div>

      <!-- Chart 4: Top 10 Publishers Avg Price (Horizontal Bar) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">주요 10대 출판사별 평균 판매가 비교</h2>
            <p class="text-xs text-slate-400">출판사별 가격 정책 및 단가 포지셔닝</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-amber-50 text-amber-700 font-semibold">Horizontal Bar</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartPubAvgPrice"></canvas>
        </div>
      </div>

      <!-- Chart 5: Rank vs Price (Scatter) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">순위 vs 판매가 다변량 산점도</h2>
            <p class="text-xs text-slate-400">포인트 호버 시 도서명 및 상세 정보 노출</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-rose-50 text-rose-700 font-semibold">Scatter Plot</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartRankPriceScatter"></canvas>
        </div>
      </div>

      <!-- Chart 6: TF-IDF Keywords Top 20 (Horizontal Bar) -->
      <div class="bg-white rounded-xl p-5 border border-slate-200 card-shadow">
        <div class="flex items-center justify-between pb-3 mb-2 border-b border-slate-100">
          <div>
            <h2 class="text-base font-bold text-slate-900">도서명·소개글 TF-IDF 핵심 키워드 Top 20</h2>
            <p class="text-xs text-slate-400">인공지능, 자격증, 수험서 중심의 시장 수요</p>
          </div>
          <span class="text-xs px-2 py-0.5 rounded bg-purple-50 text-purple-700 font-semibold">Text Mining</span>
        </div>
        <div class="h-64 relative">
          <canvas id="chartKeywords"></canvas>
        </div>
      </div>

    </section>

    <!-- Detailed Interactive Data Table -->
    <section class="bg-white rounded-xl border border-slate-200 card-shadow overflow-hidden">
      <!-- Table Header & Controls -->
      <div class="p-4 sm:p-5 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
        <div>
          <h2 class="text-base font-bold text-slate-900">베스트셀러 도서 상세 목록</h2>
          <p class="text-xs text-slate-500">현재 필터 조건에 부합하는 도서 내역 (정렬 및 페이지 이동 지원)</p>
        </div>
        <div class="flex items-center space-x-3">
          <!-- Sort Selector -->
          <div class="flex items-center space-x-1.5 text-xs text-slate-600">
            <span>정렬:</span>
            <select id="tableSortBy" class="px-2.5 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 font-medium">
              <option value="RANK_ASC">순위 오름차순 (1위부터)</option>
              <option value="PRICE_DESC">가격 높은순</option>
              <option value="PRICE_ASC">가격 낮은순</option>
              <option value="DATE_DESC">최신 출간일순</option>
            </select>
          </div>
          <!-- Page Size -->
          <div class="flex items-center space-x-1.5 text-xs text-slate-600">
            <span>표시:</span>
            <select id="tablePageSize" class="px-2.5 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500 font-medium">
              <option value="10">10개씩</option>
              <option value="25" selected>25개씩</option>
              <option value="50">50개씩</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Table Body -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead class="bg-slate-50 text-slate-600 text-xs font-semibold uppercase tracking-wider">
            <tr>
              <th scope="col" class="py-3 px-4 w-16 text-center">순위</th>
              <th scope="col" class="py-3 px-4">도서명</th>
              <th scope="col" class="py-3 px-4 w-40">저자</th>
              <th scope="col" class="py-3 px-4 w-32">출판사</th>
              <th scope="col" class="py-3 px-4 w-28 text-center">출간일</th>
              <th scope="col" class="py-3 px-4 w-28 text-right">판매가</th>
            </tr>
          </thead>
          <tbody id="tableBody" class="divide-y divide-slate-100 bg-white text-slate-700">
            <!-- Dynamic Injection -->
          </tbody>
        </table>
      </div>

      <!-- Table Pagination Footer -->
      <div class="p-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500 bg-slate-50/50">
        <div id="tableInfo">
          전체 479건 중 1 - 25건 표시 중
        </div>
        <div class="flex items-center space-x-1" id="paginationControls">
          <!-- Dynamic Pagination Buttons -->
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="mt-12 py-6 bg-white border-t border-slate-200 text-center text-xs text-slate-400">
    교보문고 IT 베스트셀러 심층 분석 리포트 대시보드 · Powered by Chart.js & Tailwind CSS · Standalone Edition
  </footer>

  <!-- Inline Injected Data & Core Application Script -->
  <script>
    // Injected Data from Python Preprocessing
    window.DASHBOARD_DATA = {data_json_str};

    // State Management
    const state = {{
      allItems: window.DASHBOARD_DATA.items,
      filteredItems: window.DASHBOARD_DATA.items,
      metadata: window.DASHBOARD_DATA.metadata,
      currentPage: 1,
      pageSize: 25,
      sortBy: 'RANK_ASC',
      filters: {{
        search: '',
        publisher: 'ALL',
        priceTier: 'ALL',
        year: 'ALL'
      }},
      chartInstances: {{}}
    }};

    // DOM Elements
    const elements = {{
      kpiTotalBooks: document.getElementById('kpiTotalBooks'),
      kpiTotalRatio: document.getElementById('kpiTotalRatio'),
      kpiAvgPrice: document.getElementById('kpiAvgPrice'),
      kpiMedianPrice: document.getElementById('kpiMedianPrice'),
      kpiNewBookRate: document.getElementById('kpiNewBookRate'),
      kpiNewBookCount: document.getElementById('kpiNewBookCount'),
      kpiTopKeyword: document.getElementById('kpiTopKeyword'),
      kpiKeywordScore: document.getElementById('kpiKeywordScore'),
      filterSearch: document.getElementById('filterSearch'),
      filterPublisher: document.getElementById('filterPublisher'),
      filterPriceTier: document.getElementById('filterPriceTier'),
      filterYear: document.getElementById('filterYear'),
      btnResetFilter: document.getElementById('btnResetFilter'),
      btnExportCSV: document.getElementById('btnExportCSV'),
      tableBody: document.getElementById('tableBody'),
      tableInfo: document.getElementById('tableInfo'),
      tableSortBy: document.getElementById('tableSortBy'),
      tablePageSize: document.getElementById('tablePageSize'),
      paginationControls: document.getElementById('paginationControls')
    }};

    // Initialization
    document.addEventListener('DOMContentLoaded', () => {{
      initFilterOptions();
      initEventListeners();
      renderAll();
    }});

    // Populate Filter Dropdowns
    function initFilterOptions() {{
      // Publishers
      state.metadata.publishers.forEach(pub => {{
        const opt = document.createElement('option');
        opt.value = pub;
        opt.textContent = pub;
        elements.filterPublisher.appendChild(opt);
      }});

      // Price Tiers
      state.metadata.priceTiers.forEach(tier => {{
        const opt = document.createElement('option');
        opt.value = tier;
        opt.textContent = tier;
        elements.filterPriceTier.appendChild(opt);
      }});
    }}

    // Event Listeners
    function initEventListeners() {{
      // Search Input with Debounce
      let debounceTimer;
      elements.filterSearch.addEventListener('input', (e) => {{
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {{
          state.filters.search = e.target.value.trim().toLowerCase();
          state.currentPage = 1;
          applyFilters();
        }}, 200);
      }});

      elements.filterPublisher.addEventListener('change', (e) => {{
        state.filters.publisher = e.target.value;
        state.currentPage = 1;
        applyFilters();
      }});

      elements.filterPriceTier.addEventListener('change', (e) => {{
        state.filters.priceTier = e.target.value;
        state.currentPage = 1;
        applyFilters();
      }});

      elements.filterYear.addEventListener('change', (e) => {{
        state.filters.year = e.target.value;
        state.currentPage = 1;
        applyFilters();
      }});

      elements.btnResetFilter.addEventListener('click', resetFilters);

      elements.tableSortBy.addEventListener('change', (e) => {{
        state.sortBy = e.target.value;
        sortAndRenderTable();
      }});

      elements.tablePageSize.addEventListener('change', (e) => {{
        state.pageSize = parseInt(e.target.value, 10);
        state.currentPage = 1;
        renderTable();
      }});

      elements.btnExportCSV.addEventListener('click', exportToCSV);
    }}

    function resetFilters() {{
      state.filters.search = '';
      state.filters.publisher = 'ALL';
      state.filters.priceTier = 'ALL';
      state.filters.year = 'ALL';
      state.currentPage = 1;

      elements.filterSearch.value = '';
      elements.filterPublisher.value = 'ALL';
      elements.filterPriceTier.value = 'ALL';
      elements.filterYear.value = 'ALL';

      applyFilters();
    }}

    // Filter Logic
    function applyFilters() {{
      const {{ search, publisher, priceTier, year }} = state.filters;

      state.filteredItems = state.allItems.filter(item => {{
        // Search Filter
        if (search) {{
          const matchTitle = item.title.toLowerCase().includes(search);
          const matchAuthor = item.author.toLowerCase().includes(search);
          if (!matchTitle && !matchAuthor) return false;
        }}

        // Publisher Filter
        if (publisher !== 'ALL' && item.publisher !== publisher) {{
          return false;
        }}

        // Price Tier Filter
        if (priceTier !== 'ALL' && item.priceTier !== priceTier) {{
          return false;
        }}

        // Year Filter
        if (year !== 'ALL') {{
          if (year === 'PRE_2024' && item.pubYear >= 2024) return false;
          if (year !== 'PRE_2024' && item.pubYear !== parseInt(year, 10)) return false;
        }}

        return true;
      }});

      renderAll();
    }}

    function renderAll() {{
      updateKPIs();
      renderCharts();
      sortAndRenderTable();
    }}

    // Update KPI Summary
    function updateKPIs() {{
      const count = state.filteredItems.length;
      const total = state.allItems.length;
      elements.kpiTotalBooks.textContent = count.toLocaleString();
      elements.kpiTotalRatio.textContent = `전체 ${{total}}권 중 ${{((count/total)*100).toFixed(1)}}%`;

      if (count > 0) {{
        const prices = state.filteredItems.map(d => d.price).sort((a,b) => a-b);
        const sum = prices.reduce((acc, v) => acc + v, 0);
        const avg = Math.round(sum / count);
        const median = prices[Math.floor(count / 2)];
        const count2026 = state.filteredItems.filter(d => d.pubYear === 2026).length;
        const rate2026 = ((count2026 / count) * 100).toFixed(1);

        elements.kpiAvgPrice.textContent = `${{avg.toLocaleString()}}원`;
        elements.kpiMedianPrice.textContent = `중앙값: ${{median.toLocaleString()}}원`;
        elements.kpiNewBookRate.textContent = `${{rate2026}}%`;
        elements.kpiNewBookCount.textContent = `${{count2026}}권 등재`;
      }} else {{
        elements.kpiAvgPrice.textContent = '0원';
        elements.kpiMedianPrice.textContent = '중앙값: 0원';
        elements.kpiNewBookRate.textContent = '0.0%';
        elements.kpiNewBookCount.textContent = '0권';
      }}
    }}

    // -------------------------------------------------------------
    // Chart.js Visualizations
    // -------------------------------------------------------------
    function renderCharts() {{
      renderChartPriceDist();
      renderChartPubShare();
      renderChartYearTrend();
      renderChartPubAvgPrice();
      renderChartRankPriceScatter();
      renderChartKeywords();
    }}

    function safeDestroyChart(chartKey) {{
      if (state.chartInstances[chartKey]) {{
        state.chartInstances[chartKey].destroy();
      }}
    }}

    // 1. Price Distribution Bar Chart
    function renderChartPriceDist() {{
      safeDestroyChart('priceDist');
      const ctx = document.getElementById('chartPriceDist').getContext('2d');
      const tiers = state.metadata.priceTiers;
      const counts = tiers.map(t => state.filteredItems.filter(d => d.priceTier === t).length);

      state.chartInstances.priceDist = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: tiers,
          datasets: [{{
            label: '도서 권수',
            data: counts,
            backgroundColor: '#3b82f6',
            borderRadius: 6,
            hoverBackgroundColor: '#2563eb'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => `${{ctx.parsed.y}}권`
              }}
            }}
          }},
          scales: {{
            y: {{
              beginAtZero: true,
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ precision: 0 }}
            }},
            x: {{
              grid: {{ display: false }}
            }}
          }}
        }}
      }});
    }}

    // 2. Major Publisher Share Doughnut Chart
    function renderChartPubShare() {{
      safeDestroyChart('pubShare');
      const ctx = document.getElementById('chartPubShare').getContext('2d');
      
      const countsByPub = {{}};
      state.filteredItems.forEach(d => {{
        countsByPub[d.publisher] = (countsByPub[d.publisher] || 0) + 1;
      }});

      const sorted = Object.entries(countsByPub).sort((a,b) => b[1] - a[1]);
      const topPubs = sorted.slice(0, 6);
      const otherCount = sorted.slice(6).reduce((acc, curr) => acc + curr[1], 0);

      const labels = topPubs.map(d => d[0]);
      const values = topPubs.map(d => d[1]);
      if (otherCount > 0) {{
        labels.push('기타 출판사');
        values.push(otherCount);
      }}

      const colors = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#10b981', '#f59e0b', '#94a3b8'];

      state.chartInstances.pubShare = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
          labels: labels,
          datasets: [{{
            data: values,
            backgroundColor: colors.slice(0, labels.length),
            borderWidth: 2,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          cutout: '65%',
          plugins: {{
            legend: {{
              position: 'right',
              labels: {{ boxWidth: 12, font: {{ size: 11 }} }}
            }}
          }}
        }}
      }});
    }}

    // 3. Year Trend Line Chart
    function renderChartYearTrend() {{
      safeDestroyChart('yearTrend');
      const ctx = document.getElementById('chartYearTrend').getContext('2d');

      const years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];
      const counts = years.map(y => state.filteredItems.filter(d => d.pubYear === y).length);

      state.chartInstances.yearTrend = new Chart(ctx, {{
        type: 'line',
        data: {{
          labels: years.map(y => `${{y}}년`),
          datasets: [{{
            label: '등재 도서수',
            data: counts,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: '#10b981'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{
              beginAtZero: true,
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ precision: 0 }}
            }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // 4. Top Publishers Avg Price (Horizontal Bar)
    function renderChartPubAvgPrice() {{
      safeDestroyChart('pubAvgPrice');
      const ctx = document.getElementById('chartPubAvgPrice').getContext('2d');

      const pubPrices = {{}};
      state.filteredItems.forEach(d => {{
        if (!pubPrices[d.publisher]) pubPrices[d.publisher] = [];
        pubPrices[d.publisher].push(d.price);
      }});

      // 상위 도서수 보유 출판사 8개 필터
      const topPubs = Object.keys(pubPrices)
        .filter(p => pubPrices[p].length >= 3)
        .map(p => ({{
          name: p,
          avg: Math.round(pubPrices[p].reduce((a,b)=>a+b, 0) / pubPrices[p].length),
          count: pubPrices[p].length
        }}))
        .sort((a,b) => b.avg - a.avg)
        .slice(0, 8);

      state.chartInstances.pubAvgPrice = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: topPubs.map(d => d.name),
          datasets: [{{
            label: '평균 판매가',
            data: topPubs.map(d => d.avg),
            backgroundColor: '#f59e0b',
            borderRadius: 4,
            indexAxis: 'y'
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => `${{ctx.parsed.x.toLocaleString()}}원`
              }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ callback: (v) => `${{v/10000}}만원` }}
            }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // 5. Rank vs Price Scatter Plot
    function renderChartRankPriceScatter() {{
      safeDestroyChart('rankScatter');
      const ctx = document.getElementById('chartRankPriceScatter').getContext('2d');

      const scatterData = state.filteredItems.map(d => ({{
        x: d.rank,
        y: d.price,
        title: d.title,
        author: d.author,
        publisher: d.publisher
      }}));

      state.chartInstances.rankScatter = new Chart(ctx, {{
        type: 'scatter',
        data: {{
          datasets: [{{
            label: '도서 위치',
            data: scatterData,
            backgroundColor: 'rgba(239, 68, 68, 0.65)',
            hoverBackgroundColor: '#ef4444',
            pointRadius: 4.5,
            pointHoverRadius: 7
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => {{
                  const d = ctx.raw;
                  return [
                    `[${{d.x}}위] ${{d.title}}`,
                    `저자: ${{d.author}} | 출판사: ${{d.publisher}}`,
                    `판매가: ${{d.y.toLocaleString()}}원`
                  ];
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              title: {{ display: true, text: '베스트셀러 순위 (1~479위)', font: {{ size: 11 }} }},
              grid: {{ color: '#f1f5f9' }}
            }},
            y: {{
              title: {{ display: true, text: '판매가 (원)', font: {{ size: 11 }} }},
              grid: {{ color: '#f1f5f9' }},
              ticks: {{ callback: (v) => `${{v.toLocaleString()}}원` }}
            }}
          }}
        }}
      }});
    }}

    // 6. Keywords TF-IDF Bar Chart
    function renderChartKeywords() {{
      safeDestroyChart('keywords');
      const ctx = document.getElementById('chartKeywords').getContext('2d');
      const kwData = state.metadata.keywords.slice(0, 12);

      state.chartInstances.keywords = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: kwData.map(d => d.name),
          datasets: [{{
            label: 'TF-IDF 중요도 점수',
            data: kwData.map(d => d.score),
            backgroundColor: '#8b5cf6',
            borderRadius: 4,
            indexAxis: 'y'
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: '#f1f5f9' }} }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});
    }}

    // -------------------------------------------------------------
    // Detailed Table & Pagination Logic
    // -------------------------------------------------------------
    function sortAndRenderTable() {{
      const items = [...state.filteredItems];

      switch(state.sortBy) {{
        case 'RANK_ASC':
          items.sort((a,b) => a.rank - b.rank);
          break;
        case 'PRICE_DESC':
          items.sort((a,b) => b.price - a.price);
          break;
        case 'PRICE_ASC':
          items.sort((a,b) => a.price - b.price);
          break;
        case 'DATE_DESC':
          items.sort((a,b) => b.pubDate.localeCompare(a.pubDate));
          break;
      }}

      state.filteredItems = items;
      renderTable();
    }}

    function renderTable() {{
      const total = state.filteredItems.length;
      const start = (state.currentPage - 1) * state.pageSize;
      const end = Math.min(start + state.pageSize, total);
      const pageItems = state.filteredItems.slice(start, end);

      // Render Rows
      elements.tableBody.innerHTML = '';
      if (pageItems.length === 0) {{
        elements.tableBody.innerHTML = `
          <tr>
            <td colspan="6" class="py-8 text-center text-slate-400">
              조건에 부합하는 도서가 없습니다.
            </td>
          </tr>
        `;
      }} else {{
        pageItems.forEach(item => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-50/80 transition';
          tr.innerHTML = `
            <td class="py-3 px-4 text-center font-bold text-slate-900">${{item.rank}}</td>
            <td class="py-3 px-4">
              <div class="font-semibold text-slate-900 leading-snug">${{escapeHtml(item.title)}}</div>
              <div class="text-xs text-slate-400 mt-0.5 line-clamp-1">${{escapeHtml(item.summary)}}</div>
            </td>
            <td class="py-3 px-4 text-slate-600 text-xs">${{escapeHtml(item.author)}}</td>
            <td class="py-3 px-4">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700">
                ${{escapeHtml(item.publisher)}}
              </span>
            </td>
            <td class="py-3 px-4 text-center text-xs text-slate-500 font-mono">${{item.pubDate}}</td>
            <td class="py-3 px-4 text-right font-semibold text-slate-900">${{item.price.toLocaleString()}}원</td>
          `;
          elements.tableBody.appendChild(tr);
        }});
      }}

      // Update Pagination & Info
      elements.tableInfo.textContent = total > 0 
        ? `전체 ${{total.toLocaleString()}}건 중 ${{start + 1}} - ${{end}}건 표시 중`
        : `조회된 도서가 없습니다.`;

      renderPagination(total);
    }}

    function renderPagination(total) {{
      elements.paginationControls.innerHTML = '';
      const totalPages = Math.ceil(total / state.pageSize);
      if (totalPages <= 1) return;

      // Prev Button
      const btnPrev = document.createElement('button');
      btnPrev.textContent = '이전';
      btnPrev.disabled = state.currentPage === 1;
      btnPrev.className = `px-2.5 py-1 rounded text-xs font-medium border ${{state.currentPage === 1 ? 'text-slate-300 border-slate-200 cursor-not-allowed' : 'text-slate-600 border-slate-200 hover:bg-slate-100'}}`;
      btnPrev.onclick = () => {{
        if (state.currentPage > 1) {{
          state.currentPage--;
          renderTable();
        }}
      }};
      elements.paginationControls.appendChild(btnPrev);

      // Page numbers (Limit to max 5 displayed)
      let startP = Math.max(1, state.currentPage - 2);
      let endP = Math.min(totalPages, startP + 4);
      if (endP - startP < 4) startP = Math.max(1, endP - 4);

      for (let p = startP; p <= endP; p++) {{
        const btnP = document.createElement('button');
        btnP.textContent = p;
        btnP.className = `px-2.5 py-1 rounded text-xs font-medium border ${{p === state.currentPage ? 'bg-blue-600 text-white border-blue-600 font-bold' : 'text-slate-600 border-slate-200 hover:bg-slate-100'}}`;
        btnP.onclick = () => {{
          state.currentPage = p;
          renderTable();
        }};
        elements.paginationControls.appendChild(btnP);
      }}

      // Next Button
      const btnNext = document.createElement('button');
      btnNext.textContent = '다음';
      btnNext.disabled = state.currentPage === totalPages;
      btnNext.className = `px-2.5 py-1 rounded text-xs font-medium border ${{state.currentPage === totalPages ? 'text-slate-300 border-slate-200 cursor-not-allowed' : 'text-slate-600 border-slate-200 hover:bg-slate-100'}}`;
      btnNext.onclick = () => {{
        if (state.currentPage < totalPages) {{
          state.currentPage++;
          renderTable();
        }}
      }};
      elements.paginationControls.appendChild(btnNext);
    }}

    // Export to CSV Functionality
    function exportToCSV() {{
      if (state.filteredItems.length === 0) {{
        alert('내보낼 도서 데이터가 없습니다.');
        return;
      }}

      const headers = ['순위', '도서명', '저자', '출판사', '출간일', '판매가', '가격대', '순위구간'];
      const rows = state.filteredItems.map(d => [
        d.rank,
        `"${{d.title.replace(/"/g, '""')}}"`,
        `"${{d.author.replace(/"/g, '""')}}"`,
        `"${{d.publisher.replace(/"/g, '""')}}"`,
        d.pubDate,
        d.price,
        d.priceTier,
        d.rankTier
      ]);

      const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `교보문고_IT베스트셀러_필터결과_${{new Date().toISOString().slice(0,10)}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    function escapeHtml(str) {{
      if (!str) return '';
      return str.replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
    }}
  </script>
</body>
</html>
"""
    return html_content

def main():
    print('1. 교보문고 베스트셀러 데이터 로드 및 전처리 시작...')
    data = load_and_preprocess_data()
    print(f'   - 총 도서 수: {data["metadata"]["totalBooks"]}건')
    print(f'   - 평균 판매가: {data["metadata"]["avgPrice"]:,}원')
    print(f'   - 2026년 신간 비중: {data["metadata"]["newBookRate2026"]}%')
    print(f'   - 1위 키워드: {data["metadata"]["topKeyword"]} ({data["metadata"]["topKeywordScore"]}점)')

    print('\n2. 독립 실행형 HTML 대시보드 템플릿 렌더링...')
    html = generate_html(data)

    print(f'\n3. {OUTPUT_HTML_PATH} 파일 저장 중...')
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    
    file_size_kb = os.path.getsize(OUTPUT_HTML_PATH) / 1024
    print(f'✅ 대시보드 빌드 완료! 파일 크기: {file_size_kb:.1f} KB')

if __name__ == '__main__':
    main()
