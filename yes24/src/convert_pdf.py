import os
import markdown
import asyncio
from playwright.async_api import async_playwright

async def md_to_pdf():
    base_dir = "yes24"
    md_path = os.path.join(base_dir, "docs", "eda_report.md")
    html_path = os.path.join(base_dir, "docs", "eda_report.html")
    pdf_path = os.path.join(base_dir, "docs", "eda_report.pdf")
    
    # 1. 마크다운 파일 읽기
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    # 2. HTML 변환 (테이블 및 펜스 코드블록 등 활성화)
    html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    
    # 3. HTML 래퍼 및 스타일시트 추가
    style = """
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, "Malgun Gothic", sans-serif;
        font-size: 13px;
        line-height: 1.6;
        color: #24292e;
        background-color: #ffffff;
        padding: 40px;
        max-width: 850px;
        margin: 0 auto;
    }
    h1, h2, h3, h4, h5, h6 {
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
        border-bottom: 1px solid #eaecef;
        padding-bottom: 0.3em;
        color: #1a1a1a;
    }
    h1 { font-size: 1.8em; }
    h2 { font-size: 1.4em; }
    h3 { font-size: 1.2em; }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 15px;
        margin-bottom: 20px;
        font-size: 11px;
    }
    table th, table td {
        padding: 8px 12px;
        border: 1px solid #dfe2e5;
        text-align: left;
    }
    table th {
        background-color: #f6f8fa;
        font-weight: bold;
    }
    table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    img {
        max-width: 90%;
        display: block;
        margin: 25px auto;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        page-break-inside: avoid;
    }
    pre, code {
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 85%;
        background-color: #f6f8fa;
        border-radius: 3px;
        padding: 0.2em 0.4em;
    }
    pre {
        padding: 16px;
        overflow: auto;
        line-height: 1.45;
        border-radius: 4px;
        border: 1px solid #e1e4e8;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    hr {
        height: 0.25em;
        padding: 0;
        margin: 24px 0;
        background-color: #e1e4e8;
        border: 0;
    }
    </style>
    """
    
    full_html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>YES24 도서 EDA 보고서</title>
        {style}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("HTML 파일 임시 저장 완료:", html_path)
    
    # 4. 플레이라이트를 이용한 PDF 변환
    abs_html_path = os.path.abspath(html_path)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 파일 경로 이동
        await page.goto(f"file://{abs_html_path}")
        # 이미지 로딩 완료 대기
        await page.wait_for_timeout(2000)
        
        # PDF 출력
        await page.pdf(
            path=pdf_path,
            format="A4",
            margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
            display_header_footer=True,
            header_template='<div style="font-size: 8px; width: 100%; text-align: right; margin-right: 20px; color: #999;">YES24 도서 EDA 보고서</div>',
            footer_template='<div style="font-size: 8px; width: 100%; text-align: center; color: #999;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        )
        
        await browser.close()
        
    print("PDF 파일 변환 완료:", pdf_path)
    
    # 임시 HTML 파일 삭제
    if os.path.exists(html_path):
        os.remove(html_path)
        print("임시 HTML 파일 삭제 완료")

if __name__ == "__main__":
    asyncio.run(md_to_pdf())
