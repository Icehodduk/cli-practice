# -*- coding: utf-8 -*-
"""
프로젝트 결과물에 대한 자가 검증(Self-Verification) 수행 스크립트입니다.
작성일: 2026-07-15
"""

import os
import openpyxl
import re

def verify_files():
    print("=== 1. 산출물 파일 존재 여부 검증 ===")
    required_files = [
        "yes24/data/yes24_books.csv",
        "yes24/yes24_dashboard.xlsx",
        "yes24/docs/implementation_plan.md",
        "yes24/docs/eda_report.md",
        "yes24/docs/eda_report_presentation.md",
        "yes24/src/run_eda.py",
        "yes24/src/create_dashboard.py"
    ]
    
    all_exist = True
    for f in required_files:
        if os.path.exists(f):
            print(f"  [OK] {f} 파일이 존재합니다.")
        else:
            print(f"  [ERROR] {f} 파일이 누락되었습니다.")
            all_exist = False
    return all_exist

def verify_images():
    print("\n=== 2. EDA 시각화 이미지 검증 ===")
    img_dir = "yes24/images"
    if not os.path.exists(img_dir):
        print("  [ERROR] 이미지 디렉터리가 존재하지 않습니다.")
        return False
        
    required_imgs = [
        "01_price_distribution.png",
        "02_discount_rate_distribution.png",
        "03_sales_index_distribution.png",
        "04_review_count_distribution.png",
        "05_yearly_publish_trend.png",
        "06_price_vs_sales_index.png",
        "07_sales_index_vs_reviews.png",
        "08_top_publishers.png",
        "09_top_authors.png",
        "10_text_keywords.png"
    ]
    
    all_imgs = True
    for img in required_imgs:
        img_path = os.path.join(img_dir, img)
        if os.path.exists(img_path):
            print(f"  [OK] 시각화 이미지 존재: {img}")
        else:
            print(f"  [ERROR] 시각화 이미지 누락: {img}")
            all_imgs = False
            
    # 이미지 총 개수가 10개 이상인지 확인
    img_count = len([f for f in os.listdir(img_dir) if f.endswith('.png')])
    print(f"  -> 총 이미지 개수: {img_count}개 (기준: 10개 이상)")
    if img_count < 10:
        print("  [ERROR] 시각화 이미지가 10개 미만입니다.")
        all_imgs = False
        
    return all_imgs

def verify_excel_formulas():
    print("\n=== 3. 엑셀 대시보드 수식 및 서식 검증 ===")
    xlsx_path = "yes24/yes24_dashboard.xlsx"
    if not os.path.exists(xlsx_path):
        return False
        
    wb = openpyxl.load_workbook(xlsx_path, data_only=False)
    
    # 시트 존재 검증 (요구사항 추가 반영)
    expected_sheets = [
        "Dashboard", "Analysis_Data", "Raw_Data",
        "커뮤니케이션북스", "한빛미디어", "길벗", "제이펍", "골든래빗", "앤써북", "위키북스", "기타_출판사"
    ]
    for sheet in expected_sheets:
        if sheet in wb.sheetnames:
            print(f"  [OK] 시트 존재: {sheet}")
        else:
            print(f"  [ERROR] 시트 누락: {sheet}")
            
    # 수식 구문 검사
    ws_dash = wb["Dashboard"]
    ws_analysis = wb["Analysis_Data"]
    
    errors_found = False
    
    # Dashboard 시트의 수식 확인
    kpi_cells = ["A4", "C4", "E4", "G4", "I4"]
    print("  -> 대시보드 KPI 셀 수식 검증:")
    for cell_addr in kpi_cells:
        val = ws_dash[cell_addr].value
        print(f"     Cell {cell_addr}: {val}")
        if not str(val).startswith("="):
            print(f"     [WARNING] KPI 셀 {cell_addr}에 수식이 적용되어 있지 않습니다.")
            errors_found = True
            
    # 요약 테이블 수식 확인
    print("  -> 대시보드 테이블 연동 수식 확인 (샘플):")
    samples = [("A8", "=Analysis_Data!I2"), ("B8", "=Analysis_Data!J2"), ("I8", "=Analysis_Data!A2")]
    for cell_addr, expected in samples:
        val = ws_dash[cell_addr].value
        print(f"     Cell {cell_addr}: {val} (예상: {expected})")
        if val != expected:
            print(f"     [WARNING] 셀 {cell_addr} 수식이 예상과 다릅니다.")
            errors_found = True
            
    # 분리된 출판사별 시트 하단 수식 검증
    print("  -> 개별 출판사 시트 요약 수식 검증:")
    pub_sheets = ["커뮤니케이션북스", "한빛미디어", "길벗", "제이펍", "골든래빗", "앤써북", "위키북스", "기타_출판사"]
    for p_sheet in pub_sheets:
        ws_p = wb[p_sheet]
        last_row = ws_p.max_row
        val_avg_p = ws_p.cell(row=last_row, column=5).value # 평균정가
        val_avg_s = ws_p.cell(row=last_row, column=6).value # 평균판매가
        val_sum_r = ws_p.cell(row=last_row, column=7).value # 총리뷰수
        
        print(f"     시트 {p_sheet} (마지막행: {last_row}):")
        print(f"       정가 평균 수식: {val_avg_p}")
        print(f"       판매가 평균 수식: {val_avg_s}")
        print(f"       리뷰수 합계 수식: {val_sum_r}")
        
        if not (str(val_avg_p).startswith("=AVERAGE") and str(val_sum_r).startswith("=SUM")):
            print(f"     [WARNING] 시트 {p_sheet}의 하단 요약 셀에 공식이 올바르게 등록되지 않았습니다.")
            errors_found = True
            
    # 수식 괄호 짝 검증
    for ws_name in wb.sheetnames:
        ws = wb[ws_name]
        for row in ws.iter_rows(values_only=False):
            for cell in row:
                val = cell.value
                if isinstance(val, str) and val.startswith("="):
                    # 괄호 짝 확인
                    open_p = val.count("(")
                    close_p = val.count(")")
                    if open_p != close_p:
                        print(f"  [ERROR] {ws_name}!{cell.coordinate} 수식의 괄호 개수 불일치: {val}")
                        errors_found = True
                        
    if not errors_found:
        print("  [OK] 수식 구문 검증 완료 (에러 및 괄호 불일치 없음)")
    return not errors_found

def verify_report_content():
    print("\n=== 4. 마크다운 리포트 형식 검증 ===")
    report_path = "yes24/docs/eda_report.md"
    if not os.path.exists(report_path):
        return False
        
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    ok = True
    for i in range(1, 11):
        num_str = f"{i:02d}"
        if num_str not in content:
            print(f"  [ERROR] 리포트 내 {num_str}번 시각화 관련 언급 누락")
            ok = False
            
    if "../images/" in content:
        print("  [OK] 리포트 내 이미지 경로가 상대경로로 올바르게 치환되었습니다.")
    else:
        print("  [WARNING] 리포트 내 이미지 경로가 상대경로로 치환되지 않았습니다.")
        ok = False
        
    if ok:
        print("  [OK] 마크다운 리포트 형식 및 필수 구성요소 검증 완료")
    return ok

def verify_presentation():
    print("\n=== 5. Marp 프레젠테이션 검증 ===")
    pres_path = "yes24/docs/eda_report_presentation.md"
    if not os.path.exists(pres_path):
        print("  [ERROR] 프레젠테이션 파일이 존재하지 않습니다.")
        return False
        
    with open(pres_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # --- 개수 세기 (슬라이드 분량 검증)
    dash_count = len(re.findall(r"^---$", content, re.MULTILINE))
    slide_count = dash_count
    
    print(f"  -> 검출된 슬라이드 구분 기호(---) 수: {dash_count}개")
    print(f"  -> 추정 슬라이드 분량: {slide_count}장")
    
    ok = True
    if slide_count < 30:
        print(f"  [ERROR] 슬라이드 장수가 {slide_count}장으로 30장 미만입니다.")
        ok = False
    else:
        print(f"  [OK] 슬라이드 장수 요건 충족 ({slide_count}장 >= 30장)")
        
    # 이미지 상대경로 검증
    if "../images/" in content:
        print("  [OK] 프레젠테이션 이미지 경로가 상대경로로 올바르게 치환되었습니다.")
    else:
        print("  [WARNING] 프레젠테이션 이미지 경로가 상대경로로 치환되지 않았습니다.")
        ok = False
        
    return ok

if __name__ == "__main__":
    v1 = verify_files()
    v2 = verify_images()
    v3 = verify_excel_formulas()
    v4 = verify_report_content()
    v5 = verify_presentation()
    
    print("\n=== 최종 자가 검증 결과 ===")
    if v1 and v2 and v3 and v4 and v5:
        print("★ [PASS] 모든 검증 기준을 완벽하게 충족했습니다.")
    else:
        print("☆ [FAIL] 일부 검증 기준에 실패했습니다. 코드를 확인하십시오.")
