import pandas as pd
from pykiwoom.kiwoom import Kiwoom
import time
from datetime import datetime, timedelta

# Kiwoom 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 계좌번호와 비밀번호 가져오기 (여기서는 비밀번호 사용이 필요 없는 경우가 많습니다만, 필요한 경우에 대비해 언급)
accounts = kiwoom.GetLoginInfo("ACCNO")  # 계좌번호
account = accounts[0]  # 첫 번째 계좌 사용

# 15일치 데이터를 저장할 빈 DataFrame 생성
all_trades_df = pd.DataFrame()

# 오늘 날짜에서 15일 전까지의 날짜 생성
end_date = datetime.now()
start_date = end_date - timedelta(days=15)

for single_date in (start_date + timedelta(n) for n in range(15)):
    # 기준일자 형식 맞추기 (예: '20240302')
    base_date = single_date.strftime('%Y%m%d')
    
    # block_request로 매매일지 데이터 가져오기
    df = kiwoom.block_request("opt10170",
                              계좌번호=account,
                              비밀번호="",  # 비밀번호는 실제 사용 시 정확한 값으로 설정
                              기준일자=base_date,
                              단주구분="1",
                              현금신용구분="0",
                              output="",
                              next=0)
    
    # "기준날짜" 컬럼 추가
    df['기준날짜'] = base_date
    
    # DataFrame에 추가
    all_trades_df = pd.concat([all_trades_df, df], ignore_index=True)
    
    # API 요청 간 0.5초 대기
    time.sleep(0.5)

# CSV 파일로 저장
all_trades_df.to_csv("매매일지.csv", index=False, encoding='utf-8-sig')