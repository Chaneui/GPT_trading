import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime
from pykiwoom.kiwoom import Kiwoom
from pykrx import stock
import datetime

# Qt Designer로 생성한 gui 파일 로드
form_class = uic.loadUiType(r'파일 경로 추가')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Kiwoom 로그인
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)

        # 버튼 연결
        self.button_start.clicked.connect(self.start_trading)
        self.button_stop.clicked.connect(self.stop_trading)

        # 타이머 설정
        self.market_timer = QTimer(self)
        self.market_timer.timeout.connect(self.check_market_time)
        self.trade_timer = QTimer(self)
        self.trade_timer.timeout.connect(self.trade_stocks)

    def start_trading(self):
        self.market_timer.start(1000 * 60)  # 1분마다 check_market_time 호출
        self.trade_timer.start(1000 * 17)  # 17초마다 trade_stocks 호출

    def stop_trading(self):
        self.market_timer.stop()  # 타이머 중지
        self.trade_timer.stop()

    def check_market_time(self):
        now = QTime.currentTime()
        if now.toString("HHmm") >= "1500":  # 15시가 되면 매도
            self.stop_trading()  # 모든 타이머 중지
            self.sell_all_stocks()

    def trade_stocks(self):
        codes = self.code_list.text().split(',')  # 종목 코드 분리
        k_value = float(self.k_value.text())  # K 값 입력 받기
        
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        
        # 가장 최근의 거래일 얻기
        last_trading_day = stock.get_nearest_business_day_in_a_week(date=yesterday.strftime('%Y%m%d'))

        for code in codes:
            if code.strip():  # 종목 코드가 비어 있지 않은 경우에만 처리
                # 현재가 조회 및 로그 출력
                current_price = int(self.kiwoom.block_request("opt10001",
                                                              종목코드=code.strip(),
                                                              output="주식기본정보",
                                                              next=0)['현재가'][0].replace(",", ""))
                # 현재가가 음수인 경우 절대값으로 변환
                current_price = abs(current_price)
                
                now = datetime.datetime.now().strftime('%H:%M:%S')
                name = self.kiwoom.block_request("opt10001",
                                                 종목코드=code.strip(),
                                                 output="주식기본정보",
                                                 next=0)['종목명'][0]
                self.textboard.append(f"[{now}] [{code.strip()}] [{name}] [현재가: {current_price}]")

                # 변동성 돌파 전략 계산 및 매수 조건 확인
                yesterday_data = stock.get_market_ohlcv_by_date(last_trading_day, last_trading_day, code.strip())
                if not yesterday_data.empty:
                    high = yesterday_data['고가'][0]
                    low = yesterday_data['저가'][0]
                    close = yesterday_data['종가'][0]
                    target_price = close + (high - low) * k_value
                    
                    if current_price > target_price:  # 변동성 돌파 전략에 따라 매수
                        self.buy_stock(code.strip(), current_price, 1)

    def buy_stock(self, code, price, quantity):
        # 매수 주문
        account_number = self.kiwoom.GetLoginInfo("ACCNO")[0]  # 첫 번째 계좌 사용
        order_type = 1  # 신규매수
        trade_type = "00"  # 지정가
        self.kiwoom.SendOrder("SendOrder", "0101", account_number, order_type, code, quantity, price, trade_type, "")
        self.buysell_log.append(f"[매수 주문] [{code}] [가격: {price}] [수량: {quantity}]")

    def sell_all_stocks(self):
        account_number = self.kiwoom.GetLoginInfo("ACCNO")[0].split(';')[0]  # 첫 번째 계좌 사용
        password = ""  # 비밀번호는 빈 문자열로 설정 (실제 사용 시 필요에 따라 수정)
        
        # 계좌평가잔고내역요청
        result = self.kiwoom.block_request("opw00004",
                                        계좌번호=account_number,
                                        비밀번호=password,
                                        비밀번호입력매체구분="00",
                                        조회구분=2,
                                        output="계좌평가현황",
                                        next=0)
        
        # 보유 종목별로 매도 주문
        for i in range(len(result['종목번호'])):
            code = result['종목번호'][i].strip()[1:]  # 종목코드 앞의 'A' 제거
            quantity = int(result['보유수량'][i])
            if quantity > 0:
                # 현재가 조회
                current_price_info = self.kiwoom.block_request("opt10001", 종목코드=code, output="주식기본정보", next=0)
                current_price = current_price_info['현재가'][0].replace(",", "")
                
                # 매도 주문
                self.kiwoom.SendOrder("SendOrderSell", "0101", account_number, 2, code, quantity, current_price, "00", "")
                self.buysell_log.append(f"[매도 주문] [{code}] [가격: {current_price}] [수량: {quantity}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())