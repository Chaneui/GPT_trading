from pykiwoom.kiwoom import *

# Kiwoom 객체 생성
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)  # 로그인 창을 띄우고, 로그인이 완료될 때까지 대기 

# 로그인 성공 여부 확인
if kiwoom.GetConnectState() == 1:
    print("로그인 성공")
else:
    print("로그인 실패")

# 사용자 계좌번호 가져오기
accounts = kiwoom.GetLoginInfo("ACCNO")
my_account = accounts[0]
print(f"계좌번호: {my_account}")

# 예수금 상세 현황 요청
# opw00001: 예수금 상세현황 요청 코드
# "00": 조회구분값, 2자리의 문자열, "00"은 일반조회, "01"은 예수금상세현황
data = kiwoom.block_request("opw00001",
                            계좌번호=my_account,
                            # 비밀번호="",
                            # 비밀번호입력매체구분="00",
                            # 조회구분="2",
                            output="예수금상세현황",
                            next=0)

# 예수금 출력
deposit = data['예수금'][0]
print(f"예수금: {deposit}원")
