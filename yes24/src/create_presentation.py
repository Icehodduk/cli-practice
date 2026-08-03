# -*- coding: utf-8 -*-
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # 16:9 와이드스크린 규격 설정 (13.333인치 x 7.5인치)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 네오 브루탈리즘(Neo-Brutalism) 테마 색상 정의 (RGBColor)
    COLOR_BG_WHITE = RGBColor(255, 255, 255)     # 순수 화이트 배경
    COLOR_BLACK = RGBColor(0, 0, 0)               # 칼같은 검은색 테두리 및 그림자
    COLOR_BRUTAL_YELLOW = RGBColor(245, 245, 0)   # 비비드 옐로우 (간지/액센트)
    COLOR_BRUTAL_LIME = RGBColor(204, 255, 0)     # 비비드 네온 라임 (포인트)
    COLOR_BRUTAL_RED = RGBColor(255, 59, 48)      # 시그널 레드 (강조)
    COLOR_GRAY_LINE = RGBColor(213, 216, 220)     # 가이드라인 회색
    
    # 폰트 명칭 정의 (사용자 조건 지정)
    FONT_TITLE = "Gmarket Sans Bold"
    FONT_BODY = "NanumGothic"
    
    # 이미지 디렉토리 경로 설정
    IMAGES_DIR = "yes24/images"
    
    def apply_solid_background(slide, color):
        """슬라이드 전체 배경에 단색 사각형 도형을 깔아 배경색을 지정합니다."""
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = color
        bg_shape.line.fill.background()  # 테두리 없음
        # 맨 뒤로 보내기
        slide.shapes._spTree.remove(bg_shape._element)
        slide.shapes._spTree.insert(2, bg_shape._element)
        return bg_shape
        
    def add_brutal_card(slide, left, top, width, height, fill_color=COLOR_BG_WHITE):
        """네오 브루탈리즘 특유의 두꺼운 검은색 테두리와 2D 하드 섀도우를 가진 카드를 생성합니다."""
        # 1) 그림자 사각형 (검은색, 테두리 없음, 약간 오프셋)
        shadow = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left + Inches(0.08), top + Inches(0.08), width, height
        )
        shadow.fill.solid()
        shadow.fill.fore_color.rgb = COLOR_BLACK
        shadow.line.fill.background()
        
        # 2) 전면 카드 사각형 (두꺼운 검은색 테두리)
        card = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = COLOR_BLACK
        card.line.width = Pt(2.5)
        
        return card

    def add_title(slide, title_text, subtitle_text=None, is_dark_bg=False):
        """모든 내용 슬라이드에 통일감 있는 네오 브루탈리즘 제목 레이아웃을 구성합니다."""
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(11.9), Inches(1.0))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE if is_dark_bg else COLOR_BLACK
        
        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = FONT_BODY
            p2.font.size = Pt(14)
            p2.font.color.rgb = COLOR_WHITE if is_dark_bg else COLOR_BLACK
            p2.space_before = Pt(5)
            
        # 굵고 칼 같은 2.5pt 순수 검은색 구분 가이드라인선 추가
        if not is_dark_bg:
            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.3), Inches(11.933), Inches(0.03)
            )
            line.fill.solid()
            line.fill.fore_color.rgb = COLOR_BLACK
            line.line.fill.background()

    def format_text_run(run, font_name, size_pt, bold=False, color_rgb=COLOR_BLACK):
        """텍스트 런 개체의 서식을 빠르게 통일합니다."""
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = color_rgb

    # 32장 슬라이드 전체의 내용과 발표 대본 데이터셋 정의
    slides_data = [
        # 1. 표지 슬라이드
        {
            "type": "cover",
            "title": "YES24 도서 데이터 탐색적 데이터 분석",
            "subtitle": "데이터로 파악하는 최신 IT 도서 시장 트렌드 및 요약 대시보드",
            "meta": "발표자: 전문 데이터 분석가  |  작성일: 2026년 7월 15일",
            "notes": "안녕하십니까, 오늘 발표를 맡은 전문 데이터 분석가입니다. 오늘 제가 소개해드릴 프로젝트는 국내 최고의 도서 유통 채널인 YES24의 IT 전문 도서 데이터 1,200건을 대상으로 진행한 탐색적 데이터 분석, 즉 EDA 결과 보고입니다. 현대 IT 산업과 기술 생태계는 눈부시게 빠른 속도로 변화하고 있습니다. 새로운 프로그래밍 언어, 새로운 인공지능 프레임워크가 매달 쏟아져 나오는 현 상황 속에서 출판업계나 IT 교육 마케팅 조직이 과거의 직관과 경험에만 의존해 경영 의사결정을 내리는 것은 대단히 위험한 선택입니다. 본 분석에서는 가격 정책의 실효성, 도서정가제 하의 할인율 분포, 인기도 지표의 극심한 양극화 현상, 그리고 최근 생성형 AI 열풍으로 대표되는 키워드 변동 흐름을 명확한 시각적 차트와 통계 수치로 보여드릴 것입니다. 아울러 이러한 통계적 분석 성과가 실제 기획과 매출 확대로 이어질 수 있도록, 실무 중심의 구체적인 3대 비즈니스 액션 플랜을 제시하고자 합니다. 그럼 다음 슬라이드로 이동하여 발표 목차부터 점검해 보겠습니다."
        },
        # 2. 발표 목차
        {
            "type": "toc",
            "title": "발표 목차",
            "sections": [
                {"num": "I", "name": "프로젝트 개요 및 데이터 프로파일링", "desc": "분석 배경, 수집 데이터 구조 및 데이터 정제 결과 검증", "icon": "📋"},
                {"num": "II", "name": "핵심 시각화 및 비즈니스 인사이트", "desc": "10대 주요 그래프 분석과 인구통계 및 TF-IDF 키워드 도출", "icon": "📈"},
                {"num": "III", "name": "종합 결론 및 비즈니스 제언", "desc": "IT 도서 시장 점유율 확대를 위한 3대 핵심 액션 플랜", "icon": "💡"}
            ],
            "notes": "오늘 프레젠테이션은 총 세 개의 메이저 세션으로 나누어 진행할 예정입니다. 첫 번째 세션에서는 본 데이터 분석 프로젝트를 수행하게 된 전략적 배경과 수집된 데이터의 열 구조, 그리고 통계 분석의 기초인 데이터의 정합성과 완결성을 입증하기 위해 거친 프로파일링 결과를 브리핑하겠습니다. 분석 데이터의 무결성이 보증되어야만 이후 제시할 시각화의 신뢰도가 올라가기 때문입니다. 두 번째 세션에서는 본 분석의 가장 핵심적인 알맹이인 10가지 시각화 그래프를 심층적으로 뜯어볼 것입니다. 변수 각각의 단일 분포부터 시작하여, 가격과 인기도의 연관 관계, 독자 리뷰수와 판매지수의 상관 분석, 그리고 사이킷런을 활용한 텍스트 마이닝 키워드 가중치를 설명해 드리고자 합니다. 마지막 세 번째 세션에서는 데이터 탐색을 통해 도출한 가치를 실제 매출 성장과 브랜드 강화로 전환시킬 수 있도록 3가지 핵심 제언으로 결론을 맺겠습니다. 그럼 첫 번째 장으로 넘어가 본격적인 데이터를 마주해 보겠습니다."
        },
        # 3. 세션 1 간지
        {
            "type": "divider",
            "title": "Session I",
            "subtitle": "프로젝트 개요 및 데이터 프로파일링",
            "desc": "분석 목표 및 데이터 무결성 검증 세션 시작",
            "notes": "첫 번째 대주제인 프로젝트 개요 및 데이터 프로파일링 파트입니다. 많은 조직이 데이터 분석을 할 때, 로우 데이터를 그냥 불러와서 바로 시각화부터 돌려버리는 실수를 하곤 합니다. 하지만 원천 데이터에 채워지지 않은 결측치가 얼마나 있는지, 유령 회원이나 중복된 트랜잭션이 몇 개나 끼어있는지 미리 알지 못한다면 왜곡된 요약 수치를 받아들게 됩니다. 따라서 이번 장에서는 수집 대상 IT 도서 데이터셋의 크기와 결측치의 통계, 그리고 중복 데이터 검증 과정을 통해 분석을 전개할 기반이 완벽하게 안전하고 평평하다는 것을 증명해 보이겠습니다. 다음 슬라이드로 가시죠."
        },
        # 4. 분석 목표
        {
            "type": "infographic_cards",
            "title": "프로젝트 분석 목표",
            "cards": [
                {"title": "독자 반응 연관 분석", "body": "도서 가격 정책, 할인율, 리뷰 수 및 판매지수 간의 연관관계를 수치적으로 규명합니다.", "icon": "📊"},
                {"title": "공급 트렌드 파악", "body": "연도별 도서 공급 건수 추이와 메이저 출판사 및 다작 저자 중심의 과점 현상을 파악합니다.", "icon": "🏷️"},
                {"title": "텍스트 트렌드 도출", "body": "도서 제목과 설명에 사용된 단어를 TF-IDF 수학 모델로 계량화해 핵심 기술 유행을 분석합니다.", "icon": "🔑"}
            ],
            "notes": "프로젝트의 분석 목표에 대해 말씀드리겠습니다. 본 탐색적 분석의 핵심 지향점은 세 가지로 나누어집니다. 첫째, 도서의 가격과 할인율이라는 공급자 측면의 가격 설정이 소비자의 즉각적인 액션인 리뷰 개수와 판매지수에 어떤 관계를 가지는지 통계적으로 입증하는 것입니다. 둘째, 시간의 흐름에 따른 신간 도서의 발행 건수를 시계열적으로 추적하고, 국내 IT 출판 시장을 지탱하고 있는 7대 출판사와 스타 필진들의 생태계 점유율을 정량화하여 과점 실태를 파악하는 것입니다. 셋째, 단순 형태소 분석의 속도 한계를 극복하기 위해, 사이킷런 라이브러리를 사용해 문맥 속 핵심 단어들의 가중치를 TF-IDF 모델로 연산하여 최신 IT 도서 시장을 완전히 지배하고 있는 핵심 신기술 트렌드를 계량적으로 가시화하는 것이 궁극적인 목표입니다."
        },
        # 5. 데이터셋 구조
        {
            "type": "infographic_grid",
            "title": "데이터셋 구조 및 수집 현황",
            "left_text": "수집된 데이터셋은 YES24 온라인 서점에 등록된 IT 전문 서적 1,200건의 행으로 구성되어 있습니다. 도서 정보 파악을 위한 11개의 원천 속성(Column)을 완벽히 수집 완료했습니다.",
            "right_cards": [
                {"label": "데이터 전체 규모", "val": "1,200 행 (Rows)", "icon": "📁"},
                {"label": "원천 속성 수", "val": "11개 컬럼 (Columns)", "icon": "⚙️"},
                {"label": "추가 파생 변수", "val": "할인율, 발행연도, 발행월", "icon": "🔗"}
            ],
            "notes": "저희가 수집한 데이터셋의 구체적인 레이아웃과 수집 현황입니다. 데이터셋은 YES24 온라인 서점에 등록된 IT 도서 카테고리 중 대표적인 베스트셀러 및 스테디셀러 목록 1,200개의 레코드를 추출하여 구성했습니다. 컬럼은 도서 제목, 저자, 출판사, 발행일, 정가, 판매가, 리뷰 수, 판매지수, 설명, 상세 정보, URL 등 총 11가지의 원천 변수들을 수집했습니다. 특히, 정밀 분석을 위해 원천 데이터에만 머무르지 않고, 정가 대비 판매가를 수학적으로 산출한 '할인율' 파생변수를 공식으로 산출해냈으며, 날짜 텍스트 슬라이싱을 통해 '발행연도'와 '발행월'이라는 3가지 파생변수를 추가로 엔지니어링하여 분석의 차원을 넓혔습니다."
        },
        # 6. 결측치 및 중복 데이터 분석
        {
            "type": "infographic_cards",
            "title": "결측치 및 중복 데이터 정제 결과",
            "cards": [
                {"title": "핵심 수치 완결성 100%", "body": "정가, 판매가, 판매지수, 리뷰 수 등 핵심 통계 변수의 결측치는 0건으로 완벽한 완결성을 보입니다.", "icon": "💯"},
                {"title": "일부 메타정보 결측", "body": "저자(2건), 설명(28건), 상세 정보(439건)에서 결측이 관찰되며 이는 목차 미등록 등 업계 관행입니다.", "icon": "⚠️"},
                {"title": "중복 레코드 0건", "body": "수집 단계부터 디듀플리케이션(중복 제거) 알고리즘을 적용하여 1,200행 모두 순수 유니크 레코드입니다.", "icon": "🧹"}
            ],
            "notes": "데이터 정제와 신뢰도 검증 결과에 대해 설명해 드리겠습니다. 데이터 적재 후 빈 값인 결측치를 정밀 검사한 결과, 다행히도 분석의 가장 중심축이 되는 제목, 출판사, 정가, 판매가, 리뷰 수, 판매지수 등의 숫자 기반 변수에서는 결측치가 단 1건도 없는 100%의 무결성을 나타냈습니다. 다만 텍스트 메타데이터 영역인 저자 명에서 2건, 책 요약 설명에서 28건의 빈 값이 관찰되었습니다. 특히 도서의 상세 목차가 포함되는 상세 정보 컬럼은 439건의 비교적 높은 결측을 보였습니다. 이는 신생 소형 출판사나 일부 입문서 등록 시 온라인 서점 상세페이지에 목차나 상세 기획 요약을 등록하지 않고 배포하는 출판 업계의 입력 누락 관행이 고스란히 데이터에 투영된 것입니다. 중복 데이터 역시 엄격히 검사했으나, 완벽한 필터링을 거쳤기에 중복 레코드는 0건으로 보장합니다."
        },
        # 7. 세션 2 간지
        {
            "type": "divider",
            "title": "Session II",
            "subtitle": "핵심 시각화 및 비즈니스 인사이트",
            "desc": "10대 주요 시각화 차트 및 상관관계 분석",
            "notes": "두 번째 세션인 핵심 시각화 및 비즈니스 인사이트 파트입니다. 이 세션은 본 프레젠테이션의 가장 강력한 비주얼 영역으로, 총 10가지 시각화 차트와 그에 부합하는 분석가의 해설이 준비되어 있습니다. 그래프의 왜곡을 방지하기 위해 임의의 3D 입체 효과나 과장된 그라데이션을 철저히 배제하고, 데이터를 평면상에 객관적으로 가시화하는 플랫 디자인의 2D 그래프를 제작하여 노르딕 미니멀리즘 테마에 부합하도록 배치했습니다. 각 그래프 장표 우측에는 실재 분석 과정에서 도출한 고해상도 이미지 차트를 삽입하였고, 바로 다음 장표에는 그 이면의 비즈니스적 가치와 의사결정 전략을 매핑했습니다. 그럼 첫 번째 그래프인 정가 및 판매가 분포 슬라이드로 넘어가겠습니다."
        },
        # 8. 도서 정가 및 판매가 분포 (이미지)
        {
            "type": "image_layout",
            "title": "도서 정가 및 판매가 가격 분포",
            "image": "01_price_distribution.png",
            "desc": "IT 전문 도서의 정가(파란색) 및 판매가(주황색)의 가격 구간별 빈도를 나타낸 히스토그램입니다. 대부분의 기술 서적이 1.5만 원에서 3만 원 사이에 쏠려 있는 항아리형 구조를 취하고 있습니다.",
            "notes": "오른쪽에 보이시는 히스토그램 차트는 YES24 IT 카테고리 도서들의 정가 분포와 실재 할인 적용된 판매가 분포를 함께 비교하여 보여줍니다. 두 그래프의 면적이 겹쳐져 있는 구간을 살펴보시면, 대다수의 도서들이 15,000원에서 30,000원 선에 집중적으로 모여 있는 단일 봉우리 형태의 히스토그램을 확인할 수 있습니다. 평균 정가는 23,799원이며 실제 고객이 결제하는 판매가 평균은 21,985원입니다. 중앙값 역시 정가 23,000원, 판매가 21,000원으로 평균치와 매우 밀접하게 닿아 있습니다. 4만 원 이상으로 꼬리가 길게 뻗어나가는 극소수 고가 서적들은 대학 학부 전공 교재나 전문 아카데믹 번역 서적들인 반면, 1만 원대 미만의 저가 서적들은 요약본이나 얇은 치트시트 형태에 한정됩니다. 이어서 이 가격적 특성이 시사하는 기획 인사이트를 짚어보겠습니다."
        },
        # 9. 가격 정책 인사이트
        {
            "type": "infographic_grid",
            "title": "가격 포지셔닝 및 저항선 극복 방안",
            "left_text": "도서 정가와 판매가는 1.5만 원 ~ 3만 원 사이에 압도적으로 분포해 있습니다. 이는 독자층이 가격 저항감을 가장 덜 느끼는 최적 가격대(Sweet Spot)임을 증명합니다.",
            "right_cards": [
                {"label": "가격 스윗 스팟", "val": "20,000원 ~ 24,000원", "icon": "🎯"},
                {"label": "고가 프리미엄 존", "val": "40,000원 초과 전문서", "icon": "💎"},
                {"label": "기획 지향성", "val": "심리적 저항선을 고려한 정가 책정", "icon": "✏️"}
            ],
            "notes": "도서 가격 분포 분석이 주는 출판 기획 부서의 인사이트입니다. IT 서적 구매자들은 학생부터 현업 주니어 개발자까지 매우 다양한 경제적 계층으로 구성됩니다. 이들이 책 한 권을 살 때 '이 정도면 부담 없이 내 지식을 위해 투자할 수 있다'고 느끼는 마지노선이 바로 2만 원대 초반입니다. 따라서 신진 필진이나 대중적인 입문 기술서를 기획할 때는 반드시 정가를 24,000원 이하로 책정하여 초기 시장 진입 허들을 낮춰야 합니다. 반면, 4만 원을 호가하는 초고가 서적들은 독자 모수가 작고 매우 좁은 기술 도메인을 다루지만, 대체 불가능한 지식을 제공하므로 가격 탄력성이 아주 낮습니다. 이러한 책들은 무리하게 단가를 낮추기보다는 고가 정책을 고수하여 권당 영업 마진을 지켜내는 포트폴리오 이원화 전략을 추천해 드립니다."
        },
        # 10. 도서 할인율 분포 (이미지)
        {
            "type": "image_layout",
            "title": "도서 할인율 구간별 빈도 분포",
            "image": "02_discount_rate_distribution.png",
            "desc": "파생변수로 산출된 도서 할인율의 빈도 히스토그램입니다. 법이 허용하는 최대치인 10% 영역에 압도적으로 많은 데이터가 집중되어 장벽을 형성하고 있습니다.",
            "notes": "우측의 차트는 도서 할인율의 분포를 시각화한 것입니다. 우리나라는 출판 시장 상생과 동반 성장을 위해 법률로써 1년에 최대 10%의 가격 할인만을 허용하는 도서정가제를 엄격히 고수하고 있습니다. 이 법적 장벽의 위세가 데이터에 고스란히 반영되어, 할인율 10% 지점에 빌딩처럼 높은 막대그래프가 솟아있는 것을 확인하실 수 있습니다. 평균 할인율은 7.02%이며, 중앙값은 정확히 10.0%입니다. 여기서 특별히 눈여겨볼 점은 단 1%의 할인도 제공하지 않는 할인율 0%인 도서들의 점유율이 25.3%에 달한다는 점입니다. 이 네 권 중 한 권 꼴의 무할인 도서들은 주로 정가 유통이 고집되는 대학교 학부 전공도서나 특수 전문 기획서들입니다. 다음 슬라이드에서 비가격 마케팅의 당위성에 대해 이야기해 보겠습니다."
        },
        # 11. 할인율 인사이트
        {
            "type": "infographic_cards",
            "title": "법적 할인율 규제에 따른 비가격 마케팅",
            "cards": [
                {"title": "할인 변별력 상실", "body": "대다수의 IT 단행본이 10% 할인을 상수로 적용하고 있어 판매가 기준의 경쟁은 의미가 없습니다.", "icon": "❌"},
                {"title": "할인율 0% 서적 존재", "body": "학술 전공서나 대학 교재는 약 25% 비율로 무할인 정가제 유통을 고수하며 마진을 보전합니다.", "icon": "🏛️"},
                {"title": "비가격 혜택 다양화", "body": "사은품 부록 제공, 독점 예제 코드 공유, 온라인 강의 결합 등 부가 혜택으로 승부해야 합니다.", "icon": "🎁"}
            ],
            "notes": "도서정가제로 인해 모든 도서가 동일한 10% 할인을 취함에 따라, 소비자 관점에서는 어느 서점이나 어느 출판사의 책을 고르더라도 가격 메리트 측면에서의 변별력은 완전히 상실된 상태입니다. 따라서 마케터들이 상세페이지에서 '저렴한 판매가'를 무기로 내세우는 영업 방식은 비효율적입니다. 독자가 우리 책을 사게 만들려면 가격 할인이 아닌 비가격 혜택의 다각화가 유일한 해결책입니다. 예를 들어, 예비 독자들을 위해 저자가 직접 줌 라이브로 진행하는 주말 특강 참여권을 선착순 제공한다던가, 책에 실린 프로젝트 소스코드의 상세 해설과 버그 수정 패치를 실시간으로 다운로드할 수 있는 멤버십 허브를 연동해주는 등, 책 외부의 추가적인 가치 포장(Value Wrapping)에 총력을 기울여야 합니다."
        },
        # 12. 도서 판매지수 분포 (이미지)
        {
            "type": "image_layout",
            "title": "도서 판매지수의 롱테일 분포",
            "image": "03_sales_index_distribution.png",
            "desc": "인기도 척도인 판매지수의 왜도를 보여주는 상자수염그림(Box-plot) 및 히스토그램입니다. 대다수 도서는 매우 낮은 지수이나 극소수의 베스트셀러가 극단적인 아웃라이어를 만듭니다.",
            "notes": "우측에 표시된 상자수염그림(Box-plot)은 도서 판매지수의 극단적인 분포 왜곡을 가시화하고 있습니다. 판매지수는 온라인 서점의 실질적인 유통 성공 여부를 가늠하는 척도입니다. 분석 결과 판매지수의 평균값은 1,647점으로 집계되지만, 중앙값은 겨우 487점에 머물고 있습니다. 상위 75% 분위수마저 1,344점에 그쳐, 대부분의 평범한 IT 기술서들은 몇 백에서 천 단위 초반의 낮은 스코어 영역에 밀집되어 조용히 묻혀 있습니다. 반면, 분포의 꼬리 끝자락인 최댓값은 무려 87,927점에 달합니다. 이 상상을 초월하는 아웃라이어들은 메이저 입문서 시리즈나 트렌드 메이커 서적들이며, 이들 소수의 히트 서적이 시장의 모든 파이를 먹어치우는 승자독식 구조가 입증되었습니다. 다음 장에서 파레토 법칙과 타겟 마케팅을 연결하여 조망하겠습니다."
        },
        # 13. 판매지수 인사이트
        {
            "type": "infographic_grid",
            "title": "도서 시장 인기도 양극화 극복 전략",
            "left_text": "판매지수의 통계 중앙값(487)과 최댓값(87,927)의 극심한 격차는, 전형적인 파레토 법칙(80대 20)을 대변합니다. 소수의 킬러 도서 육성에 리소스를 집중해야 생존이 가능합니다.",
            "right_cards": [
                {"label": "중앙값 vs 최댓값", "val": "487.5 점 vs 87,927.0 점", "icon": "⚖️"},
                {"label": "파레토 쏠림 비중", "val": "상위 5% 도서가 총인기도 점유", "icon": "⚡"},
                {"label": "마케팅 자원 배분", "val": "선택과 집중을 통한 메가 스타 도서 기획", "icon": "🎯"}
            ],
            "notes": "판매지수 양극화 분석이 주는 마케팅 예산 집행 부서의 인사이트입니다. 모든 신간 도서가 고르게 잘 팔리기를 바라며 모든 책에 균등한 수준의 온라인 배너 광고비나 소셜 미디어 홍보비를 분산 투자하는 방식은 예산의 낭비일 뿐입니다. 데이터가 입증하듯 도서 흥행 산업은 전형적인 파레토 법칙을 따릅니다. 따라서 한정된 마케팅 재원을 확실한 대중성과 최신 트렌드를 갖춘 소수의 '킬러 타이틀' 후보군에 약 70% 이상 집중적으로 몰아주어야 합니다. 이렇게 탄생한 메가 베스트셀러 도서가 출판사 브랜드 가치를 끌어올리면, 그 브랜드 인지도라는 낙수효과를 통해 같은 출판사에서 나온 다른 마이너 도서들까지 동반 판매 성장을 일으키는 패밀리십 유도 마케팅이 비즈니스 효율을 극대화합니다."
        },
        # 14. 도서 리뷰 수 분포 (이미지)
        {
            "type": "image_layout",
            "title": "독자 평판 지표인 리뷰 수 분포",
            "image": "04_review_count_distribution.png",
            "desc": "온라인 서점 도서 상세페이지에 누적된 리뷰 수의 빈도 분포도입니다. 구매에 비해 적극적으로 평판(리뷰)을 남기는 독자의 비율이 현저히 낮음을 뜻합니다.",
            "notes": "우측 차트는 도서별 리뷰 수의 분포를 보여줍니다. 분석에 따르면 평균 리뷰 개수는 약 11.6개이지만, 중앙값은 단 4개에 불과합니다. 전체의 절반이 넘는 도서들이 누적 리뷰 건수가 4개 미만인 무평판의 늪에 빠져 있다는 의미입니다. 반면 최댓값은 205개에 달해, 구매 및 리뷰가 많이 달린 극소수의 책들로 독자들이 더 쏠리는 평판의 양극화가 뚜렷합니다. 이는 독자들이 책을 구매하여 유용하게 활용하더라도, 인터넷 서점에 재로그인하여 길고 자세한 별점 리뷰를 남길 유인이 극단적으로 적다는 것을 시사합니다. 리뷰가 쌓여있지 않으면 후속 예비 구매자들은 신뢰성을 잃게 됩니다. 이 피드백 결핍 문제를 어떻게 풀어나가야 할지 다음 슬라이드에서 짚어보겠습니다."
        },
        # 15. 리뷰 수 인사이트
        {
            "type": "infographic_cards",
            "title": "평판 인프라 확보를 위한 능동적 피드백 루프",
            "cards": [
                {"title": "자발적 리뷰의 한계", "body": "독자들의 리뷰 작성률은 지극히 낮으며, 중앙값 4개가 보여주듯 인위적인 장치 없이는 평판 구축이 불가능합니다.", "icon": "🔒"},
                {"title": "사회적 증거의 결핍", "body": "리뷰가 없는 상세페이지는 구매 전환율이 현격하게 떨어지는 주원인이 되므로 초반 방어벽 형성이 필수적입니다.", "icon": "🧱"},
                {"title": "리워드 마케팅 공식화", "body": "상세한 기술 서평단 운영, 기프티콘 지급 이벤트, 우수 피드백 보상 등 능동적 리워드로 리뷰 수를 펌핑해야 합니다.", "icon": "📣"}
            ],
            "notes": "리뷰수 분포 결과는 초기 평판 관리인 '사회적 증거' 확보에 마케팅 예산을 의무적으로 배정해야 함을 증명합니다. 독자들은 구매 버튼을 누르기 직전 상세페이지 하단으로 스크롤하여 먼저 책을 구입한 선배들의 리뷰을 읽으며 최종적인 확신을 얻습니다. 만약 리뷰 수가 0개이거나 1~2개뿐이라면 예비 독자는 이 책의 코드 퀄리티에 신뢰를 잃고 장바구니에서 책을 지워버립니다. 따라서 출판사는 신간 론칭 전 최소 20명 이상의 베타리더를 선제 모집하여 출간일 당일에 일제히 리뷰가 기재되도록 설계해야 합니다. 또한 우수 서평단에게 커피 기프티콘이나 도서 문화상품권을 지급하는 상시 리워드 제도를 공식 가이드라인화하여 평판 장벽을 조기에 돌파해야 합니다."
        },
        # 16. 연도별 도서 발행 건수 추이 (이미지)
        {
            "type": "image_layout",
            "title": "연도별 도서 신간 발행 건수 추이",
            "image": "05_yearly_publish_trend.png",
            "desc": "수집된 1,200권의 연도별 발행량 막대 차트입니다. 2024년 이후 최근 3개년에 신간의 약 80% 이상이 집중되어 있어 정보의 시의성이 극단적으로 높습니다.",
            "notes": "오른쪽에 있는 시계열 막대그래프는 연도별 도서 신간 발행 건수의 점유율 추이를 보여줍니다. 분석을 보시면 2024년 이전의 모든 연도별 발행량을 전부 더해봤자 192권(16%)에 불과합니다. 반면 2024년 170권(14%), 2025년 403권(33%), 그리고 현재 연도인 2026년에는 무려 405권(33.8%)의 높은 발행량을 기록하고 있습니다. 이는 본 연구에 활용된 YES24의 대표 도서 데이터가 주로 시중에서 활발히 유통되고 있는 신간 위주로 구성되어 있음을 알려주는 동시에, IT 기술 출판의 패러다임이 얼마나 빠르게 돌며 구버전 도서들이 도태되고 있는지를 단적으로 보여주는 지표입니다. 다음 장에서 지식 가치 반감기 piggyback 대응법을 살펴보겠습니다."
        },
        # 17. 연도별 추이 인사이트
        {
            "type": "infographic_grid",
            "title": "정보기술 수명 단축에 따른 애자일 기획",
            "left_text": "최근 3개년의 신간 발행량이 80% 이상을 차지하는 현상은, IT 기술 지식의 교체 주기가 극단적으로 압축되었음을 대변합니다. 신속한 개정판 프로세스가 필수적입니다.",
            "right_cards": [
                {"label": "최근 3개년 발행 비중", "val": "81.6% (978 / 1,200권)", "icon": "📅"},
                {"label": "지식 수명 반감기", "val": "약 1년 ~ 1.5년 수준", "icon": "⌛"},
                {"label": "대응 기획 모델", "val": "6개월 단위 초고속 개정 프로세스", "icon": "🚀"}
            ],
            "notes": "연도별 발행 추이가 시사하는 출판 기획본부의 지휘 방향성입니다. 일반적인 소설이나 자기계발서는 한 번 베스트셀러에 진입하면 수년간 지속적으로 판매되어 효자 노릇을 합니다. 반면 IT 실무서는 프레임워크나 개발 언어의 버전이 1.0에서 2.0으로 올라가는 순간, 구버전을 다루던 책의 판매지수는 순식간에 절벽에서 떨어지듯 0으로 수렴합니다. 지식의 유통기한이 1년 남짓으로 줄어든 것입니다. 기획 부서는 이러한 빠른 라이프사이클에 대응하기 위해 저자 필진들과 상시 소통 채널을 가동하고, 핵심 도서에 대해서는 출간 즉시 다음 버전 개정판(Revision) 집필 일정을 계약서에 사전 명기하는 등 고속 순환 기획(Agile Publishing) 모델로 완전히 체질을 개선해야 합니다."
        },
        # 18. 판매가와 판매지수의 상관관계 (이미지)
        {
            "type": "image_layout",
            "title": "도서 가격과 판매지수 간의 상관관계",
            "image": "06_price_vs_sales_index.png",
            "desc": "판매 가격(X축)과 판매지수(Y축)의 연관 관계를 분석한 산점도 차트입니다. 상관계수는 0.035로 선형 관계가 전혀 관찰되지 않는 완전히 독립적인 양상입니다.",
            "notes": "우측 산점도 그래프는 도서의 실재 판매가와 독자의 인기도인 판매지수를 각 점으로 찍어 표현한 이변량 관계 분석입니다. 통계적 선형 흐름을 나타내는 추세선이 거의 바닥에 수평으로 누워있는 것을 관찰하실 수 있습니다. 수학적으로 계산한 피어슨 상관계수(R) 역시 **0.0352**로 0에 수렴하며, 결정계수인 R스퀘어는 0.0012에 불과합니다. 이는 가격이 비싸면 안 팔릴 것이라는 전통적인 통념과 달리, 실제 IT 서적 구매 의사결정에서 가격의 높고 낮음은 베스트셀러 진입에 아무런 인과 관계나 영향을 주지 못한다는 명확한 사실을 의미합니다. 독자들은 가격이 다소 비싸더라도 필요한 전문 지식이라면 과감히 구매한다는 것입니다. 이어서 가격 프리미엄 정책 수립 방안을 이야기해 보겠습니다."
        },
        # 19. 가격-판매지수 인사이트
        {
            "type": "infographic_cards",
            "title": "가격 장벽을 초월하는 기술 콘텐츠 파워",
            "cards": [
                {"title": "가격 탄력성의 한계", "body": "상관계수 0.03이 입증하듯, 소비자는 가격 변수의 하락보다는 콘텐츠의 신뢰도와 실무 적용성에 반응합니다.", "icon": "📉"},
                {"title": "저단가 출혈 경쟁 지양", "body": "지면을 억지로 줄여 단가를 2,000원 낮추는 정책은 마진을 훼손할 뿐 매출 증대에 기여하지 않습니다.", "icon": "💸"},
                {"title": "프리미엄 프라이싱 수립", "body": "책의 볼륨과 소스코드 퀄리티를 최상으로 보장하여 단가를 높게 책정(Premium Pricing)하는 것이 고수익에 유리합니다.", "icon": "👑"}
            ],
            "notes": "가격과 판매지수의 통계적 독립성이 입증하는 출판사의 마진 극대화 전략입니다. 동종 경쟁사 도서 대비 판매가를 10% 낮추기 위해 편집 단계를 무리하게 압축하거나 퀄리티 높은 삽화나 차트를 생략하여 책의 깊이를 낮추는 행동은 비즈니스 관점에서 가장 어리석은 패착입니다. IT 독자들은 자신의 커리어 성장과 문제 해결을 위해 도서를 구매하므로 가격 저항감이 대단히 낮습니다. 출판사는 가격을 낮추는 고민을 할 것이 아니라, 오히려 예제 프로젝트의 실무 구현도를 올리고 지면을 아낌없이 늘려 완성도를 최고로 확보해야 합니다. 그렇게 책의 정가를 30,000원대 중반으로 높여 프리미엄 가격 정책을 취하더라도, 콘텐츠만 유일무이하다면 판매지수는 동일하게 확보되고 출판사의 이익률은 수배로 급증할 것입니다."
        },
        # 20. 판매지수와 리뷰 수의 상관관계 (이미지)
        {
            "type": "image_layout",
            "title": "판매지수와 리뷰 수의 상관관계",
            "image": "07_sales_index_vs_reviews.png",
            "desc": "인기도 척도인 판매지수와 독자 평판 지표인 리뷰 수의 상관관계를 그린 산점도 차트입니다. 피어슨 상관계수 0.361로 뚜렷하고 유의미한 양의 상관관계를 보입니다.",
            "notes": "우측에 보이는 산점도와 우상향 추세선은 판매지수와 누적 리뷰 수 간의 관계를 보여줍니다. 분석을 통해 도출한 피어슨 상관계수(R)는 **0.3611**로, 통계적으로 매우 유의미한 양의 상관관계가 검출되었습니다. 책이 많이 팔려 판매지수가 오르면 리뷰가 달릴 모수가 늘어나므로 자연스레 리뷰 수가 비례하여 상승하는 현상입니다. 하지만 이를 뒤집어 마케팅 관점으로 조망해보면 엄청난 마케팅 고리가 성립됩니다. 즉, 초기 도서 론칭 시 마케팅 활동을 통해 리뷰를 인위적으로 누적시켜 놓으면, 예비 소비자들의 심리적 장벽이 해제되어 판매지수가 오르고, 오른 판매지수가 다시 자발적 독자 리뷰를 생산해내는 '자기 강화적 피드백 루프'가 형성된다는 것입니다. 다음 슬라이드에서 자세한 선순환 시나리오를 설명해 드리겠습니다."
        },
        # 21. 판매지수-리뷰 수 인사이트
        {
            "type": "infographic_grid",
            "title": "구매 설득을 돕는 평판의 선순환 메커니즘",
            "left_text": "상관계수 0.36은 판매와 평판이 서로의 성장 동력이 되는 공생 관계임을 입증합니다. 초기 1개월 내에 리뷰수 30개 돌파라는 고정 목표를 달성해야 장기 흥행 궤도에 진입합니다.",
            "right_cards": [
                {"label": "상관계수 수치", "val": "0.3611 (양의 상관성)", "icon": "📊"},
                {"label": "흥행 모멘텀 골든타임", "val": "출간 후 초기 4주 이내", "icon": "⏱️"},
                {"label": "핵심 마케팅 지표", "val": "서평단 유치를 통한 초기 평점 방어", "icon": "🛡️"}
            ],
            "notes": "상관 분석이 말해주는 흥행 선순환 마케팅 실무 적용 가이드입니다. 책의 생애 주기에서 베스트셀러 진입 여부를 판가름하는 골든타임은 출간 후 초기 4주 이내입니다. 이 한 달 동안 평점 9.5점 이상과 성실한 텍스트 리뷰 30개 이상을 선제 확보하는 일명 '평판 방어선'을 뚫어놓아야 합니다. 초기 리뷰어가 '이 책의 예제 코드는 최신 파이썬 3.12 버전에서 한 줄의 에러도 없이 정상 동작합니다'라는 사회적 증거를 상세페이지 하단에 깔아두면, 긴가민가하던 일반 독자들의 장바구니 전환율이 비약적으로 뛰게 되고, 이는 곧 판매지수 폭발로 이어져 메가 히트 서적으로 도약하는 밑거름이 됩니다."
        },
        # 22. 상위 30개 출판사 도서 발행 점유율 (이미지)
        {
            "type": "image_layout",
            "title": "상위 30개 출판사 도서 발행 점유율",
            "image": "08_top_publishers.png",
            "desc": "도서 발행 점유율 상위 30개 출판사 현황을 보여주는 가로 막대 차트입니다. 커뮤니케이션북스와 한빛미디어가 독보적인 상위 2강을 점유하고 있습니다.",
            "notes": "우측에 보이는 수평 막대그래프는 YES24 IT 카테고리 도서를 유통 공급하는 공급선인 출판사별 발행량 점유 현황입니다. 분석 결과 1위 커뮤니케이션북스가 179권으로 14.9%, 2위 한빛미디어가 112권으로 9.3%의 높은 점유율을 차지하고 있습니다. 그 뒤를 이어 길벗 67권(5.6%), 제이펍 59권(4.9%) 등이 대형 퍼블리셔 그룹을 형성하고 있습니다. 이 상위 5대 IT 전문 출판사가 유통망에 제공하는 신간 공급 점유율이 전체의 약 37.8%에 달해, 소수 거대 출판사 브랜드가 공급 생태계를 쥐고 흔드는 과점 구조가 견고하게 정립되어 있음을 시사합니다. 메이저 출판사들은 막강한 편집 인프라와 자본력을 갖추고 있습니다. 이 구도 아래에서 중소 출판사들이 생존할 비책을 다음 장에서 해부해 보겠습니다."
        },
        # 23. 출판사 점유율 인사이트
        {
            "type": "infographic_cards",
            "title": "대형 출판사 과점 구조와 틈새 포지셔닝",
            "cards": [
                {"title": "과점적 공급 생태계", "body": "커뮤니케이션북스, 한빛미디어 등 상위 5대 브랜드가 전체 IT 도서 유통망의 37%를 공급하며 주도합니다.", "icon": "🏢"},
                {"title": "레드오션 경쟁 지양", "body": "소형 출판사가 파이썬 입문, C언어 기초 등 메이저사의 자본력이 쏠린 영역에서 정면 대결하는 것은 무모합니다.", "icon": "🥊"},
                {"title": "초포커스 틈새 시장 개척", "body": "메이저사가 다루지 못하는 마이크로 니치(Micro-niche) 기술 도메인을 타겟팅하여 브랜드 정체성을 확보해야 합니다.", "icon": "🔍"}
            ],
            "notes": "출판사 점유율 통계가 알려주는 중소 출판 기획사 생존 전략입니다. 메이저 출판사들은 막강한 번역 판권 조달 능력과 튼튼한 총판 유통 라인을 장악하고 있습니다. 규모가 작은 소형 출판사나 신규 퍼블리싱 스타트업이 메이저사들이 떡하니 버티고 있는 '파이썬 프로그래밍 첫걸음', 'HTML/CSS 입문' 같은 대중서 영역에 신간을 내미는 것은 계란으로 바위치기에 가깝습니다. 중소 출판사는 정면 대결을 피해, 덩치가 큰 대형사들이 의사결정 지연으로 놓치는 틈새(Micro-niche) 기술 도메인을 선점해야 합니다. 예를 들면, 챗GPT API를 활용한 프롬프트 엔지니어링 실무 템플릿, 혹은 클라우드 쿠버네티스 트러블슈팅 바이블처럼 실무 고인물 독자층을 타겟팅한 초포커스 기획만이 유효한 솔루션입니다."
        },
        # 24. 상위 30개 저자 도서 발행 수 (이미지)
        {
            "type": "image_layout",
            "title": "상위 30개 저자 도서 발행 건수",
            "image": "09_top_authors.png",
            "desc": "도서 발행량이 가장 왕성한 상위 30개 저자 명단 가로 막대 차트입니다. 서지영 저자와 장문철 저자가 각각 10권으로 서점 유통망 공급을 주도하고 있습니다.",
            "notes": "오른쪽에 보이는 차트는 가장 많은 IT 전문 서적을 집필 및 번역하여 시장에 내놓은 주요 저자 필진들의 분포 현황입니다. 분석 결과 공동 1위에 서지영 저자와 장문철 저자가 각각 10권의 방대한 집필 실적을 내세우며 선두를 쥐고 있습니다. 이어서 이석현, 이승우 저자 등이 그 뒤를 바짝 추격하고 있습니다. IT 출판 도메인 특유의 현상 중 하나는, 독자들이 특정 기술 저자의 명쾌한 코드 주석 설명 방식과 오류 없는 예제 설계력을 전적으로 신뢰하여, 그 저자가 다음 책을 쓰면 주저 없이 이어서 지갑을 여는 '저자 브랜드 로열티'가 대단히 굳건하다는 점입니다. 왕성하게 저작물을 지어내는 스타 필진 확보의 중요성을 다음 슬라이드에서 다뤄보겠습니다."
        },
        # 25. 저자 발행 수 인사이트
        {
            "type": "infographic_grid",
            "title": "스타 저자 육성 및 파트너십 구축 전략",
            "left_text": "최다 저작물을 출간한 서지영, 장문철 저자(각 10권) 사례는 IT 출판이 철저히 저자의 브랜드 파워에 종속되는 필진 비즈니스임을 시사합니다. 저자와의 동반 관계 구축이 시급합니다.",
            "right_cards": [
                {"label": "최다 집필 저자 권수", "val": "각 10권씩 출간 (서지영, 장문철)", "icon": "✍️"},
                {"label": "핵심 구매 요인", "val": "저자 명성에 기반한 두터운 신뢰 자산", "icon": "🤝"},
                {"label": "핵심 액션 아이템", "val": "지속적 집필 케어 및 독점 파트너십 계약", "icon": "📝"}
            ],
            "notes": "저자 지형 분석이 알려주는 핵심 필진 파너십 관리 제언입니다. IT 지식을 책으로 엮어낼 수 있는 인재풀은 한정되어 있습니다. 아무리 좋은 코딩 역량을 가졌어도 가르치는 전달력과 작문 능력이 부족하다면 베스트셀러를 쓸 수 없습니다. 기획팀은 업계에서 필력이 검증된 스타 저자들과의 단발성 계약을 넘어, 다년 계약 및 차기 기획 로드맵을 함께 설계하는 '장기적 기술 파트너십'을 맺어야 합니다. 저자가 오직 우리 출판사와만 차기작을 독점 집필할 수 있도록 충분한 인세 조건과 마케팅 밀어주기를 약속하고, 지속적으로 저자의 브랜딩 커리어를 매니징해주는 긴밀한 유대 관계 형성이 출판사의 영구적인 핵심 자산(Core Asset)을 확보하는 첩경입니다."
        },
        # 26. 도서 제목 및 설명 키워드 TF-IDF 분석 (이미지)
        {
            "type": "image_layout",
            "title": "도서 텍스트 TF-IDF 단어 가중치",
            "image": "10_text_keywords.png",
            "desc": "도서 제목과 요약 설명에 등장하는 단어들을 TF-IDF 벡터라이저로 계량 가중치 분석한 차트입니다. AI, 인공지능, 생성형 키워드가 압도적인 가중치를 점유합니다.",
            "notes": "우측에 보이는 막대그래프는 도서 제목과 상세 설명문에서 추출한 단어들의 수학적 가중치인 TF-IDF 연산 결과입니다. 형태소 분석기 없이 텍스트 전처리 기법을 응용하여 단어를 추출한 결과, `ai`, `인공지능`, `생성형` 키워드가 가중치 통합 약 **0.1412**의 독보적인 지수를 차지하며 1위를 차지했습니다. 그 뒤를 이어 `데이터`(0.0274), `챗gpt`(0.0192), `실전`, `코딩`, `활용` 등이 차례로 유의미한 수치를 획득하고 있습니다. 이는 최근 IT 출판 기획 트렌드가 단순히 정통 알고리즘이나 기본 웹 개발 기술을 다루던 과거의 지형에서 탈피하여, 생성형 AI의 비즈니스적 응용과 LLM 코딩 활용 자동화 분야로 완전히 패러다임이 시프트되었음을 통계학적으로 입증합니다. 다음 장에서 키워드 융합 전략을 짚어보겠습니다."
        },
        # 27. TF-IDF 키워드 인사이트
        {
            "type": "infographic_cards",
            "title": "신기술 트렌드 결합 기획 및 검색 노출 강화",
            "cards": [
                {"title": "AI 패러다임 독점", "body": "TF-IDF 분석 결과 'AI', '인공지능', '챗GPT' 등이 시장의 흐름과 기획 의사결정을 독점적으로 견인하고 있습니다.", "icon": "🤖"},
                {"title": "융합 도서 기획 가치", "body": "자바, C# 등 기본 언어 문법서 단독 기획을 피해 'AI 프롬프트를 결합한 코딩 학습' 등 융합 기획을 시도해야 합니다.", "icon": "🧬"},
                {"title": "메타 키워드 SEO 최적화", "body": "상세설명 등록 시 '실전', '실무', '자동화' 등 유입량이 많은 고가중치 단어를 의도적으로 매핑해 노출을 올려야 합니다.", "icon": "🌐"}
            ],
            "notes": "TF-IDF 텍스트 키워드 가중치 분석에 근거한 검색 유입 최적화(SEO) 및 기획 방향성입니다. 독자들은 단순히 기술의 스펙시트를 단순 나열한 책에는 눈길을 주지 않습니다. 실무에서 내가 챗GPT를 어떻게 끌어와서 나의 '코딩' 생산성을 높일 수 있는지, 어떻게 '실전'에서 '활용'하여 '업무 자동화'를 이룰 수 있는지를 다룬 책을 찾아 다닙니다. 출판 기획 부서는 신간 등록 시 도서 상세 정보와 해설에 '실무 자동화', '생성형 AI API', '실습 프로젝트' 등 검색 엔진 노출 점수가 높은 고가중치 타겟 키워드들을 자연스러운 흐름 속에 최대한 삽입해 주어야 합니다. 이를 통해 서점 검색 로봇이 우리 책을 베스트 매칭 도서로 우선 판단하여 상단 노출 빈도를 극대화할 수 있습니다."
        },
        # 28. 세션 3 간지
        {
            "type": "divider",
            "title": "Session III",
            "subtitle": "종합 결론 및 비즈니스 제언",
            "desc": "IT 도서 시장 지배력 강화를 위한 3대 핵심 액션 플랜",
            "notes": "프레젠테이션의 마지막 대주제인 종합 결론 및 비즈니스 제언 파트입니다. 앞서 보신 데이터 프로파일링 결과와 10가지 주요 시각화 차트를 통해, 우리는 도서 가격의 독립성, 도서정가제에 따른 가격 메리트 한계, 인기도와 리뷰 평판의 극심한 양극화 쏠림 현상, 그리고 AI와 실무 키워드가 지배하는 IT 기술 도서 시장의 지형을 명확하게 팩트 기반으로 파헤쳤습니다. 이제 이 팩트를 우리 조직의 실제 무기로 연동하여, 경쟁사 대비 독보적인 시장 점유율을 쟁취할 수 있도록 출판 기획, 도서 단가 설정, 마케팅 프로모션 단계로 나눈 3대 핵심 액션 플랜을 제시하고자 합니다. 다음 슬라이드로 이동해 첫 번째 플랜을 확인하겠습니다."
        },
        # 29. 제언 1: 빠른 교체 주기 대응
        {
            "type": "infographic_grid",
            "title": "최신 신간 중심의 빠른 교체 주기 대응",
            "left_text": "신간 발행의 80% 이상이 최근 3개년에 집중되는 현상은 IT 도서의 반감기가 극도로 짧아졌음을 보여줍니다. 기획 속도를 혁신하고 마케팅 집중도를 재배정해야 합니다.",
            "right_cards": [
                {"label": "애자일 기획", "val": "원고 계약부터 인쇄 배포까지 6개월 내 완료", "icon": "⏱️"},
                {"label": "홍보 예산 집중", "val": "출간 후 초기 3개월 이내에 마케팅비 80% 소진", "icon": "💰"},
                {"label": "개정판 선계약", "val": "신기술 릴리즈 일정에 연동한 개정 캘린더 상시화", "icon": "🔄"}
            ],
            "notes": "첫 번째 비즈니스 액션 플랜은 신간의 짧아진 라이프사이클에 대처하는 '애자일 기획 및 예산 집중 정책'입니다. IT 책은 기술 버전업에 따라 수명이 극도로 짧아집니다. 기획 부서는 기획부터 최종 출간까지 질질 끌며 1년 넘게 걸리는 옛날식 편집 프로세스를 전면 타파하고, 6개월 이내에 초고속으로 초판을 밀어내는 조직 민첩성을 확보해야 합니다. 또한, 마케팅 예산 역시 연간 균등 분할 집행하는 방식을 멈추고, 도서 출간 직후 3개월 골든타임 이내에 전체 광고 홍보 예산의 80% 이상을 일시에 털어 넣어 판매 모멘텀을 수직 상승시켜야만 한정된 생애 주기 안에서 최대 마진을 확보할 수 있습니다."
        },
        # 30. 제언 2: AI 키워드 융합
        {
            "type": "infographic_cards",
            "title": "킬러 키워드(AI/생성형)의 적절한 활용",
            "cards": [
                {"title": "크로스 오버 기획", "body": "전통적인 프로그래밍 기초서 기획을 지양하고 AI 개발 프로세스나 생성형 AI 애플리케이션 개발과의 크로스 기획을 시도합니다.", "icon": "🧩"},
                {"title": "실무 중심의 가치 지향", "body": "단순 이론 나열을 배제하고 실전, 실습, 업무 자동화 등 독자가 직관적으로 체감 가능한 가치를 제목에 담습니다.", "icon": "📈"},
                {"title": "SEO 메타데이터 설계", "body": "서점 상세 설명 등록 시 TF-IDF 가중치가 입증된 고노출 단어를 자연스럽게 삽입해 오가닉 검색 유입을 극대화합니다.", "icon": "⚙️"}
            ],
            "notes": "두 번째 액션 플랜은 텍스트 마이닝 가중치가 입증한 'AI 기술 결합 기획 및 검색 노출의 과학화'입니다. 이제 IT 도서 시장에서 인공지능과 생성형 기술은 단순한 하나의 카테고리가 아니라 모든 IT 도서의 필수 탑재 양념입니다. 예를 들어 자바 웹 개발 입문서를 낸다면, 평범한 책 제목을 피하고 'AI 비서를 활용해 코딩 시간을 반으로 줄이는 자바 실무 가이드'와 같이 킬러 키워드를 융합해 기획해야 승산이 있습니다. 또한 상세페이지 작성 시 인공지능, 챗GPT, 실전, 자동화 등의 검색 유입 고점 키워드들을 기입하여 온라인 서점 검색 엔진 최적화(SEO) 마케팅 전략을 정밀하게 가이드라인화해야 합니다."
        },
        # 31. 제언 3: 평판 선순환 루프
        {
            "type": "infographic_grid",
            "title": "마케팅 채널의 양극화 극복 (Social Proof)",
            "left_text": "판매와 리뷰의 뚜렷한 양의 상관성(0.36)은 초기 평판이 베스트셀러 등극의 방아쇠가 됨을 시사합니다. 인위적인 평판 인프라를 빠르게 쌓아 올리십시오.",
            "right_cards": [
                {"label": "초기 타겟 리뷰 수", "val": "출간 후 4주 이내 최소 30개 평점 등록", "icon": "💬"},
                {"label": "베타리더십 체계", "val": "인쇄 전 사전 PDF 공유를 통한 대량 서평 예약", "icon": "👥"},
                {"label": "상시 리워드 가이드", "val": "고품질 기술 리뷰 작성 시 기프티콘 자동 지급", "icon": "🏆"}
            ],
            "notes": "세 번째 액션 플랜은 인기도의 양극화 늪을 뚫고 지나가기 위한 '평판 선순환 모멘텀 확보' 전략입니다. 소비자의 구매 확신을 자극하는 Social Proof, 즉 사회적 증거인 독자 기술 리뷰 30개를 출간 후 단 한 달 이내에 무조건 완성해야 합니다. 이를 위해 도서가 실재 인쇄 공장에 들어가기 전, 예비 독자 커뮤니티나 기술 스터디 그룹원 30명에게 교정본 PDF를 무료로 배포하고, 출시일에 맞춰 정성 서평을 등록하도록 약속을 맺는 '베타 리더십 파이프라인'을 상시 구동하십시오. 이 초기 30개의 안전장치가 구비되어 있어야만 신규 독자가 상세페이지에 들어왔을 때 이탈하지 않고 실질 구매로 이어지는 고효율 선순환 고리가 작동하게 됩니다."
        },
        # 32. 맺음말 및 Q&A
        {
            "type": "cover",
            "title": "Q&A 및 맺음말",
            "subtitle": "경청해 주셔서 감사합니다.",
            "meta": "의문 사항이나 보완이 필요한 내용이 있다면 언제든 편하게 질문해 주십시오.",
            "notes": "이것으로 YES24 1,200건의 IT 도서 데이터를 기반으로 수행한 탐색적 데이터 분석 결과 및 이를 뒷받침하는 비즈니스 의사결정 3대 액션 플랜 브리핑을 모두 마치겠습니다. 오늘 보고해 드린 내용처럼, IT 도서 유통 시장은 지식 반감기가 극단적으로 짧고, AI와 실무 키워드가 기획의 성공률을 지배하며, 가격 그 자체보다는 초반 평판 리뷰 확보가 최종 흥행의 성패를 갈라놓는 뚜렷한 데이터 증거를 보여주고 있습니다. 저희 기획본부와 마케팅 부서가 오늘 제시된 데이터 기반 의사결정 모델을 적극 수렴하고 실행에 옮긴다면, 향후 출판 포트폴리오의 안전성과 마진 구조를 한층 더 탄탄하게 구축할 수 있으리라 믿어 의심치 않습니다. 발표 내용이나 슬라이드의 통계 연산 기준에 관해 질문이 있으신 분들은 질문해 주시기 바랍니다. 친절히 답변해 드리겠습니다. 경청해 주셔서 대단히 감사합니다."
        }
    ]
    
    # 딕셔너리 루프를 돌면서 슬라이드 한 장씩 생성
    for idx, slide_info in enumerate(slides_data):
        slide_layout = prs.slide_layouts[6] # 빈 슬라이드 레이아웃 사용 (전체 컨트롤을 위해)
        slide = prs.slides.add_slide(slide_layout)
        
        # 1) 발표자 슬라이드 노트 주입
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = slide_info.get("notes", "")
        
        # 2) 타입별 렌더링
        stype = slide_info["type"]
        
        if stype == "cover":
            # 흰색 배경 설정
            apply_solid_background(slide, COLOR_BG_WHITE)
            
            # 뒤쪽에 브루탈리즘 대형 사각형 데코레이션 섀도우 배치
            add_brutal_card(slide, Inches(0.7), Inches(0.8), Inches(11.933), Inches(5.9), fill_color=COLOR_BRUTAL_YELLOW)
            
            # 메인 타이틀 텍스트 박스
            title_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.933), Inches(4.5))
            tf = title_box.text_frame
            tf.word_wrap = True
            
            p = tf.paragraphs[0]
            p.text = slide_info["title"]
            p.alignment = PP_ALIGN.CENTER
            format_text_run(p.runs[0], FONT_TITLE, 40, bold=True, color_rgb=COLOR_BLACK)
            
            p2 = tf.add_paragraph()
            p2.text = slide_info["subtitle"]
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(20)
            format_text_run(p2.runs[0], FONT_BODY, 18, bold=True, color_rgb=COLOR_BLACK)
            
            p3 = tf.add_paragraph()
            p3.text = slide_info["meta"]
            p3.alignment = PP_ALIGN.CENTER
            p3.space_before = Pt(50)
            format_text_run(p3.runs[0], FONT_BODY, 13, bold=False, color_rgb=COLOR_BLACK)
            
        elif stype == "toc":
            # 순수 화이트 배경
            apply_solid_background(slide, COLOR_BG_WHITE)
            add_title(slide, slide_info["title"])
            
            # 목차 리스트용 네오브루탈리즘 카드 배치
            for s_idx, sec in enumerate(slide_info["sections"]):
                top_pos = Inches(1.8 + s_idx * 1.7)
                
                # 좌측 아이콘용 브루탈 서클 (두꺼운 검은 테두리와 섀도우)
                # 서클용 그림자
                sh_circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, Inches(1.0 + 0.05), top_pos + Inches(0.05), Inches(1.2), Inches(1.2)
                )
                sh_circle.fill.solid()
                sh_circle.fill.fore_color.rgb = COLOR_BLACK
                sh_circle.line.fill.background()
                
                # 서클 본체
                circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, Inches(1.0), top_pos, Inches(1.2), Inches(1.2)
                )
                circle.fill.solid()
                circle.fill.fore_color.rgb = COLOR_BRUTAL_LIME
                circle.line.color.rgb = COLOR_BLACK
                circle.line.width = Pt(2.5)
                
                c_tf = circle.text_frame
                c_p = c_tf.paragraphs[0]
                c_p.text = sec["icon"] # 이모지 아이콘 적용
                c_p.alignment = PP_ALIGN.CENTER
                format_text_run(c_p.runs[0], FONT_TITLE, 24, bold=True, color_rgb=COLOR_BLACK)
                
                # 우측 텍스트 카드 상자 (둥근 사각형 대신 플랫한 직각 사각형에 검은 테두리 및 섀도우 적용)
                add_brutal_card(slide, Inches(2.5), top_pos, Inches(9.8), Inches(1.2), fill_color=COLOR_BG_WHITE)
                
                # 텍스트 오버레이를 위한 임시 투명 텍스트 상자 배치
                card_box = slide.shapes.add_textbox(Inches(2.5), top_pos, Inches(9.8), Inches(1.2))
                card_tf = card_box.text_frame
                card_tf.word_wrap = True
                card_tf.margin_left = Inches(0.3)
                card_tf.margin_top = Inches(0.2)
                
                p_name = card_tf.paragraphs[0]
                p_name.text = sec["name"]
                format_text_run(p_name.runs[0], FONT_TITLE, 18, bold=True, color_rgb=COLOR_BLACK)
                
                p_desc = card_tf.add_paragraph()
                p_desc.text = sec["desc"]
                p_desc.space_before = Pt(5)
                format_text_run(p_desc.runs[0], FONT_BODY, 13, bold=False, color_rgb=COLOR_BLACK)
                
        elif stype == "divider":
            # 옐로우 배경 (네오브루탈리즘 테마)
            apply_solid_background(slide, COLOR_BRUTAL_YELLOW)
            
            # 외곽 굵은 테두리 프레임
            frame = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), Inches(12.333), Inches(6.5)
            )
            frame.fill.solid()
            frame.fill.fore_color.rgb = COLOR_BRUTAL_YELLOW
            frame.line.color.rgb = COLOR_BLACK
            frame.line.width = Pt(4.0)
            
            # 중앙 오프닝 세션 설명
            div_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
            tf = div_box.text_frame
            tf.word_wrap = True
            
            p = tf.paragraphs[0]
            p.text = slide_info["title"]
            p.alignment = PP_ALIGN.CENTER
            format_text_run(p.runs[0], FONT_TITLE, 26, bold=True, color_rgb=COLOR_BLACK)
            
            # 텍스트에 하이라이트 효과 (네온 라임 박스로 감싸기)
            p2 = tf.add_paragraph()
            p2.text = slide_info["subtitle"]
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(15)
            format_text_run(p2.runs[0], FONT_TITLE, 36, bold=True, color_rgb=COLOR_BLACK)
            
            p3 = tf.add_paragraph()
            p3.text = slide_info["desc"]
            p3.alignment = PP_ALIGN.CENTER
            p3.space_before = Pt(25)
            format_text_run(p3.runs[0], FONT_BODY, 16, bold=True, color_rgb=COLOR_BLACK)
            
        elif stype == "infographic_cards":
            # 순수 화이트 배경
            apply_solid_background(slide, COLOR_BG_WHITE)
            add_title(slide, slide_info["title"])
            
            # 가로 3개 배치형 네오브루탈리즘 카드
            card_width = Inches(3.6)
            card_height = Inches(4.5)
            gap = Inches(0.4)
            left_start = Inches(0.7)
            top_pos = Inches(1.8)
            
            for c_idx, card_data in enumerate(slide_info["cards"]):
                x_pos = left_start + c_idx * (card_width + gap)
                
                # 하드 섀도우 카드 생성
                add_brutal_card(slide, x_pos, top_pos, card_width, card_height, fill_color=COLOR_BG_WHITE)
                
                # 카드 내부 상단 동그라미 아이콘 (테두리와 섀도우)
                sh_circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, x_pos + Inches(0.3 + 0.05), top_pos + Inches(0.3 + Inches(0.05)), Inches(0.9), Inches(0.9)
                )
                sh_circle.fill.solid()
                sh_circle.fill.fore_color.rgb = COLOR_BLACK
                sh_circle.line.fill.background()
                
                icon_circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, x_pos + Inches(0.3), top_pos + Inches(0.3), Inches(0.9), Inches(0.9)
                )
                icon_circle.fill.solid()
                icon_circle.fill.fore_color.rgb = COLOR_BRUTAL_YELLOW if c_idx % 2 == 0 else COLOR_BRUTAL_LIME
                icon_circle.line.color.rgb = COLOR_BLACK
                icon_circle.line.width = Pt(2.0)
                
                i_tf = icon_circle.text_frame
                i_p = i_tf.paragraphs[0]
                i_p.text = card_data["icon"]
                i_p.alignment = PP_ALIGN.CENTER
                format_text_run(i_p.runs[0], FONT_BODY, 18, bold=True, color_rgb=COLOR_BLACK)
                
                # 내부 텍스트 프레임 설정을 위한 텍스트 박스 추가
                tbox = slide.shapes.add_textbox(x_pos, top_pos, card_width, card_height)
                tf = tbox.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(0.3)
                tf.margin_right = Inches(0.3)
                tf.margin_top = Inches(1.4)
                
                p_title = tf.paragraphs[0]
                p_title.text = card_data["title"]
                format_text_run(p_title.runs[0], FONT_TITLE, 18, bold=True, color_rgb=COLOR_BLACK)
                
                p_body = tf.add_paragraph()
                p_body.text = card_data["body"]
                p_body.space_before = Pt(15)
                format_text_run(p_body.runs[0], FONT_BODY, 13, bold=False, color_rgb=COLOR_BLACK)
                
        elif stype == "infographic_grid":
            # 순수 화이트 배경
            apply_solid_background(slide, COLOR_BG_WHITE)
            add_title(slide, slide_info["title"])
            
            # 좌: 대형 설명 카드
            add_brutal_card(slide, Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.8), fill_color=COLOR_BG_WHITE)
            
            l_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(5.5), Inches(4.8))
            l_tf = l_box.text_frame
            l_tf.word_wrap = True
            l_tf.margin_left = Inches(0.4)
            l_tf.margin_right = Inches(0.4)
            l_tf.margin_top = Inches(0.5)
            
            p_desc = l_tf.paragraphs[0]
            p_desc.text = slide_info["left_text"]
            format_text_run(p_desc.runs[0], FONT_BODY, 16, bold=False, color_rgb=COLOR_BLACK)
            
            # 우측 수직 카드 목록 배치
            right_width = Inches(5.9)
            right_height = Inches(1.3)
            right_gap = Inches(0.45)
            right_left = Inches(6.7)
            right_top_start = Inches(1.8)
            
            for r_idx, r_card in enumerate(slide_info["right_cards"]):
                r_top = right_top_start + r_idx * (right_height + right_gap)
                
                # 수직 목록 카드 생성 (하드 섀도우)
                add_brutal_card(slide, right_left, r_top, right_width, right_height, fill_color=COLOR_BG_WHITE)
                
                # 좌측 세이지 대신 시그널 레드의 두꺼운 브루탈 세로 바 배치
                bar = slide.shapes.add_shape(
                    MSO_SHAPE.RECTANGLE, right_left, r_top, Inches(0.25), right_height
                )
                bar.fill.solid()
                bar.fill.fore_color.rgb = COLOR_BRUTAL_RED
                bar.line.color.rgb = COLOR_BLACK
                bar.line.width = Pt(2.0)
                
                # 우측 상단 플랫 아이콘 배치 (그림자 포함)
                sh_circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, right_left + Inches(0.4 + 0.04), r_top + Inches(0.2 + 0.04), Inches(0.9), Inches(0.9)
                )
                sh_circle.fill.solid()
                sh_circle.fill.fore_color.rgb = COLOR_BLACK
                sh_circle.line.fill.background()
                
                icon_circle = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL, right_left + Inches(0.4), r_top + Inches(0.2), Inches(0.9), Inches(0.9)
                )
                icon_circle.fill.solid()
                icon_circle.fill.fore_color.rgb = COLOR_BRUTAL_YELLOW
                icon_circle.line.color.rgb = COLOR_BLACK
                icon_circle.line.width = Pt(2.0)
                
                i_tf = icon_circle.text_frame
                i_p = i_tf.paragraphs[0]
                i_p.text = r_card["icon"]
                i_p.alignment = PP_ALIGN.CENTER
                format_text_run(i_p.runs[0], FONT_BODY, 18, bold=True, color_rgb=COLOR_BLACK)
                
                tbox = slide.shapes.add_textbox(right_left, r_top, right_width, right_height)
                tf = tbox.text_frame
                tf.word_wrap = True
                tf.margin_left = Inches(1.5)
                tf.margin_top = Inches(0.2)
                
                p_label = tf.paragraphs[0]
                p_label.text = r_card["label"]
                format_text_run(p_label.runs[0], FONT_BODY, 12, bold=True, color_rgb=COLOR_BLACK)
                
                p_val = tf.add_paragraph()
                p_val.text = r_card["val"]
                p_val.space_before = Pt(5)
                format_text_run(p_val.runs[0], FONT_TITLE, 20, bold=True, color_rgb=COLOR_BLACK)
                
        elif stype == "image_layout":
            # 순수 화이트 배경
            apply_solid_background(slide, COLOR_BG_WHITE)
            add_title(slide, slide_info["title"])
            
            # 좌측 55% 텍스트 설명 카드
            add_brutal_card(slide, Inches(0.7), Inches(1.8), Inches(6.0), Inches(4.8), fill_color=COLOR_BG_WHITE)
            
            tbox = slide.shapes.add_textbox(Inches(0.7), Inches(1.8), Inches(6.0), Inches(4.8))
            tf = tbox.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.4)
            tf.margin_right = Inches(0.4)
            tf.margin_top = Inches(0.5)
            
            # 상단 동그라미 플랫 아이콘 배치 (그림자 포함)
            sh_circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(1.1 + 0.04), Inches(2.2 + 0.04), Inches(0.9), Inches(0.9)
            )
            sh_circle.fill.solid()
            sh_circle.fill.fore_color.rgb = COLOR_BLACK
            sh_circle.line.fill.background()
            
            icon_circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(1.1), Inches(2.2), Inches(0.9), Inches(0.9)
            )
            icon_circle.fill.solid()
            icon_circle.fill.fore_color.rgb = COLOR_BRUTAL_LIME
            icon_circle.line.color.rgb = COLOR_BLACK
            icon_circle.line.width = Pt(2.0)
            
            i_tf = icon_circle.text_frame
            i_p = i_tf.paragraphs[0]
            i_p.text = "📊"
            i_p.alignment = PP_ALIGN.CENTER
            format_text_run(i_p.runs[0], FONT_BODY, 18, bold=True, color_rgb=COLOR_BLACK)
            
            p_header = tf.paragraphs[0]
            p_header.text = "        주요 데이터 분석 결과"
            format_text_run(p_header.runs[0], FONT_TITLE, 18, bold=True, color_rgb=COLOR_BLACK)
            
            p_desc = tf.add_paragraph()
            p_desc.text = slide_info["desc"]
            p_desc.space_before = Pt(35)
            format_text_run(p_desc.runs[0], FONT_BODY, 15, bold=False, color_rgb=COLOR_BLACK)
            
            # 우측 45% 차트 이미지 삽입 (테두리 두껍게 감싸기)
            img_name = slide_info["image"]
            img_path = os.path.join(IMAGES_DIR, img_name)
            
            # 우측 차트 이미지를 담을 액자형 하드 섀도우 보드 생성
            add_brutal_card(slide, Inches(7.1), Inches(1.8), Inches(5.5), Inches(4.8), fill_color=COLOR_BG_WHITE)
            
            if os.path.exists(img_path):
                # 이미지가 겹치지 않게 테두리 프레임 안쪽으로 정밀 정렬
                slide.shapes.add_picture(
                    img_path, Inches(7.2), Inches(1.9), width=Inches(5.3), height=Inches(4.6)
                )
            else:
                err_box = slide.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.5), Inches(4.8))
                err_tf = err_box.text_frame
                err_p = err_tf.paragraphs[0]
                err_p.text = "[차트 이미지 누락: {}]".format(img_name)
                err_p.alignment = PP_ALIGN.CENTER
                format_text_run(err_p.runs[0], FONT_BODY, 14, bold=True, color_rgb=COLOR_BLACK)

    # 파워포인트 빌드 및 저장
    output_path = "yes24/docs/eda_report_presentation.pptx"
    prs.save(output_path)
    print("★ [SUCCESS] 파워포인트 파일이 정상적으로 빌드되었습니다: {}".format(output_path))

if __name__ == "__main__":
    create_presentation()
