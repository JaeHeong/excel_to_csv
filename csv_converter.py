import sys
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import csv
import pickle

class ExcelToCSVMapper(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CSV 변환툴 by 김재형")
        self.setGeometry(100, 100, 800, 600)
        
        self.csv_columns = []
        self.excel_columns = []

        layout = QVBoxLayout()

        # 홈 버튼
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        layout.addWidget(home_button, alignment=Qt.AlignCenter)

        # 테이블 위젯 생성
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["CSV 컬럼명", "Excel 컬럼명"])
        self.table.setShowGrid(True)
        # self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.table)

        # 매핑 추가/삭제 버튼 레이아웃
        button_layout = QVBoxLayout()
        button_layout.addStretch()

        add_button = QPushButton("열 추가")
        add_button.clicked.connect(self.add_mapping)
        button_layout.addWidget(add_button, alignment=Qt.AlignCenter)

        remove_button = QPushButton("열 삭제")
        remove_button.clicked.connect(self.remove_mapping)
        button_layout.addWidget(remove_button, alignment=Qt.AlignCenter)

        save_button = QPushButton("현재값 저장")
        save_button.clicked.connect(self.save_mappings)
        button_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        generate_button = QPushButton("CSV 생성")
        generate_button.clicked.connect(self.generate_csv)
        button_layout.addWidget(generate_button, alignment=Qt.AlignCenter)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.load_mappings()
        self.setLayout(layout)
        if not self.table.rowCount():
            self.add_mapping()

    def resizeEvent(self, event):
        table_width = self.table.width()
        self.table.setColumnWidth(0, table_width // 2 - 1)
        self.table.setColumnWidth(1, table_width // 2 - 1)
        super().resizeEvent(event)

    def go_home(self):
        main_window = self.parent().parent()
        main_window.stack.setCurrentWidget(main_window.main_widget)

    def add_mapping(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        csv_item = QTableWidgetItem("")
        excel_item = QTableWidgetItem("")
        self.table.setItem(row_position, 0, csv_item)
        self.table.setItem(row_position, 1, excel_item)

    def remove_mapping(self):
        row_position = self.table.rowCount()
        if row_position > 0:
            self.table.removeRow(row_position - 1)

    def save_mappings(self):
        mappings = []
        for row in range(self.table.rowCount()):
            csv_col = self.table.item(row, 0).text().strip()
            excel_col = self.table.item(row, 1).text().strip()
            if csv_col and excel_col:
                mappings.append((csv_col, excel_col))

        with open("mappings.pkl", "wb") as f:
            pickle.dump(mappings, f)

        QMessageBox.information(self, "저장 완료", "매핑 데이터가 성공적으로 저장되었습니다!")

    def load_mappings(self):
        try:
            with open("mappings.pkl", "rb") as f:
                mappings = pickle.load(f)
                for csv_col, excel_col in mappings:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    csv_item = QTableWidgetItem(csv_col)
                    excel_item = QTableWidgetItem(excel_col)
                    self.table.setItem(row_position, 0, csv_item)
                    self.table.setItem(row_position, 1, excel_item)
        except (FileNotFoundError, EOFError):
            pass

    def generate_csv(self):
        excel_path, _ = QFileDialog.getOpenFileName(self, "엑셀 파일 선택", "", "Excel files (*.xlsx)")
        if not excel_path:
            return

        try:
            excel_data = pd.read_excel(excel_path)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"엑셀 파일을 불러오는데 실패했습니다: {e}")
            return

        mapping = {}
        for row in range(self.table.rowCount()):
            csv_col = self.table.item(row, 0).text().strip()
            excel_col = self.table.item(row, 1).text().strip()
            if csv_col and excel_col:
                mapping[csv_col] = excel_col

        csv_data = {}
        for csv_col, excel_col in mapping.items():
            if excel_col in excel_data.columns:
                csv_data[csv_col] = excel_data[excel_col].fillna('').tolist()
            else:
                QMessageBox.critical(self, "오류", f"Excel 열 '{excel_col}'을 찾을 수 없습니다! 열 이름을 확인하세요.")
                return

        csv_df = pd.DataFrame(csv_data)
        csv_save_path, _ = QFileDialog.getSaveFileName(self, "CSV 파일 저장", "", "CSV files (*.csv)")
        if csv_save_path:
            try:
                csv_df.to_csv(csv_save_path, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
                QMessageBox.information(self, "성공", "CSV 파일이 성공적으로 만들어졌습니다!")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"CSV 파일을 저장하는데 실패했습니다: {e}")
