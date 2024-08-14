# Excel to CSV Mapper

이 프로젝트는 Excel 파일의 열을 CSV 파일로 매핑할 수 있는 GUI 도구를 제공합니다. 사용자는 Excel 파일에서 열을 선택하고, 원하는 열 매핑으로 CSV 파일을 생성할 수 있습니다.

## 주요 기능

- PyQt5로 구현된 간단하고 직관적인 GUI.
- 사용자가 동적으로 열 매핑을 추가 및 제거할 수 있습니다.
- UTF-8 인코딩과 적절한 인용을 사용하여 CSV 파일을 생성합니다.

## 사전 준비

이 프로젝트를 실행하려면 Python 3.x가 설치되어 있어야 합니다.

## 설치 방법

1. **레포지토리 클론**:

   ```bash
   git clone https://github.com/JaeHeong/excel_to_csv.git
   cd excel_to_csv
   ```

2. **가상 환경 생성 및 활성화** (선택 사항):

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Windows에서는: myenv\Scripts\activate
   ```

3. **필요한 Python 패키지 설치**:

   ```bash
   pip install -r requirements.txt
   ```

   만약 `requirements.txt` 파일이 없다면, 다음 명령어로 패키지를 수동으로 설치할 수 있습니다:

   ```bash
   pip install pandas pyqt5
   ```

## 사용 방법

1. **애플리케이션 실행**:

   ```bash
   python excel_to_csv_mapper.py
   ```

2. **독립 실행 가능한 실행 파일 생성** (선택 사항):
   애플리케이션을 독립 실행형 `.exe` 파일로 배포하려면:

   ```bash
   pyinstaller --onefile --windowed excel_to_csv_mapper.py
   ```

   생성된 실행 파일은 `dist/` 디렉토리에서 찾을 수 있습니다.

3. **애플리케이션 사용**:
   - CSV 열 이름과 해당하는 Excel 열 이름을 입력하여 원하는 매핑을 추가합니다.
   - "Add Mapping" 버튼을 사용하여 매핑을 추가할 수 있습니다.
   - "Remove Last Mapping" 버튼을 사용하여 마지막으로 추가한 매핑을 제거할 수 있습니다.
   - "Generate CSV" 버튼을 클릭하여 Excel 파일을 선택하고, CSV 파일을 생성합니다.

## 프로젝트 구조

- `excel_to_csv_mapper.py`: GUI 로직이 포함된 메인 Python 스크립트입니다.
- `README.md`: 프로젝트 개요와 사용법이 포함된 파일입니다.
- `.gitignore`: Git이 무시할 파일과 디렉토리를 지정합니다.
- `requirements.txt`: 필요한 의존성 목록을 포함한 파일입니다.

## 의존성

- **pandas**: Excel 및 CSV 파일 작업을 처리하기 위해 사용됩니다.
- **PyQt5**: 애플리케이션의 그래픽 사용자 인터페이스를 제공합니다.
- **PyInstaller** (선택 사항): 독립 실행형 실행 파일을 생성하기 위해 사용됩니다.
