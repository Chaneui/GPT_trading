from pykiwoom.kiwoom import Kiwoom

# Kiwoom 클래스 초기화
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)  # 로그인 창을 띄워서 로그인

# 삼성전자(종목코드: "005930")와 현대자동차(종목코드: "005380")의 현재가 요청 ❶
codes = ["005930", "005380"]  # 종목 코드 리스트
fields = ["현재가"]  # 요청할 필드
# ❷
for code in codes:
    data = kiwoom.block_request("opt10001",
                                종목코드=code,
                                output="주식기본정보",
                                next=0)

    # 현재가 출력 ❸
    price = data['현재가'][0]
    print(f"{code} 현재가: {price}")