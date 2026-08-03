# Yes24 데이터 수집 명세

## 1. 과업 목표
- Yes24 웹사이트에서 특정 카테고리의 도서 정보를 수집합니다.
- 수집된 데이터는 분석 및 시각화에 활용될 수 있도록 정제된 형태로 저장합니다.

## 2. 수집 관련 정보

### 네트워크 메뉴를 통해 실제 데이터를 가져오는 URL
Request URL
https://www.yes24.com/product/category/CategoryProductContents?dispNo=001001003032&order=SINDEX_ONLY&addOptionTp=0&page=4&size=24&statGbYn=N&viewMode=&_options=&directDelvYn=&usedTp=0&elemNo=0&elemSeq=0&seriesNumber=0
Request Method
GET
Status Code
200 OK

### 해당 Request에 대한 Header 정보
host
www.yes24.com
referer
https://www.yes24.com/product/category/display/001001003032
rtt
50
sec-ch-ua
"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"macOS"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
viewport-width
813
x-requested-with
XMLHttpRequest

### Payload
dispNo=001001003032&order=SINDEX_ONLY&addOptionTp=0&page=4&size=24&statGbYn=N&viewMode=&_options=&directDelvYn=&usedTp=0&elemNo=0&elemSeq=0&seriesNumber=0


### 응답 예시 (HTML, JSON 의 일부 정보)
<div class="itemUnit">
        <div class="item_img">
            <div class="img_canvas">
                
                <span class="img_item">
                    <span class="img_grp">
                        
                                                                                                <a href="/product/goods/151170115" class="lnk_img" onclick=" ">
                            <em class="img_bdr">
                                <img class="lazy" data-original="https://image.yes24.com/goods/151170115/L" src="https://image.yes24.com/goods/151170115/L" border="0" alt="챗GPT와 엑셀로 만드는 주식 &amp;amp; 암호화폐 자동매매 시스템" style="display: inline;">
                            </em>
                        </a>
                    </span>
                </span>
            </div>
            <div class="img_btn">
                
                        <a href="javascript:yes24GU.openPreviewCheck(151170115); " class="btnC btn_preview"><span class="bWrap"><em class="txt">미리보기</em></span></a>
                                            </div>
        </div>
        <div class="item_info">
            
                <div class="info_row info_keynote">




    
    <script type="text/javascript">
        if ($('#spanGdKeynote').children().length == 0) {
            $('#spanGdKeynote').remove();
        }
    </script>


                </div>
            <div class="info_row info_name">
                
                                <a class="gd_name" href="/product/goods/151170115" onclick=" ">챗GPT와 엑셀로 만드는 주식 &amp; 암호화폐 자동매매 시스템</a>
                
                    <span class="gd_nameE">엑셀 VBA와 AI로 시작하는 금융 프로그래밍</span>
                                <a href="/product/goods/151170115" target="_blank" class="bgYUI ico_nWin" onclick=" ">챗GPT와 엑셀로 만드는 주식 &amp; 암호화폐 자동매매 시스템 새창이동</a>
            </div>
                <div class="info_row info_pubGrp">
                    
                            <span class="authPub info_auth" onclick="">
                                <a href="https://www.yes24.com/product/search?domain=ALL&amp;query=%25EC%2584%25A4%25EA%25B7%25BC%25EB%25AF%25BC&amp;authorNo=441357&amp;author=설근민" target="_blank">설근민</a> 저
                            </span>
                    
                        <span class="authPub info_pub" onclick=""><a href="https://www.yes24.com/product/search?&amp;domain=ALL&amp;company=%ec%a0%9c%ec%9d%b4%ed%8e%8d&amp;query=%25EC%25A0%259C%25EC%259D%25B4%25ED%258E%258D">제이펍</a></span>
                                            <span class="authPub info_date">2025년 08월</span>
                </div>
                                                        <div class="info_row info_price">
                            <span class="txt_sale"><em class="num">10</em>%</span>
                        <strong class="txt_num"><em class="yes_b">22,500</em>원</strong>
                        <span class="txt_num dash"><em class="yes_m">25,000</em>원</span>
                                                    <span class="yPoint"><em class="bgYUI ico_point">포인트적립</em>1,250원</span>
                    </div>
                            <div class="info_row info_rating ">
                            <span class="saleNum">
                                판매지수 1,692
                            </span>
                                            <span class="rating_rvCount">
                            <a href="https://www.yes24.com/product/goods/151170115?ReviewYn=Y" onclick=""><em class="bit">회원리뷰</em>(<em class="txC_blue">6</em>건)</a>
                        </span>
                        <span class="rating_grade">
                            <span class="bgYUI tRating tRating_10">리뷰 총점</span><em class="yes_b">10.0</em>
                            <span class="moreRatingArea">
                                <span class="moreRatingBtn">
                                        <a href="javascript:void(0);" onclick="toggleLiCont(this,$('.sGLi'),event);" class="bgYUI">정보 더 보기/감추기</a>
                                </span>
                                <span class="moreRatingLi">
                                    <span class="moreRatingLiRow">
                                        <ul class="yesAlertLi">
                                            <li><em class="bl_dot bgYUI">&nbsp;</em>종이책 리뷰 (4건)</li>
                                            <li><em class="bl_dot bgYUI">&nbsp;</em>eBook 리뷰 (0건)</li>
                                            <li><em class="bl_dot bgYUI">&nbsp;</em>종이책 한줄평 (1건)</li>
                                            <li><em class="bl_dot bgYUI">&nbsp;</em>eBook 한줄평 (1건)</li>
                                        </ul>
                                    </span>
                                </span>
                            </span>
                        </span>
                </div>

                    <div class="info_row info_deli" name="delvTextArea"><span class="deli_des">21시까지 주문하면 </span><span class="deli_date"><strong class="deli_act">내일 아침 7시 전 (10/11, 토)</strong> 도착예정</span></div>

            
                                                                                                
            
                    <div class="info_row info_read">
                        누구나 할 수 있는 AI 기반 트레이딩 시스템 구축 엑셀 VBA와 챗GPT로 완성하는 금융 자동화의 시작! 복잡한 엑셀 VBA는 몰라도 괜찮다. 챗GPT에 질문하고, 챗GPT가 만들어준 코드를 엑셀에 붙여넣기만 하면 자동화 ...
                    </div>
                                        <div class="info_row info_event">
                                <div class="event">
                                        <span class="iconC freeD"><em class="txt">이벤트</em></span>
                                                                                                            <span class="iconC"><em class="txt">사은품</em></span>

                                    <span class="txt"><a href="https://event.yes24.com/template?EventNo=261398">[단독] 『챗GPT와 엑셀로 만드는 주식 &amp; 암호화폐 자동매매 시스템』 출간 기념 - 아이스 변색 머그</a></span>
                                    <span class="date">(25.08.14 ~ 00.12.31)</span>
                                </div>
                            </div>


            
                                        <div class="info_row info_relG">
                    관련상품 :                            <span class="relG"><a href="/product/goods/153684960">eBook <span class="relG_num">17,500원</span></a></span>
                </div>
                    </div>
            <div class="item_btnCol">
                
                


            <span class="btn_row">
                <span class="chkBox" style=""><label><input type="checkbox" name="ORD_GOODS_CHKBOX" id="ordChk_151170115" data-goodsno="151170115" class="basic" style=""><span class="bgYUI chk"></span></label></span>
                    <span class="numBox">
                        <span class="yesIpt ipt_wSizeF">
                            <input type="text" name="ORD_GOODS_CNT" id="ordCnt_151170115" style="ime-mode:disabled !important" title="수량설정" value="1" class="ac yes_m" onkeyup="return checkNumeric(this);" maxlength="3">
                        </span>
                        <button type="button" class="minus" onclick="order_payment.downOrderCount('151170115'); "><span class="bgYUI">수량감소</span></button>
                        <button type="button" class="plus" onclick="order_payment.upOrderCount('151170115'); "><span class="bgYUI">수량증가</span></button>
                    </span>
            </span>
                <a href="javascript:void(0);" onclick="order_payment.addCartV3('151170115', '', this, '', '', '', '', 'Search', true); " class="btnC btn_blue"><span class="bWrap"><em class="txt">카트에 넣기</em></span></a>
            <a href="javascript:void(0);" onclick="order_payment.orderDirectV3('151170115', '', this, '', '', '', '', 'Search'); " class="btnC btn_sBlue"><span class="bWrap"><em class="txt">바로구매</em></span></a>
        <a href="javascript:void(0);" class="btnC" name="btnList" onclick="order_payment.addMyListV3('151170115', '', '', true, ''); ;"><span class="bWrap"><em class="txt">리스트에 넣기</em></span></a>
<input type="hidden" name="ORD_GOODS_OPT" id="ordOpt_151170115" value="{&quot;goods_no&quot;:151170115,&quot;goods_seq&quot;:1,&quot;order_limit_yn&quot;:&quot;N&quot;,&quot;order_remain_count&quot;:0,&quot;event_no&quot;:0,&quot;add_cart_yn&quot;:&quot;Y&quot;,&quot;goods_state&quot;:&quot;02&quot;,&quot;order_limit_count&quot;:0,&quot;resource_key&quot;:&quot;01&quot;,&quot;limit_age_yn&quot;:&quot;N&quot;,&quot;limit_age&quot;:0,&quot;member_age&quot;:0,&quot;goods_name&quot;:&quot;챗GPT와 엑셀로 만드는 주식 &amp;amp; 암호화폐 자동매매 시스템&quot;,&quot;noint_quotamonth&quot;:0,&quot;min_cnt&quot;:0,&quot;max_cnt&quot;:0,&quot;opt_salepr&quot;:0,&quot;opt_yn&quot;:&quot;N&quot;,&quot;opt_inst_yn&quot;:&quot;N&quot;,&quot;flat_rate_yn&quot;:null,&quot;rent_goods_yn&quot;:&quot;N&quot;,&quot;bookclue_yn&quot;:&quot;N&quot;,&quot;goods_gb&quot;:&quot;01&quot;,&quot;goodsSortNo&quot;:&quot;001002&quot;,&quot;goodsSortNm&quot;:&quot;IT 모바일&quot;,&quot;goodsAuth&quot;:&quot;&lt;설근민&gt; 저&quot;,&quot;shopPrice&quot;:25000.00,&quot;salePrice&quot;:22500.00,&quot;discountShopPrice&quot;:2500.00}">

            </div>
    </div>



## 3. 수집할 데이터 항목
각 도서에 대해 다음 정보를 수집합니다.

- **제목:** 도서 제목
- **저자:** 저자 정보
- **출판사:** 출판사 정보
- **발행일:** 도서 발행일
- **정가:** 정가
- **판매가:** 할인이 적용된 판매 가격
- **리뷰 수:** 리뷰 개수
- **판매지수:** 판매지수
- **상세 정보:** 상세 정보
- **설명:** 설명
- **상세 페이지 URL:** 각 도서의 상세 정보 페이지 링크

## 4. 데이터 수집 프로세스
* 파이썬과 관련 라이브러리를 활용하여 1페이지부터 10페이지까지 수집하고 페이지당 120개씩 수집하게 하고
수집한 결과의 일부를 데이터프레임 형태로 가공하고 수집 결과는 csv파일로 저장할 것
* 수집 과정을 로그로 출력하여 수집 상태를 확인할 수 있게 할 것 

## 5. 데이터 저장 형식
- **파일 형식:** CSV (Comma-Separated Values)


## 6. 추가 요구사항
- 가상환경은 uv를 사용할 것
- 데이터 수집 시 웹사이트에 과도한 부하를 주지 않도록 요청 간에 적절한 시간 간격(예: 1-2초)을 둡니다.
- 오류 발생 시(예: 특정 항목을 찾을 수 없는 경우), 해당 항목은 건너뛰고 로그를 남긴 후 다음 항목 수집을 계속 진행합니다.