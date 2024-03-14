import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser, QPushButton, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from pykiwoom.kiwoom import Kiwoom
import datetime

class StockApp(QMainWindow):
    def __init__(self): #
        super().__init__()
        uic.loadUi('파일 경로 입력', self)  # QtDesigner로 생성한 gui.ui 파일 로드. .ui 파일 저장 경로 입력 필요.

        # Ui에서 요소 찾기
        self.textboard = self.findChild(QTextBrowser, 'textboard')
        self.button_start = self.findChild(QPushButton, 'button_start')
        self.button_stop = self.findChild(QPushButton, 'button_stop')
        self.code_list = self.findChild(QLineEdit, 'code_list')

        # Kiwoom 로그인
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)

        # 타이머 설정 #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stock_price)

        # 버튼 이벤트 연결 #
        self.button_start.clicked.connect(self.start_update)
        self.button_stop.clicked.connect(self.stop_update)

    def start_update(self):
        self.timer.start(1000)  # 1초마다 update_stock_price 호출

    def stop_update(self):
        self.timer.stop()  # 타이머 중지
        self.textboard.clear()  # QTextBrowser 내용 삭제

    def update_stock_price(self): #
        codes = self.code_list.text().split(',')  # 사용자 입력 종목 코드 분리
        for code in codes:
            if code.strip():  # 종목 코드가 비어있지 않은 경우
                # 현재가 정보 요청
                data = self.kiwoom.block_request("opt10001",
                                                 종목코드=code.strip(),
                                                 output="주식기본정보",
                                                 next=0)
                
                now = datetime.datetime.now().strftime("%H:%M:%S")  # 현재 시간
                name = data['종목명'][0]  # 종목명
                price = data['현재가'][0]  # 현재가
                log = f"[{now}] [{code}] [{name}] [{price}]"
                self.textboard.append(log)  # 로그 출력

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())
