# 메모리 관리 문제가 있어서 일단 보류
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLineEdit, QLabel
from PyQt5.QtCore import Qt
import dask.dataframe as dd

class CSVDeduplicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CSV 중복 제거 by 김재형")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 홈 버튼
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_home)
        layout.addWidget(home_button, alignment=Qt.AlignCenter)

        # 식별자 입력 (폼 스타일)
        identifier_label = QLabel("식별자(열 일치 기준) help. 비우면 모든 열 값 비교")
        layout.addWidget(identifier_label, alignment=Qt.AlignCenter)

        self.identifier_input = QLineEdit()
        layout.addWidget(self.identifier_input, alignment=Qt.AlignCenter)

        # 파일 선택 버튼 레이아웃
        file_layout = QVBoxLayout()

        load_a_button = QPushButton("중복을 제거할 CSV 파일 선택")
        load_a_button.clicked.connect(self.load_csv_a)
        file_layout.addWidget(load_a_button, alignment=Qt.AlignCenter)

        load_b_button = QPushButton("제거해야 값이 있는 CSV 파일 선택")
        load_b_button.clicked.connect(self.load_csv_b)
        file_layout.addWidget(load_b_button, alignment=Qt.AlignCenter)

        layout.addLayout(file_layout)

        # 중복 제거 버튼
        deduplicate_button = QPushButton("중복 제거 및 CSV 생성")
        deduplicate_button.clicked.connect(self.deduplicate_csv)
        layout.addWidget(deduplicate_button, alignment=Qt.AlignCenter)

        self.csv_a = None
        self.csv_b = None

        self.setLayout(layout)

    def go_home(self):
        main_window = self.parent().parent()
        main_window.stack.setCurrentWidget(main_window.main_widget)

    def load_csv_a(self):
        csv_a_path, _ = QFileDialog.getOpenFileName(self, "중복을 제거할 CSV 파일 선택", "", "CSV files (*.csv)")
        if csv_a_path:
            try:
                self.csv_a = pd.read_csv(csv_a_path)
                QMessageBox.information(self, "성공", "원본 CSV 파일을 성공적으로 불러왔습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"원본 CSV 파일을 불러오는데 실패했습니다: {e}")

    def load_csv_b(self):
        csv_b_path, _ = QFileDialog.getOpenFileName(self, "제거해야 값이 있는 CSV 파일 선택", "", "CSV files (*.csv)")
        if csv_b_path:
            try:
                self.csv_b = pd.read_csv(csv_b_path)
                QMessageBox.information(self, "성공", "제거해야 값이 있는 CSV 파일을 성공적으로 불러왔습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"제거해야 값이 있는 CSV 파일을 불러오는데 실패했습니다: {e}")

    def deduplicate_csv(self):
        if self.csv_a is None or self.csv_b is None:
            QMessageBox.critical(self, "오류", "먼저 CSV 파일을 모두 선택해주세요.")
            return

        identifier = self.identifier_input.text().strip()

        # Dask 데이터프레임으로 로드
        ddf_a = dd.from_pandas(self.csv_a, npartitions=4)
        ddf_b = dd.from_pandas(self.csv_b, npartitions=4)

        if identifier:  # 식별자가 제공된 경우
            if identifier not in ddf_a.columns or identifier not in ddf_b.columns:
                QMessageBox.critical(self, "오류", f"식별자 '{identifier}'이(가) CSV 파일에 존재하지 않습니다.")
                return
            duplicated_rows = ddf_a[ddf_a[identifier].isin(ddf_b[identifier])].compute()
            non_duplicated_a = ddf_a[~ddf_a[identifier].isin(ddf_b[identifier])].compute()
        else:  # 식별자가 제공되지 않은 경우
            # 메모리 절약을 위해 필요한 열만 가져오기
            selected_columns = ddf_a.columns.intersection(ddf_b.columns).tolist()
            ddf_a = ddf_a[selected_columns]
            ddf_b = ddf_b[selected_columns]

            duplicated_rows = dd.merge(ddf_a, ddf_b, how='inner').compute()
            non_duplicated_a = dd.concat([ddf_a, duplicated_rows]).drop_duplicates(keep=False).compute()

        if duplicated_rows.empty:
            QMessageBox.information(self, "결과", "중복된 항목이 없습니다.")
            return

        # 중복된 항목 제거된 A 파일 저장
        save_path_a, _ = QFileDialog.getSaveFileName(self, "중복 제거된 CSV 파일 저장", "", "CSV files (*.csv)")
        if save_path_a:
            non_duplicated_a.to_csv(save_path_a, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
            QMessageBox.information(self, "성공", "중복 제거된 CSV 파일을 성공적으로 저장했습니다.")

        # 중복된 항목 저장
        save_path_dup, _ = QFileDialog.getSaveFileName(self, "삭제한 항목 CSV 파일 저장", "", "CSV files (*.csv)")
        if save_path_dup:
            duplicated_rows.to_csv(save_path_dup, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
            QMessageBox.information(self, "성공", "삭제한 항목을 성공적으로 저장했습니다.")
