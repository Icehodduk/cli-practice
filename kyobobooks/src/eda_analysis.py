"""
교보문고 IT/컴퓨터 베스트셀러 데이터셋 심층 탐색적 데이터 분석(EDA) 스크립트
작성자: 20년차 베테랑 전문 데이터 분석가
"""

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer

# 출력 및 이미지 저장 디렉터리 설정
IMAGE_DIR = 'kyobobooks/images'
DATA_PATH = 'kyobobooks/data/bestseller_cleaned.csv'
os.makedirs(IMAGE_DIR, exist_ok=True)

# 1. 데이터 로드 및 전처리
df = pd.read_csv(DATA_PATH)

# 출간일 전처리: YYYYMMDD -> 연도, 월, 연월 추출
df['출간일_str'] = df['출간일'].astype(str)
df['출간연도'] = df['출간일_str'].str[:4].astype(int)
df['출간월'] = df['출간일_str'].str[4:6].astype(int)
df['출간연월'] = df['출간일_str'].str[:4] + '-' + df['출간일_str'].str[4:6]

# 가격대 구간 생성
price_bins = [0, 15000, 20000, 25000, 30000, 40000, 100000]
price_labels = ['1.5만원 미만', '1.5만~2만원', '2만~2.5만원', '2.5만~3만원', '3만~4만원', '4만원 이상']
df['가격대'] = pd.cut(df['판매가'], bins=price_bins, labels=price_labels)

# 순위 구간 생성 (50위 단위)
rank_bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 500]
rank_labels = ['1~50위', '51~100위', '101~150위', '151~200위', '201~250위', '251~300위', '301~350위', '351~400위', '401위 이상']
df['순위구간'] = pd.cut(df['순위'], bins=rank_bins, labels=rank_labels)

# 시각화 기본 설정 (seaborn 테마 설정 미사용, 순수 matplotlib 스타일 기반)
plt.rcParams['font.family'] = 'NanumGothic' if 'NanumGothic' in plt.rcParams['font.sans-serif'] else plt.rcParams['font.family']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

# -------------------------------------------------------------
# 1. 시각화 1: 도서 판매가 분포 (Histogram & KDE)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
counts, bins, patches = ax.hist(df['판매가'], bins=25, color='#2b5c8f', edgecolor='white', alpha=0.85, density=True)
df['판매가'].plot(kind='kde', ax=ax, color='#e74c3c', linewidth=2.5, label='밀도 추정선(KDE)')
ax.set_title('교보문고 IT 베스트셀러 도서 판매가 분포', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('판매가 (원)', fontsize=12)
ax.set_ylabel('확률 밀도 (Density)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
ax.legend(loc='upper right', fontsize=11)
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/01_price_distribution.png')
plt.close()

# -------------------------------------------------------------
# 2. 시각화 2: 도서 판매가 박스플롯 (Box Plot)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
bp = ax.boxplot(df['판매가'], vert=False, patch_artist=True,
                boxprops=dict(facecolor='#4a90e2', color='#1f4788', alpha=0.7),
                whiskerprops=dict(color='#1f4788', linewidth=1.5),
                capprops=dict(color='#1f4788', linewidth=1.5),
                medianprops=dict(color='#d9534f', linewidth=2.5),
                flierprops=dict(marker='o', markerfacecolor='#d9534f', markeredgecolor='none', alpha=0.6))
ax.set_title('도서 판매가 사분위 및 이상치 분포 (Box Plot)', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('판매가 (원)', fontsize=12)
ax.set_yticks([])
ax.grid(True, linestyle='--', alpha=0.5, axis='x')
median_val = df['판매가'].median()
mean_val = df['판매가'].mean()
ax.axvline(median_val, color='#d9534f', linestyle='--', label=f'중앙값: {int(median_val):,}원')
ax.axvline(mean_val, color='#27ae60', linestyle=':', label=f'평균값: {int(mean_val):,}원')
ax.legend(loc='upper right', fontsize=11)
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/02_price_boxplot.png')
plt.close()

# -------------------------------------------------------------
# 3. 시각화 3: 출간 연도별 베스트셀러 도서 수 추이 (Bar Plot)
# -------------------------------------------------------------
year_counts = df['출간연도'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(year_counts.index.astype(str), year_counts.values, color='#34495e', edgecolor='white', alpha=0.85)
ax.set_title('연도별 베스트셀러 등재 도서 수 추이', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('출간 연도', fontsize=12)
ax.set_ylabel('도서 권수 (권)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
for bar in bars:
    yval = bar.get_height()
    if yval > 0:
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f'{int(yval)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/03_publication_year_trend.png')
plt.close()

# -------------------------------------------------------------
# 4. 시각화 4: 베스트셀러 점유 상위 20개 출판사 빈도 (Horizontal Bar Plot)
# -------------------------------------------------------------
top_pubs = df['출판사'].value_counts().head(20).iloc[::-1]
fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(top_pubs.index, top_pubs.values, color='#2980b9', edgecolor='white', alpha=0.85)
ax.set_title('베스트셀러 도서 수 상위 20개 출판사 점유 현황', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('베스트셀러 도서 권수 (권)', fontsize=12)
ax.set_ylabel('출판사명', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='x')
for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 0.8, bar.get_y() + bar.get_height()/2.0, f'{int(xval)}권', ha='left', va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/04_top_publishers.png')
plt.close()

# -------------------------------------------------------------
# 5. 시각화 5: 베스트셀러 다작 저자 상위 20인 빈도 (Horizontal Bar Plot)
# -------------------------------------------------------------
top_authors = df['저자'].value_counts().head(20).iloc[::-1]
fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(top_authors.index, top_authors.values, color='#16a085', edgecolor='white', alpha=0.85)
ax.set_title('베스트셀러 다작 저자 상위 20인 도서 수 현황', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('베스트셀러 도서 권수 (권)', fontsize=12)
ax.set_ylabel('저자명', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='x')
for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 0.2, bar.get_y() + bar.get_height()/2.0, f'{int(xval)}권', ha='left', va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/05_top_authors.png')
plt.close()

# -------------------------------------------------------------
# 6. 시각화 6: 순위 구간별 평균 판매가 비교 (Bar & Line Plot)
# -------------------------------------------------------------
rank_price_summary = df.groupby('순위구간', observed=True)['판매가'].agg(['mean', 'median', 'count']).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(rank_price_summary))
bars = ax.bar(x, rank_price_summary['mean'], color='#4a69bd', width=0.55, alpha=0.85, label='평균 판매가')
ax.plot(x, rank_price_summary['median'], color='#eb2f06', marker='o', linewidth=2.5, label='중앙값 판매가')
ax.set_xticks(x)
ax.set_xticklabels(rank_price_summary['순위구간'], rotation=15, ha='right', fontsize=11)
ax.set_title('순위 구간(Tier)별 평균 및 중앙값 판매가 비교', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('순위 구간', fontsize=12)
ax.set_ylabel('판매가 (원)', fontsize=12)
ax.set_ylim(15000, 32000)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
ax.legend(loc='upper right', fontsize=11)
for i, mean_val in enumerate(rank_price_summary['mean']):
    ax.text(i, mean_val + 400, f'{int(mean_val):,}원', ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/06_rank_tier_price.png')
plt.close()

# -------------------------------------------------------------
# 7. 시각화 7: 주요 상위 10개 출판사별 판매가 분포 비교 (Box Plot)
# -------------------------------------------------------------
top10_pubs = df['출판사'].value_counts().head(10).index.tolist()
top10_pub_data = [df[df['출판사'] == pub]['판매가'].values for pub in top10_pubs]

fig, ax = plt.subplots(figsize=(13, 7))
bp = ax.boxplot(top10_pub_data, patch_artist=True, tick_labels=top10_pubs,
                boxprops=dict(facecolor='#82ccdd', color='#0a3d62', alpha=0.7),
                whiskerprops=dict(color='#0a3d62', linewidth=1.5),
                capprops=dict(color='#0a3d62', linewidth=1.5),
                medianprops=dict(color='#e55039', linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='#e55039', markeredgecolor='none', alpha=0.5))
ax.set_title('주요 상위 10대 출판사별 판매가 분포 비교 (Box Plot)', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('출판사명', fontsize=12)
ax.set_ylabel('판매가 (원)', fontsize=12)
ax.set_xticklabels(top10_pubs, rotation=25, ha='right', fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5, axis='y')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/07_top_publishers_price_boxplot.png')
plt.close()

# -------------------------------------------------------------
# 8. 시각화 8: 최근 출간 연도별 평균 및 중앙값 판매가 추이 (Line Plot)
# -------------------------------------------------------------
yearly_price = df[df['출간연도'] >= 2018].groupby('출간연도')['판매가'].agg(['mean', 'median', 'std', 'count']).reset_index()
fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(yearly_price['출간연도'].astype(str), yearly_price['mean'], marker='s', color='#1e3799', linewidth=2.5, markersize=8, label='평균 판매가')
ax.plot(yearly_price['출간연도'].astype(str), yearly_price['median'], marker='^', color='#f6b93b', linewidth=2.5, markersize=8, label='중앙값 판매가')
ax.set_title('최근 출간 연도별(2018~2026) 도서 판매가 변동 추이', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('출간 연도', fontsize=12)
ax.set_ylabel('판매가 (원)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='lower right', fontsize=11)
for i, row in yearly_price.iterrows():
    ax.text(i, row['mean'] + 500, f'{int(row["mean"]):,}원', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/08_yearly_price_trend.png')
plt.close()

# -------------------------------------------------------------
# 9. 시각화 9: 주요 출판사 상위 8개사의 최근 연도별 출간 도서 수 히트맵
# -------------------------------------------------------------
top8_pubs = df['출판사'].value_counts().head(8).index.tolist()
recent_years = [2022, 2023, 2024, 2025, 2026]
sub_df = df[(df['출판사'].isin(top8_pubs)) & (df['출간연도'].isin(recent_years))]
pivot_table = pd.crosstab(sub_df['출판사'], sub_df['출간연도']).reindex(index=top8_pubs, columns=recent_years, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 7))
cax = ax.matshow(pivot_table.values, cmap='YlGnBu', alpha=0.85)
fig.colorbar(cax)
ax.set_xticks(range(len(recent_years)))
ax.set_xticklabels([str(y) + '년' for y in recent_years], fontsize=11)
ax.set_yticks(range(len(top8_pubs)))
ax.set_yticklabels(top8_pubs, fontsize=11)
ax.xaxis.set_ticks_position('bottom')
ax.set_title('주요 출판사 상위 8개사의 최근 연도별 출간 권수 매트릭스', fontsize=15, pad=15, fontweight='bold')
for i in range(len(top8_pubs)):
    for j in range(len(recent_years)):
        val = pivot_table.values[i, j]
        text_color = 'white' if val > pivot_table.values.max() * 0.55 else 'black'
        ax.text(j, i, f'{val}권', ha='center', va='center', color=text_color, fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/09_publisher_year_heatmap.png')
plt.close()

# -------------------------------------------------------------
# 10. 시각화 10: 순위 vs 판매가 산점도 및 가격대별 분포
# -------------------------------------------------------------
colors_map = {
    '1.5만원 미만': '#3498db',
    '1.5만~2만원': '#2ecc71',
    '2만~2.5만원': '#f1c40f',
    '2.5만~3만원': '#e67e22',
    '3만~4만원': '#e74c3c',
    '4만원 이상': '#9b59b6'
}
fig, ax = plt.subplots(figsize=(12, 7))
for label, group in df.groupby('가격대', observed=True):
    ax.scatter(group['순위'], group['판매가'], label=label, color=colors_map[label], alpha=0.75, edgecolors='w', s=55)

z = np.polyfit(df['순위'], df['판매가'], 1)
p = np.poly1d(z)
ax.plot(df['순위'], p(df['순위']), color='#2c3e50', linestyle='--', linewidth=2, label=f'선형 추세선 (기울기={z[0]:.2f})')

ax.set_title('베스트셀러 순위와 판매가 간의 다변량 산점도 및 추세 분석', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('베스트셀러 순위 (Rank)', fontsize=12)
ax.set_ylabel('판매가 (원)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(title='가격대 구간', loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/10_rank_vs_price_scatter.png')
plt.close()

# -------------------------------------------------------------
# 11. 시각화 11: 도서명 및 소개글 핵심 키워드 TF-IDF 상위 30개
# -------------------------------------------------------------
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
top30_keywords = sorted(zip(tfidf.get_feature_names_out(), scores), key=lambda x: x[1], reverse=True)[:30]

kw_df = pd.DataFrame(top30_keywords, columns=['키워드', 'TFIDF_합계'])
kw_df_sorted = kw_df.iloc[::-1]

fig, ax = plt.subplots(figsize=(12, 10))
bars = ax.barh(kw_df_sorted['키워드'], kw_df_sorted['TFIDF_합계'], color='#e17055', edgecolor='white', alpha=0.85)
ax.set_title('도서명 및 소개글 핵심 키워드 상위 30개 (TF-IDF 점수 합계)', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('TF-IDF 중요도 점수 합계', fontsize=12)
ax.set_ylabel('키워드', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5, axis='x')
for bar in bars:
    xval = bar.get_width()
    ax.text(xval + 0.5, bar.get_y() + bar.get_height()/2.0, f'{xval:.1f}', ha='left', va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{IMAGE_DIR}/11_tfidf_top30_keywords.png')
plt.close()

print('모든 11개 시각화 이미지 생성이 완료되었습니다.')
