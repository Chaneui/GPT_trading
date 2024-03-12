# 필요 모듈 임포트 ❶
import numpy as np
import pandas as pd
from pykrx import stock
import matplotlib.pyplot as plt

# 삼성전자 주식 데이터 불러오기 (2022년 1월부터 12월까지) ❷
df = stock.get_market_ohlcv_by_date(fromdate="20230101", todate="20231231", ticker="005930")

# 변동성 돌파 전략을 위한 대상 계산 (전일 고가 - 전일 저가) * K ❸
K = 0.5  # K 값은 전략에 따라 조정 가능
df['Target'] = (df['고가'].shift(1) - df['저가'].shift(1)) * K

# 매수 조건 및 매도 조건 설정 ❹
df['Buy'] = df['시가'] + df['Target']
df['Sell'] = np.where(df['고가'] > df['Buy'], df['종가'], np.nan)

# 백테스팅 수익률 계산 ❺
df['Return'] = np.where(df['고가'] > df['Buy'], df['Sell'] / df['Buy'], 1)

# 누적 수익률 계산 ❻
df['Cumulative Return'] = df['Return'].cumprod()

# 결과 시각화 ❼
plt.figure(figsize=(12, 6))
plt.plot(df['Cumulative Return'], label='Cumulative Return')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.title('Samsung Electronics - Volatility Breakout Strategy')
plt.legend()
plt.show()