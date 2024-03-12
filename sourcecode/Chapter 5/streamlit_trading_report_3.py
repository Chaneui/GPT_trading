import streamlit as st
from pykrx import stock
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import CustomBusinessDay

# 한국 공휴일 정의 
class KoreanHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Year\'s Day', month=1, day=1, observance=nearest_workday),
        Holiday('Seollal', month=2, day=11, observance=nearest_workday),
        Holiday('Independence Day', month=3, day=1, observance=nearest_workday),
        Holiday('Children\'s Day', month=5, day=5, observance=nearest_workday),
        Holiday('Buddha\'s Birthday', month=5, day=19, observance=nearest_workday),
        Holiday('Memorial Day', month=6, day=6, observance=nearest_workday),
        Holiday('Liberation Day', month=8, day=15, observance=nearest_workday),
        Holiday('Chuseok', month=9, day=20, observance=nearest_workday),
        Holiday('National Foundation Day', month=10, day=3, observance=nearest_workday),
        Holiday('Hangeul Day', month=10, day=9, observance=nearest_workday),
        Holiday('Christmas Day', month=12, day=25, observance=nearest_workday)
    ]


# Streamlit 앱의 사이드바 설정
st.sidebar.title('주식 데이터 대시보드 설정')
# 사용자로부터 주식 종목코드 입력 받기
symbol_input = st.sidebar.text_input('주식 종목코드 입력', '005930,000660')
symbols = symbol_input.split(',')
# K값 입력 받기
k_value = st.sidebar.text_input('K값 입력', '0.5')
k_value = float(k_value)
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])
# 데이터 가져오기 버튼
if st.sidebar.button('데이터 가져오기'):
    # 현재 날짜와 15일 전 날짜 계산
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)

    st.header('종목별 OHLC 차트와 매수목표가격') # 임의 추가
    
    tabs = st.tabs([f"종목 {symbol}" for symbol in symbols])
    for tab, symbol in zip(tabs, symbols):
        with tab:
            # pykrx 모듈을 사용하여 주식 데이터 가져오기
            df = stock.get_market_ohlcv_by_date(start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'), symbol) #날짜수정
            
            # 직전 날짜의 데이터를 이용해 매수목표가격 계산
            df['매수목표가격'] = ((df['고가'] - df['저가']) * k_value + df['종가']).shift(1)

            # Plotly 그래프 생성
            fig = go.Figure()

            # OHLCV 차트 추가
            fig.add_trace(go.Candlestick(x=df.index,
                                         open=df['시가'], high=df['고가'],
                                         low=df['저가'], close=df['종가'],
                                         name='OHLCV'))

            # 매수목표가격 꺾은선 그래프 추가 (NaN 값을 제외하고 표시)
            fig.add_trace(go.Scatter(x=df.index, y=df['매수목표가격'],
                                     mode='lines+markers',
                                     name='매수목표가격'))

            # 레이아웃 설정
            fig.update_layout(title=f"{symbol} 주식 데이터",
                              yaxis_title="가격",
                              xaxis_title="날짜")
            st.plotly_chart(fig, use_container_width=True)
            
    if uploaded_file is not None:
        st.divider() # 임의추가
        st.header('일별 종목 수익 차트') # 임의추가
        st.write(
            '''
            일별로 매매한 종목의 수익률과 손익금액에 대한 그래프를 한 차트에 그립니다.
            수익률은 꺾은선 그래프로 왼쪽 y축 값으로 확인할 수 있으며,
            손익금액은 막대 그래프로 오른쪽 y축에서 값을 확인할 수 있습니다.
            오른쪽의 범례를 클릭하면 특정 그래프를 숨기거나 보이게 할 수 있습니다.
            '''
        )
        
        # CSV 파일 읽기
        df = pd.read_csv(uploaded_file)
        
        # NaN 값 제거 및 데이터 전처리
        filtered_df = df.dropna()
        filtered_df['기준날짜'] = pd.to_datetime(filtered_df['기준날짜'], format='%Y%m%d')
        
        # 종목별 색상 매핑
        colors = {stock: f'rgb({(i*50)%255}, {(i*80)%255}, {(i*30)%255})' for i, stock in enumerate(filtered_df['종목명'].unique())}
        
        # 2개의 y축을 가진 서브플롯 생성
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 각 종목별로 차트에 데이터 추가
        for stock, group_df in filtered_df.groupby('종목명'):
            color = colors[stock]
            # 수익률 꺾은선 그래프
            fig.add_trace(go.Scatter(x=group_df['기준날짜'], y=group_df['수익률'], name=f"{stock} 수익률", marker_color=color), secondary_y=False)
            # 손익금액 막대 그래프
            fig.add_trace(go.Bar(x=group_df['기준날짜'], y=group_df['손익금액'], name=f"{stock} 손익금액", marker_color=color), secondary_y=True)

        # 차트 레이아웃 설정
        fig.update_layout(title_text="일별 수익률 및 손익금액", xaxis_title="기준날짜")
        fig.update_yaxes(title_text="수익률 (%)", secondary_y=False)
        fig.update_yaxes(title_text="손익금액 (원)", secondary_y=True)
        
        # Streamlit을 통해 차트 표시
        st.plotly_chart(fig)
    
    
        st.divider() # 임의추가 
        st.header('종목별 전체 기간 데이터') # 임의추가
        st.write(
            '''
            전체 기간동안의 매매 데이터를 차트로 표시합니다.
            1) 종목별 전체 기간 동안의 매매 수량의 비율을 나타냅니다.
            2) 종목별 전체 기간 동안의 평균 수익률을 나타냅니다.
            3) 종목별 전체 거래일 동안 해당 종목을 매수할 확률을 나타냅니다.
            '''
        )
        
        # 기준날짜를 datetime 타입으로 변환 
        df['기준날짜'] = pd.to_datetime(df['기준날짜'], format='%Y%m%d')
        
        # 한국 공휴일을 고려한 Business Day 계산
        kr_business_day = CustomBusinessDay(calendar=KoreanHolidayCalendar())
        total_days = pd.date_range(start=df['기준날짜'].min(), end=df['기준날짜'].max(), freq=kr_business_day)

        # 데이터 분석
        buy_quantity_by_stock = df.groupby('종목명')['매수수량'].sum()
        avg_return_by_stock = df.groupby('종목명')['수익률'].mean()
        trading_days_by_stock = df.groupby('종목명')['기준날짜'].nunique()
        buying_progress = (trading_days_by_stock / len(total_days)) * 100

        # Streamlit 컬럼 레이아웃
        col1, col2, col3 = st.columns(3)
        chart_width, chart_height = 220, 300

        # 차트 1: 종목별 매수수량 비율 파이 차트
        with col1:
            fig1 = px.pie(values=buy_quantity_by_stock.values, names=buy_quantity_by_stock.index, title='종목별 매수수량 비율')
            fig1.update_layout(width=chart_width, height=chart_height)  # 차트 사이즈 조정
            st.plotly_chart(fig1)

        # 차트 2: 종목별 평균 수익률 막대 차트
        with col2:
            fig2 = px.bar(x=avg_return_by_stock.index, y=avg_return_by_stock.values, title='종목별 평균 수익률', labels={'x':'종목명', 'y':'평균 수익률'})
            fig2.update_layout(width=chart_width, height=chart_height)  # 차트 사이즈 조정
            st.plotly_chart(fig2)

        # 차트 3: 종목별 일일 매수 확률 막대 차트
        with col3:
            fig3 = px.bar(x=buying_progress.index, y=buying_progress.values, title='종목별 일일 매수 확률', labels={'x':'종목명', 'y':'매수 확률 (%)'})
            fig3.update_layout(width=chart_width, height=chart_height)  # 차트 사이즈 조정
            st.plotly_chart(fig3)