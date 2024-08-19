import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QStackedWidget, QHBoxLayout, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from csv_converter import ExcelToCSVMapper
from csv_deduplicator import CSVDeduplicator
from csv_merger import CSVMerger  # CSV 병합 클래스를 import

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CSV 툴 by 김재형")
        self.setGeometry(100, 100, 800, 600)

        # 스택 위젯 생성
        self.stack = QStackedWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        # 메인 화면 위젯 추가
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 버튼을 중앙에 배치하는 레이아웃
        button_layout = QVBoxLayout()

        # 중앙 정렬을 위한 QHBoxLayout 추가
        hbox = QHBoxLayout()
        hbox.addStretch()

        convert_button = QPushButton("Excel → CSV 변환")
        convert_button.clicked.connect(self.show_converter)
        convert_button.setFixedSize(200, 50)  # 버튼 크기 조정
        hbox.addWidget(convert_button)

        hbox.addStretch()
        button_layout.addLayout(hbox)

        hbox2 = QHBoxLayout()
        hbox2.addStretch()

        dedup_button = QPushButton("CSV 중복 제거 및 추출")
        dedup_button.clicked.connect(self.show_deduplicator)
        dedup_button.setFixedSize(200, 50)  # 버튼 크기 조정
        hbox2.addWidget(dedup_button)

        hbox2.addStretch()
        button_layout.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addStretch()

        merge_button = QPushButton("CSV 병합")
        merge_button.clicked.connect(self.show_merger)
        merge_button.setFixedSize(200, 50)  # 버튼 크기 조정
        hbox3.addWidget(merge_button)

        hbox3.addStretch()
        button_layout.addLayout(hbox3)

        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.main_widget.setLayout(main_layout)
        self.stack.addWidget(self.main_widget)

        # CSV 변환툴 위젯 추가
        self.converter = ExcelToCSVMapper(parent=self)
        self.stack.addWidget(self.converter)

        # CSV 중복 제거 위젯 추가
        self.deduplicator = CSVDeduplicator(parent=self)
        self.stack.addWidget(self.deduplicator)

        # CSV 병합 위젯 추가
        self.merger = CSVMerger(parent=self)
        self.stack.addWidget(self.merger)

        self.setLayout(layout)

    def show_converter(self):
        self.stack.setCurrentWidget(self.converter)

    def show_deduplicator(self):
        self.stack.setCurrentWidget(self.deduplicator)

    def show_merger(self):
        self.stack.setCurrentWidget(self.merger)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 스플래시 화면 설정
    splash_pix = QPixmap("splash.png")  # 스플래시 화면으로 사용할 이미지 경로
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()

    # 메인 윈도우 설정
    window = MainWindow()

    # 스플래시 화면 표시 시간 (3초)
    QTimer.singleShot(3000, splash.close)  # 3초 후에 스플래시 화면 닫기
    QTimer.singleShot(3000, window.show)   # 3초 후에 메인 윈도우 표시

    sys.exit(app.exec_())
