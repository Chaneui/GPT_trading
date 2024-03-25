import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle('PyQt5 Widgets Example')
    window.setGeometry(100, 100, 300, 200)  # x, y, width, height
    
    # 레이블 생성
    label = QLabel('Hello, PyQt5!')
    
    # 텍스트 입력 필드 생성
    lineEdit = QLineEdit()
    
    # 버튼 생성 및 클릭 이벤트 처리
    button = QPushButton('Click Me')
    button.clicked.connect(lambda: label.setText(lineEdit.text()))
    
    # 수평 레이아웃에 텍스트 입력 필드와 버튼 추가
    hbox = QHBoxLayout()
    hbox.addWidget(lineEdit)
    hbox.addWidget(button)
    
    # 수직 레이아웃에 레이블과 수평 레이아웃 추가
    vbox = QVBoxLayout(window)
    vbox.addWidget(label)
    vbox.addLayout(hbox)
    
    window.setLayout(vbox)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()