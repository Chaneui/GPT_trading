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
        self.trade_timer.start(1000)  # 1초마다 trade_stocks 호출

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

        for code in codes:
            if code.strip():  # 종목 코드가 비어 있지 않은 경우에만 처리
                # 현재가 조회 및 로그 출력
                current_price = int(self.kiwoom.block_request("opt10001",
                                                              종목코드=code.strip(),
                                                              output="주식기본정보",
                                                              next=0)['현재가'][0].replace(",", ""))
                now = datetime.datetime.now().strftime('%H:%M:%S')
                name = self.kiwoom.block_request("opt10001",
                                                 종목코드=code.strip(),
                                                 output="주식기본정보",
                                                 next=0)['종목명'][0]
                self.textboard.append(f"[{now}] [{code.strip()}] [{name}] [현재가: {current_price}]") # ❷

                # 변동성 돌파 전략 계산 및 매수 조건 확인
                yesterday_data = stock.get_market_ohlcv_by_date(datetime.datetime.now().strftime('%Y%m%d'), datetime.datetime.now().strftime('%Y%m%d'), code.strip())
                if not yesterday_data.empty:
                    high = yesterday_data['고가'][0]
                    low = yesterday_data['저가'][0]
                    close = yesterday_data['종가'][0]
                    target_price = close + (high - low) * k_value
                
                    
                    if current_price > target_price:  # 변동성 돌파 전략에 따라 매수
                        self.buy_stock(code.strip(), current_price, 1)

    def buy_stock(self, code, price, quantity):
        # 매수 로직 구현 (여기서는 로그만 출력)
        name = self.kiwoom.block_request("opt10001",
                                         종목코드=code,
                                         output="주식기본정보",
                                         next=0)['종목명'][0]
        self.buysell_log.append(f"[매수] [{code}] [{name}] [가격: {price}] [수량: {quantity}]")

    def sell_all_stocks(self):
        # 매도 로직 구현 (여기서는 로그만 출력)
        self.buysell_log.append("15시가 되어 모든 주식을 매도합니다.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())