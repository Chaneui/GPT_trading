import streamlit as st
from pykrx import stock
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 앱의 사이드바 설정
st.sidebar.title('주식 데이터 대시보드 설정')
# 사용자로부터 주식 종목코드 입력 받기
symbol_input = st.sidebar.text_input('주식 종목코드 입력', '005930,000660')
symbols = symbol_input.split(',')
# K값 입력 받기
k_value = st.sidebar.text_input('K값 입력', '0.5')
k_value = float(k_value)
# 데이터 가져오기 버튼
if st.sidebar.button('데이터 가져오기'):
    # 현재 날짜와 15일 전 날짜 계산
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)

    st.header('종목별 OHLC 차트와 매수목표가격')
    
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
