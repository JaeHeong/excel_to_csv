import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
import csv

class CSVDeduplicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CSV 중복 제거 by 김재형")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # 홈 버튼
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        # home_button.setFixedSize(100, 40)  # 버튼 크기 조정
        main_layout.addWidget(home_button, alignment=Qt.AlignCenter)

        # 설명 라벨
        self.description_label = QLabel(
            "1. 첫 번째 CSV 파일을 선택하면 왼쪽에 표시됩니다.\n"
            "2. 두 번째 CSV 파일을 선택하면 오른쪽에 표시됩니다.\n"
            "3. 중복 제거 또는 중복 추출 버튼을 클릭하여 결과를 저장하세요.",
            self
        )
        self.description_label.setAlignment(Qt.AlignLeft)
        self.description_label.setStyleSheet("font-size: 14px; color: #333;")
        main_layout.addWidget(self.description_label, alignment=Qt.AlignCenter)

        # CSV 파일 표시 레이아웃
        file_layout = QHBoxLayout()

        # 첫 번째 CSV 파일 테이블
        self.table_a = QTableWidget()
        self.table_a.setColumnCount(5)  # 임시로 열 개수를 5로 설정
        self.table_a.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3", "Column 4", "Column 5"])
        file_layout.addWidget(self.table_a)

        # 두 번째 CSV 파일 테이블
        self.table_b = QTableWidget()
        self.table_b.setColumnCount(5)  # 임시로 열 개수를 5로 설정
        self.table_b.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3", "Column 4", "Column 5"])
        file_layout.addWidget(self.table_b)

        main_layout.addLayout(file_layout)

        # CSV 파일 선택 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 첫 번째 CSV 파일 선택 버튼
        open_button_a = QPushButton("첫 번째 CSV 파일")
        open_button_a.clicked.connect(self.open_csv_a)
        button_layout.addWidget(open_button_a, alignment=Qt.AlignCenter)

        # 중복 제거 버튼
        dedup_button = QPushButton("중복 제거")
        dedup_button.clicked.connect(self.deduplicate_csv)
        button_layout.addWidget(dedup_button, alignment=Qt.AlignCenter)

        # 중복 추출 버튼
        extract_button = QPushButton("중복 추출")
        extract_button.clicked.connect(self.extract_duplicates)
        button_layout.addWidget(extract_button, alignment=Qt.AlignCenter)

        # 두 번째 CSV 파일 선택 버튼
        open_button_b = QPushButton("두 번째 CSV 파일")
        open_button_b.clicked.connect(self.open_csv_b)
        button_layout.addWidget(open_button_b, alignment=Qt.AlignCenter)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def go_home(self):
        main_window = self.parent().parent()
        main_window.stack.setCurrentWidget(main_window.main_widget)

    def open_csv_a(self):
        csv_a_path, _ = QFileDialog.getOpenFileName(self, "첫 번째 CSV 파일 선택", "", "CSV files (*.csv)")
        if csv_a_path:
            self.load_csv_to_table(csv_a_path, self.table_a)

    def open_csv_b(self):
        csv_b_path, _ = QFileDialog.getOpenFileName(self, "두 번째 CSV 파일 선택", "", "CSV files (*.csv)")
        if csv_b_path:
            self.load_csv_to_table(csv_b_path, self.table_b)

    def load_csv_to_table(self, file_path, table_widget):
        try:
            # NaN 대신 빈 문자열로 읽어들이도록 설정
            df = pd.read_csv(file_path, keep_default_na=False, na_filter=False)
            table_widget.setRowCount(df.shape[0])
            table_widget.setColumnCount(df.shape[1])
            table_widget.setHorizontalHeaderLabels(df.columns)

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
        except Exception as e:
            QMessageBox.critical(self, "오류", f"CSV 파일을 불러오는데 실패했습니다: {e}")

    def deduplicate_csv(self):
        if self.table_a.rowCount() == 0 or self.table_b.rowCount() == 0:
            QMessageBox.critical(self, "오류", "두 개의 CSV 파일을 모두 선택하세요.")
            return

        df_a = self.get_df_from_table(self.table_a)
        df_b = self.get_df_from_table(self.table_b)

        try:
            # 중복된 행 제거
            df_result = df_a[~df_a.isin(df_b.to_dict(orient='list')).all(axis=1)]

            # 결과 CSV 파일 저장
            save_path, _ = QFileDialog.getSaveFileName(self, "결과 CSV 파일 저장", "", "CSV files (*.csv)")
            if save_path:
                df_result.to_csv(save_path, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
                QMessageBox.information(self, "성공", "중복 제거가 완료된 CSV 파일이 저장되었습니다!")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"CSV 파일을 처리하는데 실패했습니다: {e}")

    def extract_duplicates(self):
        if self.table_a.rowCount() == 0 or self.table_b.rowCount() == 0:
            QMessageBox.critical(self, "오류", "두 개의 CSV 파일을 모두 선택하세요.")
            return

        df_a = self.get_df_from_table(self.table_a)
        df_b = self.get_df_from_table(self.table_b)

        try:
            # 중복된 행 추출
            df_duplicates = df_a[df_a.isin(df_b.to_dict(orient='list')).all(axis=1)]

            # 결과 CSV 파일 저장
            save_path, _ = QFileDialog.getSaveFileName(self, "중복된 부분 CSV 파일 저장", "", "CSV files (*.csv)")
            if save_path:
                df_duplicates.to_csv(save_path, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
                QMessageBox.information(self, "성공", "중복된 부분이 저장된 CSV 파일이 생성되었습니다!")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"CSV 파일을 처리하는데 실패했습니다: {e}")

    def get_df_from_table(self, table_widget):
        rows = table_widget.rowCount()
        cols = table_widget.columnCount()
        data = []

        for i in range(rows):
            row_data = []
            for j in range(cols):
                item = table_widget.item(i, j)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        df = pd.DataFrame(data, columns=[table_widget.horizontalHeaderItem(j).text() for j in range(cols)])
        return df
