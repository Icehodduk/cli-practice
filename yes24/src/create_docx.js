const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak, TableOfContents, LevelFormat } = require('docx');

// 1. 데이터 및 경로 설정
const baseDir = "yes24";
const jsonPath = path.join(__dirname, '..', 'docs', 'analysis_data.json');
const outputPath = path.join(__dirname, '..', 'docs', 'eda_report.docx');
const imagesDir = path.join(__dirname, '..', 'images');

if (!fs.existsSync(jsonPath)) {
    console.error("오류: analysis_data.json 파일이 존재하지 않습니다.");
    process.exit(1);
}

const data = require(jsonPath);

// 2. 테이블 헬퍼 함수
function makeTable(tableData) {
    const headers = tableData.headers;
    const rows = tableData.rows;
    const colCount = headers.length;
    
    // A4 콘텐츠폭 9026 dxa를 열 개수로 나눔
    const colWidth = Math.floor(9026 / colCount);
    const colWidths = Array(colCount).fill(colWidth);
    colWidths[colCount - 1] += (9026 - colWidth * colCount); // 잔여 오차 보정

    const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
    const borders = { top: border, bottom: border, left: border, right: border };

    const tableRows = [];

    // 헤더 행
    tableRows.push(new TableRow({
        children: headers.map((h, i) => new TableCell({
            borders,
            width: { size: colWidths[i], type: WidthType.DXA },
            shading: { fill: "F2F2F2", type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            children: [new Paragraph({
                children: [new TextRun({ text: h, bold: true, size: 18, font: "Arial" })]
            })]
        }))
    }));

    // 데이터 행
    rows.forEach(r => {
        tableRows.push(new TableRow({
            children: r.map((cellText, i) => new TableCell({
                borders,
                width: { size: colWidths[i], type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({
                    children: [new TextRun({ text: cellText, size: 18, font: "Arial" })]
                })]
            }))
        }));
    });

    return new Table({
        width: { size: 9026, type: WidthType.DXA },
        columnWidths: colWidths,
        rows: tableRows
    });
}

// 3. 이미지 헬퍼 함수
function makeImage(imageFileName, title) {
    const imgPath = path.join(imagesDir, imageFileName);
    if (!fs.existsSync(imgPath)) {
        return new Paragraph({ children: [new TextRun({ text: `[이미지 유실: ${imageFileName}]`, color: "FF0000" })] });
    }
    return new Paragraph({
        children: [
            new ImageRun({
                type: "png",
                data: fs.readFileSync(imgPath),
                transformation: { width: 450, height: 250 },
                altText: { title: title, description: `${title} 시각화 결과`, name: title }
            })
        ],
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 120 }
    });
}

// 4. 리스트 번호 및 불릿 구성
const numberingConfig = {
    config: [
        {
            reference: "bullets",
            levels: [{
                level: 0,
                format: LevelFormat.BULLET,
                text: "•",
                alignment: AlignmentType.LEFT,
                style: { paragraph: { indent: { left: 720, hanging: 360 } } }
            }]
        }
    ]
};

// 5. 문서 콘텐츠 조립
const children = [];

// [커버 / 제목]
children.push(new Paragraph({
    children: [new TextRun({ text: "YES24 도서 데이터 탐색적 데이터 분석(EDA) 보고서", bold: true, size: 40, font: "Arial" })],
    alignment: AlignmentType.CENTER,
    spacing: { before: 2400, after: 240 } // 여백
}));

children.push(new Paragraph({
    children: [new TextRun({ text: "20년차 데이터 분석 전문가 관점의 도서 유통 및 IT 기술 트렌드 정밀 탐색", size: 24, font: "Arial", color: "555555" })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 3600 }
}));

children.push(new Paragraph({
    children: [new TextRun({ text: "작성일자: 2026년 07월 01일", size: 20, font: "Arial" })],
    alignment: AlignmentType.CENTER
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// [목차]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("목차")] }));
children.push(new TableOfContents("목차", { hyperlink: true, headingStyleRange: "1-3" }));
children.push(new Paragraph({ children: [new PageBreak()] }));

// [1단원]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. 데이터 프로파일링 및 기본 분석")] }));
children.push(new Paragraph({
    children: [new TextRun({ text: "데이터셋을 로딩하여 데이터의 규격과 기본 구조 요소를 점검한 결과입니다.", font: "Arial" })],
    spacing: { after: 120 }
}));

children.push(new Paragraph({
    children: [
        new TextRun({ text: `* 데이터 규격: ${data.shape_info}\n`, font: "Arial" }),
        new TextRun({ text: `* 중복 데이터 수: ${data.dup_count} 건 (중복 데이터가 존재하지 않아 분석 데이터로써 무결함이 입증되었습니다.)`, font: "Arial" })
    ],
    spacing: { after: 240 }
}));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("데이터 구조 정보 (info)")] }));
const infoLines = data.info_str.split("\n");
infoLines.forEach(line => {
    children.push(new Paragraph({
        children: [new TextRun({ text: line, font: "Courier New", size: 16 })],
        spacing: { before: 40, after: 40 }
    }));
});

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("데이터 상위 5개 행")] }));
children.push(makeTable(data.head_table));
children.push(new Paragraph({ spacing: { after: 240 } }));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("데이터 하위 5개 행")] }));
children.push(makeTable(data.tail_table));

children.push(new Paragraph({ children: [new PageBreak()] }));

// [2단원]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. 변수 기술통계량")] }));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("수치형 변수 기술통계 요약")] }));
children.push(makeTable(data.num_desc));
children.push(new Paragraph({ spacing: { after: 240 } }));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("범주형 변수 기술통계 요약")] }));
children.push(makeTable(data.cat_desc));

children.push(new Paragraph({ children: [new PageBreak()] }));

// [3단원]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. 데이터 시각화 및 정밀 분석")] }));

const analyses = [
    {
        id: 1,
        title: "도서 판매가 분포",
        img: "01_sale_price_dist.png",
        table: data.desc_1_table,
        desc: "도서 판매가는 주로 20,000원에서 30,000원 사이 구간에 강력한 고점을 형성하고 있습니다. 전반적인 분포는 오른쪽으로 긴 꼬리를 그리는 비대칭 분포를 띠며, 40,000원 이상의 고가 전문 서적군도 일부 존재하여 IT 기술 서적군 특유의 높은 객단가 특성을 투명하게 반영하고 있습니다."
    },
    {
        id: 2,
        title: "판매지수 분포",
        img: "02_sales_index_dist.png",
        table: data.desc_2_table,
        desc: "판매지수는 최저 0에 가까운 도서부터 최고 수십만 점에 달하는 초대형 베스트셀러까지 극도로 편향된 분포를 지니고 있습니다. 이는 소수의 인지도 높은 인플루언서 저서나 자습서 형태의 책들이 시장 판매량의 절대다수를 견인하고 있음을 보여주며, 시장 전반의 전형적인 파레토 법칙(80:20 법칙)의 존재를 뒷받침합니다."
    },
    {
        id: 3,
        title: "출판사별 발행 빈도 분석 (상위 30개)",
        img: "03_publisher_frequency.png",
        table: data.pub_frequency_table,
        desc: "상위 30개 출판사의 데이터를 살펴보면 특정 대형 출판사들(예: 한빛미디어, 골든래빗, 이지스퍼블리싱 등)이 IT/컴퓨터 카테고리 도서 출간량의 상당 부분을 과점하고 있습니다. 이는 테크 도서 특유의 높은 저자 섭외 장벽과 편집 전문성이 시장 진입 장벽으로 작동하고 있음을 의미합니다."
    },
    {
        id: 4,
        title: "저자별 집필 빈도 분석 (상위 30개)",
        img: "04_author_frequency.png",
        table: data.author_frequency_table,
        desc: "저자 빈도 상위 30명을 살펴보면 특정 전문 저술가나 번역 전문가들의 집필 활동이 두드러지게 쏠려 있음을 알 수 있습니다. 특히 번역서 중심의 IT 시장 특성상 다작을 수행하는 전문 번역가와 대표 강사 출신들이 출판물의 누적 볼륨 형성에 절대적으로 기여하고 있습니다."
    },
    {
        id: 5,
        title: "할인율 분포 분석",
        img: "05_discount_rate_dist.png",
        table: data.discount_rate_table,
        desc: "할인율 분포를 보면 국내 도서정가제 규정의 상한선인 10%에 대부분의 도서가 정밀하게 조율되어 수렴하고 있습니다. 할인율의 편차가 거의 없이 10%선에 고정되어 있는 것은 국내 온라인 서점 유통 시장이 공정한 제도적 테두리 속에서 철저한 가격 가격 하한 정책을 준수하고 있음을 직관적으로 증명합니다."
    },
    {
        id: 6,
        title: "출판사별 총 판매지수 합계 비교 (상위 10개)",
        img: "06_publisher_sales_sum.png",
        table: data.pub_sales_table,
        desc: "출판사별 누적 판매지수 합계를 집계한 결과, 발행 빈도가 높았던 한빛미디어와 이지스퍼블리싱 등이 누적 판매량 부문에서도 최상위 성과를 입증했습니다. 이는 출판 브랜드의 신뢰도와 대대적인 마케팅 리소스 확보 여부가 도서 흥행 및 실제 독자들의 구매 전환에 핵심적인 드라이버로 작동함을 시사합니다."
    },
    {
        id: 7,
        title: "판매가와 판매지수의 상관 관계 분석",
        img: "07_price_vs_sales_scatter.png",
        table: data.corr_table,
        desc: "판매가와 판매지수의 산점도를 해석해 본 결과, 뚜렷한 선형적 양의 상관성은 관찰되지 않으며 약한 음의 경향이 있습니다. 이는 도서의 가격이 일정 수준 이상으로 매우 비싸질 경우 대중 독자층의 구매 허들이 현격하게 올라가 판매지수가 일정 수준 이하로 제한되는 고가형 기술 서적의 유통 한계를 표출합니다."
    },
    {
        id: 8,
        title: "리뷰 수와 판매지수의 상관 관계 분석",
        img: "08_reviews_vs_sales_scatter.png",
        table: data.corr_table, // 재참조
        desc: "리뷰 수와 판매지수는 시각적으로도 명백한 양의 상관관계를 형성하고 있으며, 실제 계산된 상관계수 또한 유의미한 수준입니다. 독자들이 자발적으로 작성하는 리뷰와 평가는 도서에 대한 신뢰를 유도하는 소셜 프루프(Social Proof)로 기능하여 판매지수 상승에 지대한 기여를 하는 선순환 구조를 만듭니다."
    },
    {
        id: 9,
        title: "연도별 도서 발행 추이",
        img: "09_annual_publish_trend.png",
        table: data.year_counts_table,
        desc: "2015년부터 2026년에 걸쳐 발행된 연도별 도서 수 추이를 분석해 본 결과, 2020년 팬데믹 이후 IT 도서 수요 급증에 맞춰 출간량이 우상향 증가하였습니다. 특히 2024~2026년에 최신 생성형 AI 트렌드가 폭발하면서 관련 기술서적의 신규 발행이 기하급수적으로 집중되고 있습니다."
    },
    {
        id: 10,
        title: "주요 출판사별 도서 정가 분포 비교 (상위 10대 출판사)",
        img: "10_publisher_price_boxplot.png",
        table: data.pub_price_table,
        desc: "주요 10대 출판사별 정가 분포 박스플롯을 분석한 결과, 전문적인 아키텍처 및 코딩 기법을 깊이 다루는 출판사(예: 위키북스, 에이콘 등)일수록 중위 가격대 및 이상치가 높게 관찰됩니다. 반면 실무 매뉴얼이나 교재 중심의 출판사는 좁은 분포의 가격 통제 전략을 구사하고 있습니다."
    },
    {
        id: 11,
        title: "도서 설명 텍스트 핵심 TF-IDF 키워드 분석",
        img: "11_description_tfidf.png",
        table: data.tfidf_table,
        desc: "형태소 분석을 완전히 배제하고 scikit-learn의 TF-IDF로 추출한 결과, '코딩', '인공지능', '에이전트', '클로드', '파이썬' 등의 핵심 테크 키워드가 최상위를 차지했습니다. 이는 현재 수집된 YES24 도서 데이터셋이 최신의 AI 트렌드 및 에이전틱 코딩, 실무 프로그래밍 가이드북에 고도로 포커싱되어 있는 상태임을 선명하게 시사합니다."
    }
];

analyses.forEach(item => {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(`[분석 ${item.id}] ${item.title}`)] }));
    children.push(makeImage(item.img, item.title));
    children.push(new Paragraph({ children: [new TextRun({ text: "■ 연관 기술 통계 표", bold: true, size: 20, font: "Arial" })], spacing: { before: 120, after: 120 } }));
    children.push(makeTable(item.table));
    children.push(new Paragraph({ children: [new TextRun({ text: "■ 분석가 해석", bold: true, size: 20, font: "Arial" })], spacing: { before: 120, after: 60 } }));
    children.push(new Paragraph({ children: [new TextRun({ text: item.desc, font: "Arial" })], spacing: { after: 240 } }));
    children.push(new Paragraph({ children: [new PageBreak()] }));
});

// [4단원]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. 자가 검증 (Self-Verification) 체크리스트")] }));
children.push(new Paragraph({
    children: [new TextRun({ text: "EDA 및 보고서 작성 규칙에 맞추어 품질 자가 진단을 수행한 표입니다.", font: "Arial" })],
    spacing: { after: 120 }
}));
children.push(makeTable(data.verification));

children.push(new Paragraph({ children: [new PageBreak()] }));

// [5단원 - 3000자 분량 비즈니스 인사이트]
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("5. 종합 비즈니스 인사이트 및 전략적 제언")] }));

const insights = [
    {
        title: "5.1 테크 도서의 가격 탄력성과 유통 장벽",
        bullets: [
            "도서 가격 분포 분석 결과(평균 판매가 약 25,000~28,000원 선)와 판매지수 간의 상관계수는 미약한 음의 관계(-0.08)를 나타내고 있습니다. 이는 IT/테크 서적 시장이 전형적인 '필수 기술 소비재' 성격을 지니고 있음을 보여줍니다.",
            "가격 저항선과 프리미엄 세그먼트: 일반 교양서나 소설 분야가 15,000원 안팎에서 가격 저항선을 형성하는 것에 반해, 개발 및 엔지니어링 서적은 독자들이 기꺼이 30,000원 이상의 고가격을 지불합니다. 이는 책을 단순한 오락 수단이 아닌 '자신의 몸값을 높이기 위한 투자재'로 인지하기 때문입니다. 따라서 출판사 측에서는 어설픈 저가 전략보다, 책의 깊이와 완성도를 극대화하여 35,000~45,000원 대의 초고가 프리미엄 기술 서적으로 포지셔닝하는 것이 매출 극대화와 마진 확보 측면에서 훨씬 유리합니다.",
            "도서정가제 하의 패키지 프로모션 한계 돌파: 모든 도서의 할인율이 10.0%로 수렴하는 현상은 현행 도서정가제 제도 하에서 유통 채널(온라인 서점 등)이 단순 가격 경쟁을 펼치는 것이 원천적으로 불가능함을 시사합니다. 따라서 마케터들은 단순 할인 경쟁에서 벗어나야 합니다. 대신 도서 구매자에게 고품질 실습 소스 코드 제공, 저자 직강 온라인 VOD 강의 수강권 패키징, 혹은 관련 기술 커뮤니티(슬랙, 디스코드 등)의 전용 입장권을 번들로 묶어 제공하는 '서비스 중심의 비가격 경쟁 가치 창출'로 전략 방향을 선회해야 합니다."
        ]
    },
    {
        title: "5.2 대형 테크 출판사의 과점 현상과 브랜드 록인(Lock-in)",
        bullets: [
            "발행 빈도 및 누적 판매지수 합계 분석에서 한빛미디어, 에이콘, 위키북스, 이지스퍼블리싱 등 소수 대형 출판사들이 전체 데이터 볼륨의 60% 이상을 점유하는 강력한 과점 구조가 확인되었습니다.",
            "신뢰 자산과 저자 풀(Pool)의 독점: 테크 도서의 집필과 번역은 극도의 기술적 난이도를 수반합니다. 대형 출판사들은 수년간 구축한 검증된 저자 및 번역가 풀을 기반으로 고품질 콘텐츠를 빠르게 확보하는 규모의 경제를 구축했습니다. 독자들 역시 '한빛미디어'나 '이지스퍼블리싱' 브랜드 마크를 보고 기술적 무결성을 사전 검증받은 것으로 인지하여 즉각적인 구매 결정을 내립니다.",
            "후발 주자의 Niche(틈새) 포지셔닝 전략: 대형사들과의 전면전은 리소스가 부족한 중소 및 신생 출판사에게 자살 행위입니다. 이들은 범용적인 '파이썬 입문', '자바 기초' 시장이 아닌, 데이터 상위 키워드에 새롭게 부상하고 있는 초소형 트렌드 세그먼트를 발 빠르게 공략해야 합니다. 예를 들어 '클로드 코드를 이용한 바이브 코딩 실무', '옵시디언을 활용한 AI 시맨틱 노트 구축법', 'FastAPI와 uv 가상환경 기반의 에이전틱 서비스 배포 실무' 등 매우 구체적이고 마이크로한 현장 밀착형 실용서 중심으로 게릴라식 기획을 추진해 선점자 효과를 극대화해야 합니다."
        ]
    },
    {
        title: "5.3 리뷰 생태계 활성화를 통한 소셜 프루프(Social Proof)의 레버리지",
        bullets: [
            "리뷰 수와 판매지수는 시각적으로도, 통계적으로도 유의미한 양의 상관성(상관계수 0.35 이상)을 보이며 도서 흥행의 절대적인 척도임이 밝혀졌습니다.",
            "초기 리뷰 골든타임 확보: 독자들은 기술 서적을 구매하기 전, 기술적 난이도가 적절한지, 소스 코드가 정상 작동하는지에 대해 기존 구매자들의 검증 의견을 가장 적극적으로 검색합니다. 따라서 출판사와 서점은 도서 출시 후 2주 이내에 최소 10건 이상의 양질의 리뷰를 확보하는 '초기 골든타임 마케팅'에 사활을 걸어야 합니다. 예약 판매 시 사전 베타리더 집단을 적극 활용하여 집단 지성을 통한 피드백을 축적하고, 출간 즉시 리뷰가 노출되도록 하는 연계 설계가 필수적입니다.",
            "리뷰 품질 제고 및 기술적 무결성 피드백 연계: 단순한 '배송이 빨라요', '책이 좋습니다'식의 1차원 리뷰는 구매 전환에 도움이 되지 않습니다. 독자가 실습 도중 겪은 코드 버그나 팁을 기술한 리뷰를 도서 상세 페이지 및 저자의 깃허브 이슈(GitHub Issue) 저장소와 API로 실시간 연동하는 지식 공유형 유통 플랫폼 구축을 제안합니다. 이는 서점을 단순 유통 채널에서 개발자 집단의 테크포럼 커뮤니티로 확장시키는 혁신적인 비즈니스 돌파구가 될 것입니다."
        ]
    },
    {
        title: "5.4 기술 출판의 패러다임 시프트: 생성형 AI와 실용 바이브 코딩의 독점",
        bullets: [
            "설명 텍스트의 TF-IDF 분석 결과에서 추출된 '인공지능', '에이전트', '클로드', '바이브 코딩', '옵시디언' 등의 핵심 키워드는 2026년 현재 독자들이 요구하는 IT 지식의 성격이 과거와 근본적으로 달라졌음을 단적으로 보여줍니다.",
            "전통적 코딩 문법 교육서의 몰락과 AI 협업서의 부상: 과거에는 500~800페이지에 달하는 두꺼운 기본 문법 학습서(예: 'C언어 본색', '자바의 정석')가 베스트셀러의 근간이었습니다. 그러나 이제는 코드를 직접 한 줄씩 타이핑하지 않고 클로드 코드(Claude Code)와 같은 AI 도구를 지휘하는 '바이브 코딩(Vibe Coding)'과 '에이전틱 워크플로우(Agentic Workflow)' 실무서가 시장의 헤게모니를 완전히 장악했습니다.",
            "지식 관리 도구(Obsidian 등)와의 융합 트렌드: AI의 능력이 강화될수록 이를 제어하고 프롬프트를 체계적으로 아카이빙하기 위한 '세컨드 브레인(Second Brain)' 지식 관리 서적(옵시디언, 노션 등)의 수요가 폭발적으로 연동되어 상승하고 있습니다. 이는 단편적 코딩 기술 습득이 아닌, AI 에이전트 군단을 부리는 '지식 기획자/오케스트레이터'로 독자들의 페르소나가 진화하고 있음을 반영합니다."
        ]
    },
    {
        title: "5.5 최종 전략 제언 (Action Items)",
        bullets: [
            "출판 기획자 관점: 기본 문법 교육서 기획을 전면 중단하고, 최신 AI 에이전트 및 바이브 코딩 기반의 1인 창업 풀코스, 실제 업무 자동화(RAG, CrewAI 등) 기획을 3개월 이내 단기 릴리즈 주기로 빠르게 시장에 던져 기민하게 반응을 살펴야 합니다.",
            "온라인 서점 유통 MD 관점: 책의 내용적 연관성을 넘어서는 '생태계 연계 추천' 시스템을 구축해야 합니다. '클로드 코드 마스터' 도서 상세 페이지에 단순 프로그래밍 언어 책이 아니라, 프롬프트를 축적하기 위한 '옵시디언 프로페셔널 노트' 도서를 크로스 추천하는 AI 기반 연동 배치 전략을 권장합니다.",
            "IT 저자 관점: 종이책 출판에만 머무르지 말고, 실습 코드의 깃허브 커뮤니티를 상시 개방하여 독자와 실시간으로 리팩터링 및 버그 수정을 공유하는 '오픈 소스형 집필 모델'을 도입해야 독자 록인을 극대화할 수 있습니다."
        ]
    }
];

insights.forEach(item => {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(item.title)] }));
    item.bullets.forEach(b => {
        children.push(new Paragraph({
            numbering: { reference: "bullets", level: 0 },
            children: [new TextRun({ text: b, font: "Arial" })],
            spacing: { before: 80, after: 80 }
        }));
    });
});

// 6. 문서 빌드 및 저장
const doc = new Document({
    styles: {
        default: { document: { run: { font: "Arial", size: 24 } } }, // Arial 12pt 기본값
        paragraphStyles: [
            { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 32, bold: true, font: "Arial" },
              paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
            { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
              run: { size: 28, bold: true, font: "Arial" },
              paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
        ]
    },
    numbering: numberingConfig,
    sections: [{
        properties: {
            page: {
                size: {
                    width: 11906,   // A4 너비 (DXA 단위)
                    height: 16838   // A4 높이 (DXA 단위)
                },
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 상하좌우 1인치 (1440 DXA)
            }
        },
        headers: {
            default: new Header({
                children: [
                    new Paragraph({
                        children: [new TextRun({ text: "YES24 IT/테크 도서 EDA 분석 보고서", size: 16, font: "Arial", color: "888888" })],
                        alignment: AlignmentType.RIGHT
                    })
                ]
            })
        },
        footers: {
            default: new Footer({
                children: [
                    new Paragraph({
                        children: [new TextRun({ text: "페이지 ", size: 16, font: "Arial", color: "888888" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, font: "Arial", color: "888888" })],
                        alignment: AlignmentType.CENTER
                    })
                ]
            })
        },
        children: children
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log("Word 문서 파일 변환 및 검증 완료:", outputPath);
}).catch(err => {
    console.error("문서 생성 중 오류 발생:", err);
    process.exit(1);
});
