import numpy as np
import pandas as pd
from pykrx import stock
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 삼성전자 주식 데이터 불러오기
df = stock.get_market_ohlcv_by_date("20230101", "20240131", "005930")

# 특성과 타겟 설정 (전날까지의 데이터로 다음 날의 고가 예측)
X = df[['시가', '저가', '종가', '거래량']].shift(1).iloc[1:]
y = df['고가'].iloc[1:]

# 학습 및 테스트 데이터 분할
X_train, X_test = X[:'20240115'], X['20240116':'20240131']
y_train, y_test = y[:'20240115'], y['20240116':'20240131']

# 랜덤 포레스트 모델 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 예측
predictions = model.predict(X_test)

# 결과 시각화
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['고가'], label='Actual High Price', color='blue')
plt.plot(X_test.index, predictions, label='Predicted High Price', color='red', linestyle='--')
plt.title('Samsung Electronics Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('High Price')
plt.legend()
plt.show()