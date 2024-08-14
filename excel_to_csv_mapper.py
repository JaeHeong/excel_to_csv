import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
import csv  # csv 모듈을 임포트

class ExcelToCSVMapper(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CSV 변환툴 by 김재형")
        self.setGeometry(100, 100, 800, 600)
        
        self.csv_columns = []
        self.excel_columns = []

        layout = QVBoxLayout()

        # 테이블 위젯 생성
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["CSV 컬럼명", "Excel 컬럼명"])
        self.table.setShowGrid(True)  # 셀 구분을 위한 그리드 선 표시
        layout.addWidget(self.table)

        # 매핑 추가/삭제 버튼
        add_button = QPushButton("열 추가")
        add_button.clicked.connect(self.add_mapping)
        layout.addWidget(add_button)

        remove_button = QPushButton("열 삭제")
        remove_button.clicked.connect(self.remove_mapping)
        layout.addWidget(remove_button)

        # CSV 생성 버튼
        generate_button = QPushButton("CSV 생성")
        generate_button.clicked.connect(self.generate_csv)
        layout.addWidget(generate_button)

        self.setLayout(layout)
        self.add_mapping()  # 기본적으로 하나의 매핑 항목 추가

    def add_mapping(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # 입력 가능한 셀 생성
        csv_item = QTableWidgetItem("")
        excel_item = QTableWidgetItem("")
        
        self.table.setItem(row_position, 0, csv_item)
        self.table.setItem(row_position, 1, excel_item)

    def remove_mapping(self):
        row_position = self.table.rowCount()
        if row_position > 0:
            self.table.removeRow(row_position - 1)

    def generate_csv(self):
        excel_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel files (*.xlsx)")
        if not excel_path:
            return

        try:
            excel_data = pd.read_excel(excel_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load Excel file: {e}")
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
                QMessageBox.critical(self, "Error", f"Excel column '{excel_col}' not found! Please check the column name.")
                return

        csv_df = pd.DataFrame(csv_data)
        csv_save_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV files (*.csv)")
        if csv_save_path:
            try:
                csv_df.to_csv(csv_save_path, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
                QMessageBox.information(self, "성공", "CSV 파일이 성공적으로 만들어졌습니다!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelToCSVMapper()
    window.show()
    sys.exit(app.exec_())
