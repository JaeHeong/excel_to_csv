import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QStackedWidget, QHBoxLayout
from csv_converter import ExcelToCSVMapper
from csv_deduplicator import CSVDeduplicator

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

        convert_button = QPushButton("CSV 변환툴")
        convert_button.clicked.connect(self.show_converter)
        convert_button.setFixedSize(200, 50)  # 버튼 크기 조정
        hbox.addWidget(convert_button)

        hbox.addStretch()
        button_layout.addLayout(hbox)

        hbox2 = QHBoxLayout()
        hbox2.addStretch()

        dedup_button = QPushButton("CSV 중복 제거")
        dedup_button.clicked.connect(self.show_deduplicator)
        dedup_button.setFixedSize(200, 50)  # 버튼 크기 조정
        hbox2.addWidget(dedup_button)

        hbox2.addStretch()
        button_layout.addLayout(hbox2)

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

        self.setLayout(layout)

    def show_converter(self):
        self.stack.setCurrentWidget(self.converter)

    def show_deduplicator(self):
        QMessageBox.information(self, "알림", "CSV 중복 제거 기능은 아직 구현되지 않았습니다.")
        # self.stack.setCurrentWidget(self.deduplicator)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
