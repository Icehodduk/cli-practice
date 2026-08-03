# -*- coding: utf-8 -*-
"""
YES24 도서 데이터 EDA 및 시각화 수행 스크립트
작성일: 2026-07-15
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer

def run_profiling(df):
    """
    데이터 프로파일링 및 기초 분석 정보를 텍스트로 추출하여 반환합니다.
    """
    profile_text = []
    profile_text.append("### 1. 데이터 프로파일링 결과\n")
    profile_text.append(f"- **전체 데이터 크기**: {df.shape[0]}행, {df.shape[1]}열")
    
    # 중복 데이터
    duplicated_rows = df.duplicated().sum()
    profile_text.append(f"- **중복 데이터 수**: {duplicated_rows}행")
    if duplicated_rows > 0:
        profile_text.append("  - *조치 계획*: 중복된 데이터가 존재할 경우 필요 시 제거하거나 분석 목적에 맞게 정제합니다.")
    else:
        profile_text.append("  - *조치 계획*: 중복 데이터가 없으므로 정제 불필요.")
        
    # 결측치 정보
    profile_text.append("\n- **컬럼별 결측치 현황**:\n")
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        profile_text.append(f"  - `{col}`: {count}개 결측치")
        
    # 수치형 변수 기술통계량
    profile_text.append("\n- **수치형 변수 기술통계량**:\n")
    desc_num = df.describe()
    profile_text.append(desc_num.to_markdown())
    
    # 범주형 변수 기술통계량
    profile_text.append("\n- **범주형 변수 기술통계량**:\n")
    desc_cat = df.describe(include=[object])
    profile_text.append(desc_cat.to_markdown())
    
    return "\n".join(profile_text)

def preprocess_data(df):
    """
    데이터 전처리를 수행합니다.
    """
    # 1. 발행일 전처리 (YYYY-MM-DD 형식으로 가정하고 연도, 월 추출)
    # 발행일이 문자열 형태로 들어있으므로 연도와 월을 추출합니다.
    df['발행일'] = df['발행일'].astype(str)
    # 간단하게 'YYYY' 패턴이나 '-' 분할로 추출
    df['발행연도'] = df['발행일'].str.slice(0, 4)
    df['발행월'] = df['발행일'].str.slice(5, 7)
    
    # 2. 할인율 계산
    # 정가가 0인 경우 분모가 0이 되는 것을 방지
    df['할인율'] = np.where(df['정가'] > 0, (df['정가'] - df['판매가']) / df['정가'], 0)
    
    return df

def generate_visualizations(df, img_dir):
    """
    10개 이상의 시각화 그래프를 생성하고 이미지로 저장합니다.
    각 그래프의 요약 표 데이터도 생성하여 반환합니다.
    """
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        
    viz_tables = {}
    
    # 공통 그래프 스타일링 설정 (Seaborn 테마 사용 금지)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    
    # 컬러 정의
    PRIMARY_COLOR = '#1B365D' # 네이비
    SECONDARY_COLOR = '#4682B4' # 스틸 블루
    ACCENT_COLOR = '#D9534F' # 연한 레드
    
    # 1. 정가 및 판매가 분포 (Histogram/KDE)
    plt.figure()
    plt.hist(df['정가'], bins=30, alpha=0.6, color=PRIMARY_COLOR, label='정가')
    plt.hist(df['판매가'], bins=30, alpha=0.6, color=SECONDARY_COLOR, label='판매가')
    plt.title('도서 정가 및 판매가 분포')
    plt.xlabel('가격 (원)')
    plt.ylabel('도서 수 (권)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '01_price_distribution.png'))
    plt.close()
    
    price_summary = df[['정가', '판매가']].describe()
    viz_tables['01_price_distribution'] = price_summary.to_markdown()
    
    # 2. 할인율 분포 (Histogram)
    plt.figure()
    plt.hist(df['할인율'] * 100, bins=20, color=SECONDARY_COLOR, edgecolor='white')
    plt.title('도서 할인율 분포')
    plt.xlabel('할인율 (%)')
    plt.ylabel('도서 수 (권)')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '02_discount_rate_distribution.png'))
    plt.close()
    
    discount_summary = pd.DataFrame(df['할인율'] * 100).describe()
    viz_tables['02_discount_rate_distribution'] = discount_summary.to_markdown()
    
    # 3. 판매지수 분포 (Boxplot)
    plt.figure()
    plt.boxplot(df['판매지수'], vert=False, patch_artist=True,
                boxprops=dict(facecolor=SECONDARY_COLOR, color=PRIMARY_COLOR),
                medianprops=dict(color=ACCENT_COLOR, linewidth=2))
    plt.title('도서 판매지수 분포')
    plt.xlabel('판매지수')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '03_sales_index_distribution.png'))
    plt.close()
    
    sales_index_summary = pd.DataFrame(df['판매지수']).describe()
    viz_tables['03_sales_index_distribution'] = sales_index_summary.to_markdown()
    
    # 4. 리뷰 수 분포 (Boxplot)
    plt.figure()
    plt.boxplot(df['리뷰 수'], vert=False, patch_artist=True,
                boxprops=dict(facecolor=SECONDARY_COLOR, color=PRIMARY_COLOR),
                medianprops=dict(color=ACCENT_COLOR, linewidth=2))
    plt.title('도서 리뷰 수 분포')
    plt.xlabel('리뷰 수')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '04_review_count_distribution.png'))
    plt.close()
    
    review_summary = pd.DataFrame(df['리뷰 수']).describe()
    viz_tables['04_review_count_distribution'] = review_summary.to_markdown()
    
    # 5. 발행일 연도별 추이 (Bar Chart)
    # 발행연도별 도서 수 집계
    year_counts = df['발행연도'].value_counts().sort_index()
    plt.figure()
    plt.bar(year_counts.index, year_counts.values, color=PRIMARY_COLOR)
    plt.title('연도별 도서 발행 건수 추이')
    plt.xlabel('발행연도')
    plt.ylabel('도서 수 (권)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '05_yearly_publish_trend.png'))
    plt.close()
    
    viz_tables['05_yearly_publish_trend'] = pd.DataFrame(year_counts).rename(columns={'count': '도서 수'}).to_markdown()
    
    # 6. 판매가 vs 판매지수 상관관계 (Scatter Plot)
    plt.figure()
    plt.scatter(df['판매가'], df['판매지수'], alpha=0.5, color=SECONDARY_COLOR)
    plt.title('도서 판매가와 판매지수의 상관관계')
    plt.xlabel('판매가 (원)')
    plt.ylabel('판매지수')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '06_price_vs_sales_index.png'))
    plt.close()
    
    corr_price_sales = df[['판매가', '판매지수']].corr()
    viz_tables['06_price_vs_sales_index'] = corr_price_sales.to_markdown()
    
    # 7. 판매지수 vs 리뷰 수 상관관계 (Scatter Plot)
    plt.figure()
    plt.scatter(df['판매지수'], df['리뷰 수'], alpha=0.5, color=PRIMARY_COLOR)
    plt.title('판매지수와 리뷰 수의 상관관계')
    plt.xlabel('판매지수')
    plt.ylabel('리뷰 수')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '07_sales_index_vs_reviews.png'))
    plt.close()
    
    corr_sales_reviews = df[['판매지수', '리뷰 수']].corr()
    viz_tables['07_sales_index_vs_reviews'] = corr_sales_reviews.to_markdown()
    
    # 8. 주요 출판사 상위 30개 점유율 (Horizontal Bar Chart)
    pub_counts = df['출판사'].value_counts().head(30)
    plt.figure(figsize=(10, 8))
    plt.barh(pub_counts.index[::-1], pub_counts.values[::-1], color=SECONDARY_COLOR)
    plt.title('상위 30개 출판사 도서 발행 수')
    plt.xlabel('도서 수 (권)')
    plt.ylabel('출판사')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '08_top_publishers.png'))
    plt.close()
    
    viz_tables['08_top_publishers'] = pd.DataFrame(pub_counts).rename(columns={'count': '도서 수'}).to_markdown()
    
    # 9. 주요 저자 상위 30개 점유율 (Horizontal Bar Chart)
    author_counts = df['저자'].value_counts().head(30)
    plt.figure(figsize=(10, 8))
    plt.barh(author_counts.index[::-1], author_counts.values[::-1], color=PRIMARY_COLOR)
    plt.title('상위 30개 저자 도서 발행 수')
    plt.xlabel('도서 수 (권)')
    plt.ylabel('저자')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '09_top_authors.png'))
    plt.close()
    
    viz_tables['09_top_authors'] = pd.DataFrame(author_counts).rename(columns={'count': '도서 수'}).to_markdown()
    
    # 10. 도서 설명/제목 텍스트 키워드 분석 (TF-IDF 상위 30개 Bar Chart)
    # 설명의 결측치를 빈 문자열로 대체
    texts = (df['제목'].fillna('') + ' ' + df['설명'].fillna('')).tolist()
    
    # TF-IDF 벡터라이저 사용 (Okt/Mecab 등 형태소 분석기는 속도 문제로 사용 배제)
    # 한국어 불용어 처리 등을 위해 글자 수 2글자 이상 단어만 추출
    vectorizer = TfidfVectorizer(max_features=1000, token_pattern=r'\b[가-힣a-zA-Z]{2,}\b')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # 피처별 평균 TF-IDF 계산
    feature_names = vectorizer.get_feature_names_out()
    mean_tfidf = tfidf_matrix.mean(axis=0).A1
    
    # 상위 30개 키워드 추출
    top_indices = mean_tfidf.argsort()[::-1][:30]
    top_keywords = [feature_names[i] for i in top_indices]
    top_scores = [mean_tfidf[i] for i in top_indices]
    
    plt.figure(figsize=(10, 8))
    plt.barh(top_keywords[::-1], top_scores[::-1], color=SECONDARY_COLOR)
    plt.title('도서 제목 및 설명 키워드 TF-IDF 상위 30선')
    plt.xlabel('평균 TF-IDF 가중치')
    plt.ylabel('키워드')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, '10_text_keywords.png'))
    plt.close()
    
    keyword_df = pd.DataFrame({'키워드': top_keywords, '평균 TF-IDF 가중치': top_scores})
    viz_tables['10_text_keywords'] = keyword_df.to_markdown(index=False)
    
    return viz_tables

if __name__ == '__main__':
    # 경로 설정
    csv_path = 'yes24/data/yes24_books.csv'
    img_dir = 'yes24/images'
    
    # 1. 데이터 로드
    df = pd.read_csv(csv_path)
    
    # 2. 프로파일링 수행
    profiling_result = run_profiling(df)
    
    # 3. 전처리 수행
    df = preprocess_data(df)
    
    # 4. 시각화 그래프 생성 및 표 데이터 수집
    viz_tables = generate_visualizations(df, img_dir)
    
    # 프로파일링 및 표 정보 저장 (리포트 자동 생성용 중간 파일)
    # eda_results_temp.txt 에 저장
    temp_path = 'yes24/data/eda_results_temp.txt'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(profiling_result)
        f.write("\n\n=== VIZ TABLES ===\n\n")
        for key, val in viz_tables.items():
            f.write(f"--- {key} ---\n")
            f.write(val)
            f.write("\n\n")
            
    print("EDA 전처리 및 시각화가 완료되었습니다. 임시 분석 결과가 저장되었습니다.")
