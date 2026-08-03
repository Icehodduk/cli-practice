import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (Mac OS용 AppleGothic 설정)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 경로 설정 (상대 경로 기준)
DATA_PATH = 'yes24/data/yes24_books.csv'
IMAGE_DIR = 'yes24/images'
os.makedirs(IMAGE_DIR, exist_ok=True)

def clean_numeric(val):
    """숫자형 문자열에서 쉼표 등을 제거하고 float로 변환하는 함수"""
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    # 숫자와 소수점만 추출
    cleaned = re.sub(r'[^\d.]', '', val_str)
    return float(cleaned) if cleaned else None

def parse_year(date_str):
    """발행일 문자열에서 연도를 추출하는 함수 (예: '2026년 05월' -> 2026)"""
    if pd.isna(date_str):
        return None
    match = re.search(r'(\d{4})년', str(date_str))
    if match:
        return int(match.group(1))
    # '2026-05' 등 다른 형식 대비
    match = re.search(r'(\d{4})', str(date_str))
    return int(match.group(1)) if match else None

def parse_month(date_str):
    """발행일 문자열에서 월을 추출하는 함수 (예: '2026년 05월' -> 5)"""
    if pd.isna(date_str):
        return None
    match = re.search(r'(\d{2})월', str(date_str))
    if match:
        return int(match.group(1))
    return None

def main():
    print("=== [1] 데이터 로드 및 확인 ===")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {DATA_PATH}")
        
    df = pd.read_csv(DATA_PATH)
    print(f"데이터 크기: {df.shape[0]}행, {df.shape[1]}열")
    print("\n컬럼 정보:")
    print(df.info())
    
    print("\n결측치 현황:")
    print(df.isnull().sum())

    print("\n=== [2] 데이터 전처리 ===")
    # 수치형 데이터 정리
    df['정가_clean'] = df['정가'].apply(clean_numeric)
    df['판매가_clean'] = df['판매가'].apply(clean_numeric)
    df['리뷰 수_clean'] = df['리뷰 수'].apply(clean_numeric).fillna(0).astype(int)
    df['판매지수_clean'] = df['판매지수'].apply(clean_numeric).fillna(0).astype(int)
    
    # 발행 연도 및 월 파생변수 생성
    df['발행연도'] = df['발행일'].apply(parse_year)
    df['발행월'] = df['발행일'].apply(parse_month)
    
    # 할인율 계산 (정가가 유효하고 0보다 큰 경우에만 계산)
    df['할인율'] = 0.0
    valid_price_mask = (df['정가_clean'] > 0) & (df['판매가_clean'] > 0)
    df.loc[valid_price_mask, '할인율'] = (
        (df.loc[valid_price_mask, '정가_clean'] - df.loc[valid_price_mask, '판매가_clean']) 
        / df.loc[valid_price_mask, '정가_clean'] * 100
    )
    
    print("전처리 완료 후 수치 데이터 기술통계:")
    print(df[['정가_clean', '판매가_clean', '리뷰 수_clean', '판매지수_clean', '할인율']].describe())

    print("\n=== [3] 시각화 생성 ===")
    
    # 시각화 1: 가격 및 할인율 분포
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # 가격 분포 (정가 & 판매가 비교)
    sns.histplot(df['정가_clean'].dropna(), color='blue', label='정가', kde=True, ax=axes[0], alpha=0.5)
    sns.histplot(df['판매가_clean'].dropna(), color='red', label='판매가', kde=True, ax=axes[0], alpha=0.5)
    axes[0].set_title('정가 및 판매가 분포')
    axes[0].set_xlabel('가격 (원)')
    axes[0].set_ylabel('도서 수')
    axes[0].legend()
    
    # 할인율 분포
    sns.histplot(df[df['할인율'] > 0]['할인율'], color='purple', kde=True, ax=axes[1], bins=15)
    axes[1].set_title('할인율 분포 (할인 적용 도서 기준)')
    axes[1].set_xlabel('할인율 (%)')
    axes[1].set_ylabel('도서 수')
    
    plt.tight_layout()
    plt.savefig(f'{IMAGE_DIR}/price_discount_dist.png', dpi=300)
    plt.close()
    print("- 가격 및 할인율 분포 시각화 완료: price_discount_dist.png")

    # 시각화 2: 발행 트렌드 (연도별 도서 수)
    plt.figure(figsize=(10, 5))
    year_counts = df['발행연도'].value_counts().sort_index()
    if not year_counts.empty:
        sns.barplot(x=year_counts.index.astype(int), y=year_counts.values, palette='viridis')
        plt.title('연도별 도서 출판 수 추이')
        plt.xlabel('발행연도')
        plt.ylabel('도서 수')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{IMAGE_DIR}/publish_trend.png', dpi=300)
    plt.close()
    print("- 연도별 발행 트렌드 시각화 완료: publish_trend.png")

    # 시각화 3: 판매지수와 리뷰 수의 상관분석
    plt.figure(figsize=(8, 6))
    # 데이터 스케일 차이가 크므로 로그 스케일 적용 고려하되, 산점도와 회귀선 표시
    sns.regplot(data=df, x='리뷰 수_clean', y='판매지수_clean', color='darkgreen', 
                scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
    plt.title('리뷰 수와 판매지수 간의 상관관계')
    plt.xlabel('리뷰 수')
    plt.ylabel('판매지수')
    
    # 피어슨 상관계수 계산
    corr = df['리뷰 수_clean'].corr(df['판매지수_clean'])
    plt.annotate(f'Pearson r = {corr:.2f}', xy=(0.05, 0.95), xycoords='axes fraction',
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
    plt.tight_layout()
    plt.savefig(f'{IMAGE_DIR}/sales_review_corr.png', dpi=300)
    plt.close()
    print(f"- 리뷰 수와 판매지수 상관관계 시각화 완료 (상관계수: {corr:.2f}): sales_review_corr.png")

    # 시각화 4: 주요 출판사 및 저자 (Top 10)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top 10 출판사
    top_publishers = df['출판사'].value_counts().head(10)
    sns.barplot(x=top_publishers.values, y=top_publishers.index, ax=axes[0], palette='Blues_r')
    axes[0].set_title('도서 등록 수 상위 10개 출판사')
    axes[0].set_xlabel('도서 수')
    
    # Top 10 저자
    top_authors = df['저자'].value_counts().head(10)
    sns.barplot(x=top_authors.values, y=top_authors.index, ax=axes[1], palette='Oranges_r')
    axes[1].set_title('도서 등록 수 상위 10개 저자')
    axes[1].set_xlabel('도서 수')
    
    plt.tight_layout()
    plt.savefig(f'{IMAGE_DIR}/top_publishers_authors.png', dpi=300)
    plt.close()
    print("- 인기 출판사 및 저자 시각화 완료: top_publishers_authors.png")

    # 시각화 5: 제목 키워드 빈도 분석 (명사 위주 추출을 위한 텍스트 처리)
    plt.figure(figsize=(10, 6))
    # 제목에서 특수문자를 제거하고 공백 기준으로 나눔
    all_titles = " ".join(df['제목'].dropna().astype(str))
    # 한글 및 영어 단어만 추출 (2글자 이상)
    words = re.findall(r'[가-힣a-zA-Z]{2,}', all_titles)
    
    # 한글 분석을 위한 기본 불용어(조사, 의미 없는 단어 등)
    stopwords = {'위한', '으로', '에서', '하고', '하는', '도서', '책을', '있는', '있습니다', '코드', 'with', 'and', 'the', '해서', '어떻게'}
    filtered_words = [w for w in words if w.lower() not in stopwords]
    
    word_series = pd.Series(filtered_words)
    top_words = word_series.value_counts().head(20)
    
    sns.barplot(x=top_words.values, y=top_words.index, palette='magma')
    plt.title('도서 제목 핵심 키워드 빈도 (상위 20개)')
    plt.xlabel('출현 빈도')
    plt.ylabel('키워드')
    plt.tight_layout()
    plt.savefig(f'{IMAGE_DIR}/title_keyword_freq.png', dpi=300)
    plt.close()
    print("- 제목 키워드 빈도 시각화 완료: title_keyword_freq.png")

    print("\n=== [4] 추가 분석 정보 출력 (리포트용) ===")
    print(f"1. 전체 등록 도서 수: {len(df)}권")
    
    if not df['정가_clean'].dropna().empty:
        max_price_idx = df['정가_clean'].idxmax()
        print(f"2. 최고가 도서: '{df.loc[max_price_idx, '제목']}' (정가: {df.loc[max_price_idx, '정가_clean']:,.0f}원)")
        print(f"3. 평균 정가: {df['정가_clean'].mean():,.0f}원 / 평균 판매가: {df['판매가_clean'].mean():,.0f}원")
        print(f"4. 평균 할인율: {df['할인율'].mean():.2f}%")
        
    print(f"5. 리뷰가 가장 많은 도서: '{df.loc[df['리뷰 수_clean'].idxmax(), '제목']}' (리뷰 수: {df['리뷰 수_clean'].max()}개)")
    print(f"6. 판매지수가 가장 높은 도서: '{df.loc[df['판매지수_clean'].idxmax(), '제목']}' (판매지수: {df['판매지수_clean'].max():,})")
    
    # 발행년도 상위 연도
    if not df['발행연도'].dropna().empty:
        top_year = df['발행연도'].value_counts().idxmax()
        print(f"7. 가장 많은 책이 발행된 연도: {int(top_year)}년 ({df['발행연도'].value_counts().max()}권)")

if __name__ == '__main__':
    main()
