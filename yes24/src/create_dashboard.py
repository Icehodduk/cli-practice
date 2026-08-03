# -*- coding: utf-8 -*-
"""
YES24 도서 데이터를 기반으로 서식이 적용된 엑셀 대시보드를 생성하는 스크립트입니다.
추가 요구사항: 상위 7개 출판사별 개별 시트 및 기타 출판사 통합 시트 자동 생성 및 수식 요약 행 적용
작성일: 2026-07-15
"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

def create_excel_dashboard(csv_path, output_path):
    # 1. 데이터 로드 및 사전 전처리
    df = pd.read_csv(csv_path)
    
    # 발행일로부터 연도 추출
    df['발행일'] = df['발행일'].astype(str)
    df['발행연도'] = df['발행일'].str.slice(0, 4)
    df['발행월'] = df['발행일'].str.slice(5, 7)
    
    # 고유 연도 목록 추출 (정렬)
    years = sorted(df['발행연도'].unique())
    # 상위 15개 출판사 추출 (대시보드 참조용)
    top_publishers = df['출판사'].value_counts().head(15).index.tolist()
    
    # 상위 7개 출판사 정의 (개별 시트 분리용)
    top_7_publishers = ["커뮤니케이션북스", "한빛미디어", "길벗", "제이펍", "골든래빗", "앤써북", "위키북스"]
    
    # 2. openpyxl Workbook 생성
    wb = Workbook()
    
    # 기본 생성된 시트를 Dashboard로 변경
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    
    # 기본 분석 및 원본 데이터 시트 생성
    ws_analysis = wb.create_sheet("Analysis_Data")
    ws_raw = wb.create_sheet("Raw_Data")
    
    # 3. 스타일 정의
    font_name = '맑은 고딕'
    
    # 폰트 스타일
    font_title = Font(name=font_name, size=18, bold=True, color='FFFFFF')
    font_section = Font(name=font_name, size=14, bold=True, color='1B365D')
    font_header = Font(name=font_name, size=11, bold=True, color='FFFFFF')
    font_kpi_title = Font(name=font_name, size=9, bold=True, color='555555')
    font_kpi_value = Font(name=font_name, size=16, bold=True, color='000000') # 수식 결과 검은색
    
    # 텍스트 표준 색상 폰트
    font_black = Font(name=font_name, size=11, color='000000') # 수식 결과 (검은색)
    font_blue = Font(name=font_name, size=11, color='0000FF')  # 하드코딩 입력값 (파란색)
    font_green = Font(name=font_name, size=11, color='008000') # 시트 간 참조 수식 (녹색)
    font_bold_black = Font(name=font_name, size=11, bold=True, color='000000')
    font_bold_green = Font(name=font_name, size=11, bold=True, color='008000')
    
    # 채우기 스타일 (Fills)
    fill_title = PatternFill(start_color='1B365D', end_color='1B365D', fill_type='solid') # 네이비
    fill_header = PatternFill(start_color='4682B4', end_color='4682B4', fill_type='solid') # 스틸 블루
    fill_kpi = PatternFill(start_color='F0F4F8', end_color='F0F4F8', fill_type='solid') # 아주 연한 하늘색
    fill_accent = PatternFill(start_color='FFFFE0', end_color='FFFFE0', fill_type='solid') # 연한 노란색 (참조/주의)
    
    # 정렬 (Alignments)
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    align_title = Alignment(horizontal='center', vertical='center')
    
    # 테두리 (Borders)
    thin_side = Side(border_style="thin", color="CCCCCC")
    double_side = Side(border_style="double", color="1B365D")
    thick_bottom = Side(border_style="medium", color="1B365D")
    
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    border_header = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thick_bottom)
    border_total = Border(top=thin_side, bottom=double_side)
    border_kpi = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    
    # -------------------------------------------------------------
    # 4. Raw_Data 시트 작성 (원본 데이터 적재)
    # -------------------------------------------------------------
    headers_raw = ["제목", "저자", "출판사", "발행일", "정가", "판매가", "리뷰 수", "판매지수", "발행연도", "발행월", "할인율"]
    ws_raw.append(headers_raw)
    
    # 헤더 스타일
    for col_idx in range(1, len(headers_raw) + 1):
        cell = ws_raw.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = fill_title
        cell.alignment = align_center
        cell.border = border_header
        
    for i, row in df.iterrows():
        r_idx = i + 2
        discount_formula = f"=(E{r_idx}-F{r_idx})/IF(E{r_idx}>0,E{r_idx},1)"
        
        row_data = [
            row["제목"], row["저자"], row["출판사"], row["발행일"], 
            row["정가"], row["판매가"], row["리뷰 수"], row["판매지수"],
            row["발행연도"], row["발행월"], discount_formula
        ]
        ws_raw.append(row_data)
        
        # 스타일 서식 적용
        for c in range(1, 5): # 제목 ~ 발행일
            cell = ws_raw.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_left
            cell.border = border_all
            
        for c in [5, 6]: # 정가, 판매가
            cell = ws_raw.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_right
            cell.number_format = '₩#,##0;(\₩#,##0);"-"'
            cell.border = border_all
            
        for c in [7, 8]: # 리뷰수, 판매지수
            cell = ws_raw.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_right
            cell.number_format = '#,##0;(#,##0);"-"'
            cell.border = border_all
            
        for c in [9, 10]: # 연도, 월
            cell = ws_raw.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_center
            cell.border = border_all
            
        # 할인율 (수식)
        cell = ws_raw.cell(row=r_idx, column=11)
        cell.font = font_black
        cell.alignment = align_right
        cell.number_format = '0.0%'
        cell.border = border_all
        
    print("Raw_Data 시트 적재 완료.")
    
    # -------------------------------------------------------------
    # 5. Analysis_Data 시트 작성 (피벗 요약 데이터)
    # -------------------------------------------------------------
    # A. 연도별 요약
    headers_year = ["발행연도", "도서 수", "평균 정가", "평균 판매가", "평균 할인율", "판매지수 합계", "리뷰 수 합계"]
    for col_idx, h in enumerate(headers_year, start=1):
        cell = ws_analysis.cell(row=1, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_header
        
    for idx, year in enumerate(years):
        r = idx + 2
        cell_y = ws_analysis.cell(row=r, column=1, value=year)
        cell_y.font = font_blue
        cell_y.alignment = align_center
        cell_y.border = border_all
        
        ws_analysis.cell(row=r, column=2, value=f"=COUNTIF(Raw_Data!$I$2:$I$1201, A{r})").font = font_green
        ws_analysis.cell(row=r, column=2).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=2).border = border_all
        ws_analysis.cell(row=r, column=2).alignment = align_right
        
        ws_analysis.cell(row=r, column=3, value=f"=AVERAGEIF(Raw_Data!$I$2:$I$1201, A{r}, Raw_Data!$E$2:$E$1201)").font = font_green
        ws_analysis.cell(row=r, column=3).number_format = '₩#,##0;(\₩#,##0);"-"'
        ws_analysis.cell(row=r, column=3).border = border_all
        ws_analysis.cell(row=r, column=3).alignment = align_right
        
        ws_analysis.cell(row=r, column=4, value=f"=AVERAGEIF(Raw_Data!$I$2:$I$1201, A{r}, Raw_Data!$F$2:$F$1201)").font = font_green
        ws_analysis.cell(row=r, column=4).number_format = '₩#,##0;(\₩#,##0);"-"'
        ws_analysis.cell(row=r, column=4).border = border_all
        ws_analysis.cell(row=r, column=4).alignment = align_right
        
        ws_analysis.cell(row=r, column=5, value=f"=AVERAGEIF(Raw_Data!$I$2:$I$1201, A{r}, Raw_Data!$K$2:$K$1201)").font = font_green
        ws_analysis.cell(row=r, column=5).number_format = '0.0%'
        ws_analysis.cell(row=r, column=5).border = border_all
        ws_analysis.cell(row=r, column=5).alignment = align_right
        
        ws_analysis.cell(row=r, column=6, value=f"=SUMIF(Raw_Data!$I$2:$I$1201, A{r}, Raw_Data!$H$2:$H$1201)").font = font_green
        ws_analysis.cell(row=r, column=6).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=6).border = border_all
        ws_analysis.cell(row=r, column=6).alignment = align_right
        
        ws_analysis.cell(row=r, column=7, value=f"=SUMIF(Raw_Data!$I$2:$I$1201, A{r}, Raw_Data!$G$2:$G$1201)").font = font_green
        ws_analysis.cell(row=r, column=7).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=7).border = border_all
        ws_analysis.cell(row=r, column=7).alignment = align_right
        
    tot_row_y = len(years) + 2
    ws_analysis.cell(row=tot_row_y, column=1, value="합계").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=1).alignment = align_center
    ws_analysis.cell(row=tot_row_y, column=1).border = border_total
    
    ws_analysis.cell(row=tot_row_y, column=2, value=f"=SUM(B2:B{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=2).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_y, column=2).border = border_total
    ws_analysis.cell(row=tot_row_y, column=2).alignment = align_right
    
    ws_analysis.cell(row=tot_row_y, column=3, value=f"=AVERAGE(C2:C{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=3).number_format = '₩#,##0;(\₩#,##0);"-"'
    ws_analysis.cell(row=tot_row_y, column=3).border = border_total
    ws_analysis.cell(row=tot_row_y, column=3).alignment = align_right
    
    ws_analysis.cell(row=tot_row_y, column=4, value=f"=AVERAGE(D2:D{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=4).number_format = '₩#,##0;(\₩#,##0);"-"'
    ws_analysis.cell(row=tot_row_y, column=4).border = border_total
    ws_analysis.cell(row=tot_row_y, column=4).alignment = align_right
    
    ws_analysis.cell(row=tot_row_y, column=5, value=f"=AVERAGE(E2:E{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=5).number_format = '0.0%'
    ws_analysis.cell(row=tot_row_y, column=5).border = border_total
    ws_analysis.cell(row=tot_row_y, column=5).alignment = align_right
    
    ws_analysis.cell(row=tot_row_y, column=6, value=f"=SUM(F2:F{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=6).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_y, column=6).border = border_total
    ws_analysis.cell(row=tot_row_y, column=6).alignment = align_right
    
    ws_analysis.cell(row=tot_row_y, column=7, value=f"=SUM(G2:G{tot_row_y-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_y, column=7).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_y, column=7).border = border_total
    ws_analysis.cell(row=tot_row_y, column=7).alignment = align_right

    # B. 출판사별 요약 (I열 ~ O열)
    headers_pub = ["출판사", "도서 수", "평균 정가", "평균 판매가", "평균 할인율", "판매지수 합계", "리뷰 수 합계"]
    for col_idx, h in enumerate(headers_pub, start=9):
        cell = ws_analysis.cell(row=1, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_header
        
    for idx, pub in enumerate(top_publishers):
        r = idx + 2
        cell_p = ws_analysis.cell(row=r, column=9, value=pub)
        cell_p.font = font_blue
        cell_p.alignment = align_left
        cell_p.border = border_all
        
        ws_analysis.cell(row=r, column=10, value=f"=COUNTIF(Raw_Data!$C$2:$C$1201, I{r})").font = font_green
        ws_analysis.cell(row=r, column=10).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=10).border = border_all
        ws_analysis.cell(row=r, column=10).alignment = align_right
        
        ws_analysis.cell(row=r, column=11, value=f"=AVERAGEIF(Raw_Data!$C$2:$C$1201, I{r}, Raw_Data!$E$2:$E$1201)").font = font_green
        ws_analysis.cell(row=r, column=11).number_format = '₩#,##0;(\₩#,##0);"-"'
        ws_analysis.cell(row=r, column=11).border = border_all
        ws_analysis.cell(row=r, column=11).alignment = align_right
        
        ws_analysis.cell(row=r, column=12, value=f"=AVERAGEIF(Raw_Data!$C$2:$C$1201, I{r}, Raw_Data!$F$2:$F$1201)").font = font_green
        ws_analysis.cell(row=r, column=12).number_format = '₩#,##0;(\₩#,##0);"-"'
        ws_analysis.cell(row=r, column=12).border = border_all
        ws_analysis.cell(row=r, column=12).alignment = align_right
        
        ws_analysis.cell(row=r, column=13, value=f"=AVERAGEIF(Raw_Data!$C$2:$C$1201, I{r}, Raw_Data!$K$2:$K$1201)").font = font_green
        ws_analysis.cell(row=r, column=13).number_format = '0.0%'
        ws_analysis.cell(row=r, column=13).border = border_all
        ws_analysis.cell(row=r, column=13).alignment = align_right
        
        ws_analysis.cell(row=r, column=14, value=f"=SUMIF(Raw_Data!$C$2:$C$1201, I{r}, Raw_Data!$H$2:$H$1201)").font = font_green
        ws_analysis.cell(row=r, column=14).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=14).border = border_all
        ws_analysis.cell(row=r, column=14).alignment = align_right
        
        ws_analysis.cell(row=r, column=15, value=f"=SUMIF(Raw_Data!$C$2:$C$1201, I{r}, Raw_Data!$G$2:$G$1201)").font = font_green
        ws_analysis.cell(row=r, column=15).number_format = '#,##0;(#,##0);"-"'
        ws_analysis.cell(row=r, column=15).border = border_all
        ws_analysis.cell(row=r, column=15).alignment = align_right
        
    tot_row_p = len(top_publishers) + 2
    ws_analysis.cell(row=tot_row_p, column=9, value="합계").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=9).alignment = align_center
    ws_analysis.cell(row=tot_row_p, column=9).border = border_total
    
    ws_analysis.cell(row=tot_row_p, column=10, value=f"=SUM(J2:J{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=10).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_p, column=10).border = border_total
    ws_analysis.cell(row=tot_row_p, column=10).alignment = align_right
    
    ws_analysis.cell(row=tot_row_p, column=11, value=f"=AVERAGE(K2:K{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=11).number_format = '₩#,##0;(\₩#,##0);"-"'
    ws_analysis.cell(row=tot_row_p, column=11).border = border_total
    ws_analysis.cell(row=tot_row_p, column=11).alignment = align_right
    
    ws_analysis.cell(row=tot_row_p, column=12, value=f"=AVERAGE(L2:L{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=12).number_format = '₩#,##0;(\₩#,##0);"-"'
    ws_analysis.cell(row=tot_row_p, column=12).border = border_total
    ws_analysis.cell(row=tot_row_p, column=12).alignment = align_right
    
    ws_analysis.cell(row=tot_row_p, column=13, value=f"=AVERAGE(M2:M{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=13).number_format = '0.0%'
    ws_analysis.cell(row=tot_row_p, column=13).border = border_total
    ws_analysis.cell(row=tot_row_p, column=13).alignment = align_right
    
    ws_analysis.cell(row=tot_row_p, column=14, value=f"=SUM(N2:N{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=14).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_p, column=14).border = border_total
    ws_analysis.cell(row=tot_row_p, column=14).alignment = align_right
    
    ws_analysis.cell(row=tot_row_p, column=15, value=f"=SUM(O2:O{tot_row_p-1})").font = font_bold_black
    ws_analysis.cell(row=tot_row_p, column=15).number_format = '#,##0;(#,##0);"-"'
    ws_analysis.cell(row=tot_row_p, column=15).border = border_total
    ws_analysis.cell(row=tot_row_p, column=15).alignment = align_right

    print("Analysis_Data 시트 요약 완료.")
    
    # -------------------------------------------------------------
    # 6. Dashboard 시트 작성
    # -------------------------------------------------------------
    ws_dash.merge_cells("A1:O1")
    title_cell = ws_dash["A1"]
    title_cell.value = "YES24 도서 데이터 요약 대시보드"
    title_cell.font = font_title
    title_cell.fill = fill_title
    title_cell.alignment = align_title
    ws_dash.row_dimensions[1].height = 40
    
    # KPI 요약 카드 (A3:J4)
    kpis = [
        ("총 도서 등록 수", "=COUNT(Raw_Data!A2:A1201)", '#,##0" 권"', "A", "B"),
        ("평균 도서 판매가", "=AVERAGE(Raw_Data!F2:F1201)", '₩#,##0', "C", "D"),
        ("평균 도서 할인율", "=AVERAGE(Raw_Data!K2:K1201)", '0.0%', "E", "F"),
        ("도서 누적 판매지수", "=SUM(Raw_Data!H2:H1201)", '#,##0', "G", "H"),
        ("도서 누적 리뷰 수", "=SUM(Raw_Data!G2:G1201)", '#,##0" 건"', "I", "J")
    ]
    for label, val, num_fmt, start_col, end_col in kpis:
        c1 = f"{start_col}3"
        c2 = f"{end_col}3"
        c3 = f"{start_col}4"
        c4 = f"{end_col}4"
        ws_dash.merge_cells(f"{c1}:{c2}")
        ws_dash.merge_cells(f"{c3}:{c4}")
        
        ws_dash[c1] = label
        ws_dash[c1].font = font_kpi_title
        ws_dash[c1].fill = fill_kpi
        ws_dash[c1].alignment = align_center
        
        ws_dash[c3] = val
        ws_dash[c3].font = font_kpi_value
        ws_dash[c3].fill = fill_kpi
        ws_dash[c3].alignment = align_center
        ws_dash[c3].number_format = num_fmt
        
    for r in [3, 4]:
        for c in range(1, 11):
            ws_dash.cell(row=r, column=c).border = border_kpi
            
    ws_dash.merge_cells("K3:O4")
    note_cell = ws_dash["K3"]
    note_cell.value = "※ 참고 사항:\n본 대시보드는 실시간 수식 연동형으로 구성되었습니다.\n수식 결과는 검은색, 타 시트 참조 수식은 녹색,\n수동 하드코딩 입력값은 파란색으로 표시되어 있습니다."
    note_cell.font = Font(name=font_name, size=9, color='555555')
    note_cell.fill = fill_accent
    note_cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    for r in [3, 4]:
        for c in range(11, 16):
            ws_dash.cell(row=r, column=c).border = border_kpi

    ws_dash.cell(row=6, column=1, value="■ 주요 출판사별 요약 테이블 (Top 15)").font = font_section
    ws_dash.cell(row=6, column=9, value="■ 연도별 도서 발행 추이 요약 테이블").font = font_section
    
    # 출판사 테이블 연동 (A7 ~ G23)
    for col_idx, h in enumerate(headers_pub, start=1):
        cell = ws_dash.cell(row=7, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_header
        
    for idx, pub in enumerate(top_publishers):
        r = idx + 8
        ar = idx + 2
        ws_dash.cell(row=r, column=1, value=f"=Analysis_Data!I{ar}").font = font_green
        ws_dash.cell(row=r, column=1).alignment = align_left
        ws_dash.cell(row=r, column=1).border = border_all
        
        for c_idx, fmt in [(2, '#,##0;(#,##0);"-"'), (3, '₩#,##0;(\₩#,##0);"-"'), (4, '₩#,##0;(\₩#,##0);"-"'), (5, '0.0%'), (6, '#,##0;(#,##0);"-"'), (7, '#,##0;(#,##0);"-"')]:
            col_let = get_column_letter(c_idx + 8) # Analysis_Data에서는 I(9)열부터 시작하므로 c_idx(2)에 +8 필요
            cell = ws_dash.cell(row=r, column=c_idx, value=f"=Analysis_Data!{col_let}{ar}")
            cell.font = font_green
            cell.alignment = align_right
            cell.number_format = fmt
            cell.border = border_all
            
    ws_dash.cell(row=23, column=1, value="합계").font = font_bold_green
    ws_dash.cell(row=23, column=1).alignment = align_center
    ws_dash.cell(row=23, column=1).border = border_total
    
    ar_total = len(top_publishers) + 2
    for c_idx, fmt in [(2, '#,##0;(#,##0);"-"'), (3, '₩#,##0;(\₩#,##0);"-"'), (4, '₩#,##0;(\₩#,##0);"-"'), (5, '0.0%'), (6, '#,##0;(#,##0);"-"'), (7, '#,##0;(#,##0);"-"')]:
        col_let = get_column_letter(c_idx + 8) # Analysis_Data에서는 I(9)열부터 시작하므로 c_idx(2)에 +8 필요
        cell = ws_dash.cell(row=23, column=c_idx, value=f"=Analysis_Data!{col_let}{ar_total}")
        cell.font = font_bold_green
        cell.alignment = align_right
        cell.number_format = fmt
        cell.border = border_total

    # 연도별 테이블 연동 (I7 ~ O22)
    for col_idx, h in enumerate(headers_year, start=9):
        cell = ws_dash.cell(row=7, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_header
        
    for idx, year in enumerate(years):
        r = idx + 8
        ar = idx + 2
        ws_dash.cell(row=r, column=9, value=f"=Analysis_Data!A{ar}").font = font_green
        ws_dash.cell(row=r, column=9).alignment = align_center
        ws_dash.cell(row=r, column=9).border = border_all
        
        for c_idx, fmt in [(10, '#,##0;(#,##0);"-"'), (11, '₩#,##0;(\₩#,##0);"-"'), (12, '₩#,##0;(\₩#,##0);"-"'), (13, '0.0%'), (14, '#,##0;(#,##0);"-"'), (15, '#,##0;(#,##0);"-"')]:
            src_col = get_column_letter(c_idx - 8) # A, B, C, D, E, F, G
            cell = ws_dash.cell(row=r, column=c_idx, value=f"=Analysis_Data!{src_col}{ar}")
            cell.font = font_green
            cell.alignment = align_right
            cell.number_format = fmt
            cell.border = border_all
            
    tot_row_dash_y = len(years) + 8
    ws_dash.cell(row=tot_row_dash_y, column=9, value="합계").font = font_bold_green
    ws_dash.cell(row=tot_row_dash_y, column=9).alignment = align_center
    ws_dash.cell(row=tot_row_dash_y, column=9).border = border_total
    
    ar_total_y = len(years) + 2
    for c_idx, fmt in [(10, '#,##0;(#,##0);"-"'), (11, '₩#,##0;(\₩#,##0);"-"'), (12, '₩#,##0;(\₩#,##0);"-"'), (13, '0.0%'), (14, '#,##0;(#,##0);"-"'), (15, '#,##0;(#,##0);"-"')]:
        src_col = get_column_letter(c_idx - 8)
        cell = ws_dash.cell(row=tot_row_dash_y, column=c_idx, value=f"=Analysis_Data!{src_col}{ar_total_y}")
        cell.font = font_bold_green
        cell.alignment = align_right
        cell.number_format = fmt
        cell.border = border_total

    # -------------------------------------------------------------
    # 7. 엑셀 차트 추가
    # -------------------------------------------------------------
    chart_pub = BarChart()
    chart_pub.type = "col"
    chart_pub.style = 10
    chart_pub.title = "주요 출판사별 도서 발행 건수"
    chart_pub.y_axis.title = "도서 수 (권)"
    chart_pub.x_axis.title = "출판사"
    
    data_pub = Reference(ws_analysis, min_col=10, min_row=1, max_row=16)
    cats_pub = Reference(ws_analysis, min_col=9, min_row=2, max_row=16)
    chart_pub.add_data(data_pub, titles_from_data=True)
    chart_pub.set_categories(cats_pub)
    chart_pub.width = 16
    chart_pub.height = 10
    ws_dash.add_chart(chart_pub, "A25")
    
    chart_year = BarChart()
    chart_year.type = "col"
    chart_year.style = 11
    chart_year.title = "연도별 도서 발행 건수 추이"
    chart_year.y_axis.title = "도서 수 (권)"
    chart_year.x_axis.title = "발행연도"
    
    data_year = Reference(ws_analysis, min_col=2, min_row=1, max_row=len(years)+1)
    cats_year = Reference(ws_analysis, min_col=1, min_row=2, max_row=len(years)+1)
    chart_year.add_data(data_year, titles_from_data=True)
    chart_year.set_categories(cats_year)
    chart_year.width = 16
    chart_year.height = 10
    ws_dash.add_chart(chart_year, "I25")

    # -------------------------------------------------------------
    # 8. [신규 요구사항] 출판사별 도서 목록 시트 분리 생성
    # -------------------------------------------------------------
    # 상위 7개 출판사 시트 생성 및 데이터 적재
    for pub_name in top_7_publishers:
        # 시트명 생성 (공백 제거 등 안전성 확보)
        ws_pub = wb.create_sheet(pub_name)
        
        # 헤더 추가
        ws_pub.append(headers_raw)
        for col_idx in range(1, len(headers_raw) + 1):
            cell = ws_pub.cell(row=1, column=col_idx)
            cell.font = font_header
            cell.fill = fill_title
            cell.alignment = align_center
            cell.border = border_header
            
        # 해당 출판사 데이터 필터링
        pub_df = df[df['출판사'] == pub_name].reset_index(drop=True)
        
        # 데이터 기입
        for i, row in pub_df.iterrows():
            r_idx = i + 2
            # 할인율 수식
            discount_formula = f"=(E{r_idx}-F{r_idx})/IF(E{r_idx}>0,E{r_idx},1)"
            
            row_data = [
                row["제목"], row["저자"], row["출판사"], row["발행일"], 
                row["정가"], row["판매가"], row["리뷰 수"], row["판매지수"],
                row["발행연도"], row["발행월"], discount_formula
            ]
            ws_pub.append(row_data)
            
            # 서식 스타일 적용
            for c in range(1, 5):
                ws_pub.cell(row=r_idx, column=c).font = font_blue
                ws_pub.cell(row=r_idx, column=c).alignment = align_left
                ws_pub.cell(row=r_idx, column=c).border = border_all
                
            for c in [5, 6]:
                cell = ws_pub.cell(row=r_idx, column=c)
                cell.font = font_blue
                cell.alignment = align_right
                cell.number_format = '₩#,##0;(\₩#,##0);"-"'
                cell.border = border_all
                
            for c in [7, 8]:
                cell = ws_pub.cell(row=r_idx, column=c)
                cell.font = font_blue
                cell.alignment = align_right
                cell.number_format = '#,##0;(#,##0);"-"'
                cell.border = border_all
                
            for c in [9, 10]:
                ws_pub.cell(row=r_idx, column=c).font = font_blue
                ws_pub.cell(row=r_idx, column=c).alignment = align_center
                ws_pub.cell(row=r_idx, column=c).border = border_all
                
            # 할인율 수식
            cell = ws_pub.cell(row=r_idx, column=11)
            cell.font = font_black
            cell.alignment = align_right
            cell.number_format = '0.0%'
            cell.border = border_all
            
        # 하단 요약 합계 행 기입
        tot_r = len(pub_df) + 2
        ws_pub.cell(row=tot_r, column=1, value="합계 및 평균 요약").font = font_bold_black
        ws_pub.cell(row=tot_r, column=1).alignment = align_center
        ws_pub.cell(row=tot_r, column=1).border = border_total
        
        # 합계에 해당 안 되는 텍스트 열은 테두리만 두름
        for c in range(2, 5):
            ws_pub.cell(row=tot_r, column=c).border = border_total
            
        # 평균 정가
        c_avg_p = ws_pub.cell(row=tot_r, column=5, value=f"=AVERAGE(E2:E{tot_r-1})")
        c_avg_p.font = font_bold_black
        c_avg_p.alignment = align_right
        c_avg_p.number_format = '₩#,##0;(\₩#,##0);"-"'
        c_avg_p.border = border_total
        
        # 평균 판매가
        c_avg_s = ws_pub.cell(row=tot_r, column=6, value=f"=AVERAGE(F2:F{tot_r-1})")
        c_avg_s.font = font_bold_black
        c_avg_s.alignment = align_right
        c_avg_s.number_format = '₩#,##0;(\₩#,##0);"-"'
        c_avg_s.border = border_total
        
        # 총 리뷰 수 합계
        c_sum_rev = ws_pub.cell(row=tot_r, column=7, value=f"=SUM(G2:G{tot_r-1})")
        c_sum_rev.font = font_bold_black
        c_sum_rev.alignment = align_right
        c_sum_rev.number_format = '#,##0;(#,##0);"-"'
        c_sum_rev.border = border_total
        
        # 총 판매지수 합계
        c_sum_sales = ws_pub.cell(row=tot_r, column=8, value=f"=SUM(H2:H{tot_r-1})")
        c_sum_sales.font = font_bold_black
        c_sum_sales.alignment = align_right
        c_sum_sales.number_format = '#,##0;(#,##0);"-"'
        c_sum_sales.border = border_total
        
        # 발행연도, 발행월은 테두리만 두름
        for c in [9, 10]:
            ws_pub.cell(row=tot_r, column=c).border = border_total
            
        # 평균 할인율
        c_avg_d = ws_pub.cell(row=tot_r, column=11, value=f"=AVERAGE(K2:K{tot_r-1})")
        c_avg_d.font = font_bold_black
        c_avg_d.alignment = align_right
        c_avg_d.number_format = '0.0%'
        c_avg_d.border = border_total
        
        print(f"출판사 시트 생성 완료: {pub_name} ({len(pub_df)}권)")
        
    # 나머지 출판사 통합 시트 생성 및 적재 ("기타_출판사")
    other_pub_sheet_name = "기타_출판사"
    ws_other = wb.create_sheet(other_pub_sheet_name)
    
    # 헤더 추가
    ws_other.append(headers_raw)
    for col_idx in range(1, len(headers_raw) + 1):
        cell = ws_other.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = fill_title
        cell.alignment = align_center
        cell.border = border_header
        
    # 상위 7개 출판사 제외 필터링
    other_df = df[~df['출판사'].isin(top_7_publishers)].reset_index(drop=True)
    
    # 데이터 기입
    for i, row in other_df.iterrows():
        r_idx = i + 2
        discount_formula = f"=(E{r_idx}-F{r_idx})/IF(E{r_idx}>0,E{r_idx},1)"
        
        row_data = [
            row["제목"], row["저자"], row["출판사"], row["발행일"], 
            row["정가"], row["판매가"], row["리뷰 수"], row["판매지수"],
            row["발행연도"], row["발행월"], discount_formula
        ]
        ws_other.append(row_data)
        
        # 서식 스타일 적용
        for c in range(1, 5):
            ws_other.cell(row=r_idx, column=c).font = font_blue
            ws_other.cell(row=r_idx, column=c).alignment = align_left
            ws_other.cell(row=r_idx, column=c).border = border_all
            
        for c in [5, 6]:
            cell = ws_other.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_right
            cell.number_format = '₩#,##0;(\₩#,##0);"-"'
            cell.border = border_all
            
        for c in [7, 8]:
            cell = ws_other.cell(row=r_idx, column=c)
            cell.font = font_blue
            cell.alignment = align_right
            cell.number_format = '#,##0;(#,##0);"-"'
            cell.border = border_all
            
        for c in [9, 10]:
            ws_other.cell(row=r_idx, column=c).font = font_blue
            ws_other.cell(row=r_idx, column=c).alignment = align_center
            ws_other.cell(row=r_idx, column=c).border = border_all
            
        # 할인율
        cell = ws_other.cell(row=r_idx, column=11)
        cell.font = font_black
        cell.alignment = align_right
        cell.number_format = '0.0%'
        cell.border = border_all
        
    # 하단 요약 합계 행 기입 (기타_출판사)
    tot_r_other = len(other_df) + 2
    ws_other.cell(row=tot_r_other, column=1, value="합계 및 평균 요약").font = font_bold_black
    ws_other.cell(row=tot_r_other, column=1).alignment = align_center
    ws_other.cell(row=tot_r_other, column=1).border = border_total
    
    for c in range(2, 5):
        ws_other.cell(row=tot_r_other, column=c).border = border_total
        
    c_avg_p = ws_other.cell(row=tot_r_other, column=5, value=f"=AVERAGE(E2:E{tot_r_other-1})")
    c_avg_p.font = font_bold_black
    c_avg_p.alignment = align_right
    c_avg_p.number_format = '₩#,##0;(\₩#,##0);"-"'
    c_avg_p.border = border_total
    
    c_avg_s = ws_other.cell(row=tot_r_other, column=6, value=f"=AVERAGE(F2:F{tot_r_other-1})")
    c_avg_s.font = font_bold_black
    c_avg_s.alignment = align_right
    c_avg_s.number_format = '₩#,##0;(\₩#,##0);"-"'
    c_avg_s.border = border_total
    
    c_sum_rev = ws_other.cell(row=tot_r_other, column=7, value=f"=SUM(G2:G{tot_r_other-1})")
    c_sum_rev.font = font_bold_black
    c_sum_rev.alignment = align_right
    c_sum_rev.number_format = '#,##0;(#,##0);"-"'
    c_sum_rev.border = border_total
    
    c_sum_sales = ws_other.cell(row=tot_r_other, column=8, value=f"=SUM(H2:H{tot_r_other-1})")
    c_sum_sales.font = font_bold_black
    c_sum_sales.alignment = align_right
    c_sum_sales.number_format = '#,##0;(#,##0);"-"'
    c_sum_sales.border = border_total
    
    for c in [9, 10]:
        ws_other.cell(row=tot_r_other, column=c).border = border_total
        
    c_avg_d = ws_other.cell(row=tot_r_other, column=11, value=f"=AVERAGE(K2:K{tot_r_other-1})")
    c_avg_d.font = font_bold_black
    c_avg_d.alignment = align_right
    c_avg_d.number_format = '0.0%'
    c_avg_d.border = border_total
    
    print(f"기타 출판사 통합 시트 생성 완료: {other_pub_sheet_name} ({len(other_df)}권)")

    # -------------------------------------------------------------
    # 9. 모든 시트의 컬럼 너비 조정 (가독성 향상)
    # -------------------------------------------------------------
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            
            # 셀 내 최대 텍스트 길이 측정
            for cell in col:
                val = str(cell.value or '')
                h_len = sum(2 if ord(char) > 128 else 1 for char in val)
                if h_len > max_len:
                    max_len = h_len
            
            ws.column_dimensions[col_letter].width = max(min(max_len + 3, 50), 10)
            
    # Dashboard 시트의 컬럼 너비는 고정 폭으로 보기 좋게 조정
    ws_dash.column_dimensions['A'].width = 24
    ws_dash.column_dimensions['I'].width = 15
    
    # 10. 파일 저장
    wb.save(output_path)
    print(f"엑셀 대시보드 및 출판사별 시트가 생성 완료되었습니다: {output_path}")

if __name__ == '__main__':
    csv_path = 'yes24/data/yes24_books.csv'
    output_path = 'yes24/yes24_dashboard.xlsx'
    create_excel_dashboard(csv_path, output_path)
