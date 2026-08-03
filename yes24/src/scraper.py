"""
YES24 도서 데이터 수집 스크립트 (scraper.py)

이 모듈은 YES24 웹사이트에서 특정 카테고리의 도서 목록 데이터를 페이지별로 요청하여 수집하고,
각 도서의 세부 정보(제목, 저자, 출판사, 가격, 리뷰 수, 판매지수 등)를 파싱하여 CSV 파일로 저장하는 기능을 수행합니다.

주요 기능:
    - CategoryProductContents 비동기 API 엔드포인트를 호출하여 HTML 목록 데이터를 수집합니다.
    - BeautifulSoup을 사용하여 HTML 요소를 분석하고 필요한 데이터를 정밀하게 추출합니다.
    - 웹 서버 부하 방지를 위해 각 페이지 요청 사이에 1~2초의 랜덤 대기 시간을 적용합니다.
    - 수집 로그를 파일 및 콘솔에 동시에 기록하여 진행 상황을 추적할 수 있도록 지원합니다.
    - 수집된 결과는 pandas DataFrame을 거쳐 UTF-8-SIG 인코딩의 CSV 파일로 내보내집니다.
"""

import os
import time
import random
import logging
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 로깅 설정 (콘솔 및 파일 출력)
logger = logging.getLogger("Yes24Scraper")
logger.setLevel(logging.INFO)

# 기존 핸들러 제거 (중복 출력 방지)
if logger.handlers:
    logger.handlers.clear()

# 포맷터 설정
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 콘솔 핸들러 추가
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 저장할 디렉토리 및 파일 경로 계산
# yes24/src/scraper.py 기준으로 yes24/data/ 디렉토리를 가리키도록 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
output_csv_path = os.path.join(data_dir, "yes24_books.csv")

# data 디렉토리가 없으면 생성
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 파일 핸들러 추가
log_file_path = os.path.join(data_dir, "scraping.log")
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def clean_text(text):
    """텍스트의 좌우 공백 및 줄바꿈을 정제합니다.

    연속된 공백 문자(줄바꿈, 탭, 공백 등)를 하나의 공백으로 치환하고
    텍스트의 앞뒤에 있는 불필요한 공백을 제거합니다.

    Args:
        text (str): 정제 대상이 되는 원본 텍스트 문자열.

    Returns:
        str: 정제 처리가 완료된 문자열. 입력값이 빈 문자열이거나 None인 경우 빈 문자열을 반환합니다.
    """
    if text:
        return re.sub(r'\s+', ' ', text).strip()
    return ""

def parse_book_item(item):
    """HTML 요소에서 개별 도서 정보를 파싱합니다.

    BeautifulSoup Tag 객체로 제공되는 개별 도서 블록(itemUnit) 내의 하위 요소들을
    CSS 선택자를 이용하여 파싱하고 데이터를 딕셔너리 형태로 반환합니다.
    도서 제목이 없거나 파싱 중 오류가 발생할 경우 해당 도서는 수집에서 제외(None 반환)됩니다.

    Args:
        item (bs4.element.Tag): 개별 도서의 HTML 정보를 담고 있는 BeautifulSoup Tag 객체.

    Returns:
        dict or None: 파싱된 도서 데이터 딕셔너리. 필수 항목(제목)이 누락되었거나
                     예외가 발생한 경우에는 None을 반환합니다.
        
        딕셔너리 구조:
            - 제목 (str): 도서의 공식 제목.
            - 상세 정보 (str): 도서의 부제목 또는 추가 수식 문구.
            - 저자 (str): 쉼표(,)로 구분된 도서 저자 목록 (접미사 '저', '지음' 등은 제외됨).
            - 출판사 (str): 도서 출판사명.
            - 발행일 (str): 도서의 발행 연월.
            - 정가 (str): 숫자로 구성된 정가 문자열 (쉼표 및 '원' 표시 제외).
            - 판매가 (str): 숫자로 구성된 판매 가격 문자열 (쉼표 및 '원' 표시 제외).
            - 리뷰 수 (str): 회원 리뷰 개수 (숫자 형식).
            - 판매지수 (str): YES24 판매지수 값 (숫자 형식).
            - 설명 (str): 도서 소개 및 요약 내용.
            - 상세 페이지 URL (str): YES24 내 도서 상세 페이지로 연결되는 전체 URL 경로.
    """
    try:
        # 1. 제목
        name_el = item.select_one(".info_name a.gd_name")
        if not name_el:
            # 제목이 없는 경우 필수 데이터 누락으로 판단하여 수집 제외
            return None
        title = name_el.get_text(strip=True)
        
        # 상세 페이지 URL
        link = ""
        if name_el.get('href'):
            link = "https://www.yes24.com" + name_el.get('href')
            
        # 2. 상세 정보 (부제목)
        sub_title_el = item.select_one(".info_name span.gd_nameE")
        sub_title = sub_title_el.get_text(strip=True) if sub_title_el else ""
        
        # 3. 저자
        auth_el = item.select_one(".info_pubGrp .info_auth")
        author = ""
        if auth_el:
            author_links = auth_el.select("a")
            if author_links:
                author = ", ".join([a.get_text(strip=True) for a in author_links])
            else:
                author = auth_el.get_text(strip=True)
                # ' 저', ' 편', ' 역' 등의 접미사 제거
                author = re.sub(r'\s*(저|편|역|글|그림|역자|지음).*$', '', author).strip()
                
        # 4. 출판사
        pub_el = item.select_one(".info_pubGrp .info_pub")
        publisher = ""
        if pub_el:
            pub_links = pub_el.select("a")
            if pub_links:
                publisher = ", ".join([p.get_text(strip=True) for p in pub_links])
            else:
                publisher = pub_el.get_text(strip=True)
                
        # 5. 발행일
        date_el = item.select_one(".info_pubGrp .info_date")
        pub_date = date_el.get_text(strip=True) if date_el else ""
        
        # 6. 정가
        price_std_el = item.select_one(".info_price span.txt_num.dash em.yes_m")
        price_std = ""
        if price_std_el:
            price_std = price_std_el.get_text(strip=True).replace(",", "").replace("원", "")
            
        # 7. 판매가
        price_sale_el = item.select_one(".info_price strong.txt_num em.yes_b")
        price_sale = ""
        if price_sale_el:
            price_sale = price_sale_el.get_text(strip=True).replace(",", "").replace("원", "")
            
        # 정가가 없고 판매가만 있는 경우 동일하게 처리
        if not price_std and price_sale:
            price_std = price_sale
            
        # 8. 리뷰 수
        rv_el = item.select_one(".info_rating .rating_rvCount em.txC_blue")
        reviews = "0"
        if rv_el:
            reviews = rv_el.get_text(strip=True)
            
        # 9. 판매지수
        sales_index_el = item.select_one(".info_rating .saleNum")
        sales_index = "0"
        if sales_index_el:
            txt = sales_index_el.get_text(strip=True)
            digits = re.findall(r'\d+', txt.replace(",", ""))
            if digits:
                sales_index = digits[0]
                
        # 10. 설명
        desc_el = item.select_one(".info_read")
        desc = clean_text(desc_el.get_text()) if desc_el else ""
        
        return {
            "제목": title,
            "상세 정보": sub_title,
            "저자": author,
            "출판사": publisher,
            "발행일": pub_date,
            "정가": price_std,
            "판매가": price_sale,
            "리뷰 수": reviews,
            "판매지수": sales_index,
            "설명": desc,
            "상세 페이지 URL": link
        }
    except Exception as e:
        logger.warning(f"도서 파싱 중 오류 발생: {e}. 해당 항목은 건너뜁니다.")
        return None

def main():
    """YES24 도서 데이터 스크래핑 프로세스를 제어하는 메인 함수입니다.

    지정된 카테고리(dispNo)를 기준으로 여러 페이지에 걸쳐 도서 목록 API를 요청하고,
    응답받은 HTML 데이터를 파싱하여 리스트에 축적합니다.
    수집 완료 후 수집 데이터를 pandas DataFrame으로 변환하여 미리보기를 로깅하고,
    최종 결과물을 UTF-8-SIG 인코딩의 CSV 파일로 지정된 경로에 저장합니다.
    """
    logger.info("=== YES24 도서 데이터 수집 시작 ===")
    
    url = "https://www.yes24.com/product/category/CategoryProductContents"
    base_headers = {
        "host": "www.yes24.com",
        "referer": "https://www.yes24.com/product/category/display/001001003032",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    all_books = []
    
    start_page = 1
    end_page = 10
    page_size = 120
    
    for page in range(start_page, end_page + 1):
        logger.info(f"페이지 {page}/{end_page} 수집 중...")
        
        params = {
            "dispNo": "001001003032",
            "order": "SINDEX_ONLY",
            "addOptionTp": "0",
            "page": str(page),
            "size": str(page_size),
            "statGbYn": "N",
            "viewMode": "",
            "_options": "",
            "directDelvYn": "",
            "usedTp": "0",
            "elemNo": "0",
            "elemSeq": "0",
            "seriesNumber": "0"
        }
        
        try:
            response = requests.get(url, params=params, headers=base_headers, timeout=15)
            if response.status_code != 200:
                logger.error(f"페이지 {page} 호출 실패. Status Code: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select("div.itemUnit")
            
            if not items:
                logger.warning(f"페이지 {page}에서 상품 목록(itemUnit)을 찾을 수 없습니다.")
                continue
                
            page_books_count = 0
            for item in items:
                book_data = parse_book_item(item)
                if book_data:
                    all_books.append(book_data)
                    page_books_count += 1
            
            logger.info(f"페이지 {page} 수집 완료: {page_books_count}개 도서 파싱 성공 (누적: {len(all_books)}개)")
            
        except Exception as e:
            logger.error(f"페이지 {page} 처리 중 예상치 못한 오류 발생: {e}")
            
        # 디스크립션에 기재된 1-2초 사이의 대기 시간 (랜덤으로 변동을 주어 차단 방지)
        sleep_time = random.uniform(1.0, 2.0)
        logger.info(f"{sleep_time:.2f}초 대기 후 다음 페이지로 이동합니다.")
        time.sleep(sleep_time)
        
    logger.info("수집 완료. 데이터프레임 변환 및 CSV 저장을 시작합니다.")
    
    if all_books:
        # 데이터프레임 변환
        df = pd.DataFrame(all_books)
        
        # 일부 데이터 미리보기 출력
        logger.info("수집 데이터 일부:")
        logger.info("\n" + df.head(3).to_string(index=False))
        
        # CSV 파일 저장
        try:
            df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
            logger.info(f"데이터 저장 완료: {output_csv_path} (총 {len(df)}개 행)")
        except Exception as e:
            logger.error(f"CSV 저장 중 오류 발생: {e}")
    else:
        logger.error("수집된 데이터가 존재하지 않습니다.")

if __name__ == "__main__":
    main()
