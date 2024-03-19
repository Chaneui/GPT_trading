import streamlit as st
from pykrx import stock
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic' 

# Streamlit 앱의 사이드바 설정
st.sidebar.header('주식 데이터 조회')
# 사용자로부터 주식 종목 코드 입력받기
code_list = st.sidebar.text_input('주식 종목코드 입력 (콤마로 구분)', '')
# 조회 버튼 생성
plot_button = st.sidebar.button('그래프 그리기')

# 버튼이 눌렸을 때 작업 수행
if plot_button:
    if code_list:
        # 종목코드를 콤마로 구분하여 리스트로 변환
        codes = code_list.split(',')
        # 오늘 날짜와 30일 전 날짜 계산
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

        for code in codes:
            # 각 종목별로 30일간의 종가 데이터 불러오기
            df = stock.get_market_ohlcv_by_date(fromdate=start_date, todate=end_date, ticker=code)
            # 데이터가 없는 경우 메시지 출력
            if df.empty:
                st.write(f'종목코드 {code}에 대한 데이터를 찾을 수 없습니다.')
            else:
                # 데이터가 있는 경우, 종가 그래프 그리기
                plt.figure(figsize=(10, 4))
                plt.plot(df['종가'], label=code)
                plt.title(f'{code} 종가 그래프')
                plt.xlabel('날짜')
                plt.ylabel('종가')
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()
                # Streamlit을 통해 그래프 출력
                st.pyplot(plt)
    else:
        st.sidebar.write('주식 종목코드를 입력해주세요.')