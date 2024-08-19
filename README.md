# CSV 툴 by 김재형

이 프로젝트는 Excel 파일을 CSV 파일로 변환하고, CSV 파일 간의 중복 제거 및 추출, 병합을 수행할 수 있는 GUI 도구를 제공합니다. PyQt5를 사용하여 직관적인 사용자 인터페이스를 제공하며, 다양한 CSV 관련 작업을 쉽게 수행할 수 있습니다.

## 주요 기능

- **Excel → CSV 변환**: Excel 파일의 열을 CSV 파일로 매핑하여 변환합니다.
- **CSV 중복 제거 및 추출**: 두 개의 CSV 파일을 비교하여 중복된 항목을 제거하거나 추출합니다.
- **CSV 병합**: 두 개의 CSV 파일을 공통 열을 기준으로 병합합니다.

## 사전 준비

이 프로젝트를 실행하려면 Python 3.x가 설치되어 있어야 합니다.

## 설치 방법

1. **레포지토리 클론**:

   ```bash
   git clone https://github.com/JaeHeong/csv_tool.git
   cd csv_tool
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
   python main.py
   ```

2. **독립 실행 가능한 실행 파일 생성** (선택 사항):
   애플리케이션을 독립 실행형 `.exe` 파일로 배포하려면:

   ```bash
   pyinstaller --onefile --windowed main.py
   ```

   생성된 실행 파일은 `dist/` 디렉토리에서 찾을 수 있습니다.

3. **애플리케이션 사용**:
   - **Excel → CSV 변환**:
     - "Excel → CSV 변환" 버튼을 클릭하여, Excel 파일에서 CSV 파일로 변환 작업을 수행할 수 있습니다.
     - CSV 열 이름과 해당하는 Excel 열 이름을 입력하여 원하는 매핑을 추가합니다.
     - "열 추가" 버튼을 사용하여 매핑을 추가할 수 있습니다.
     - "열 삭제" 버튼을 사용하여 마지막으로 추가한 매핑을 제거할 수 있습니다.
     - "CSV 생성" 버튼을 클릭하여 Excel 파일을 선택하고, CSV 파일을 생성합니다.
     - "현재값 저장" 버튼을 클릭하여 현재 값들을 저장합니다.
   
   - **CSV 중복 제거 및 추출**:
     - "CSV 중복 제거 및 추출" 버튼을 클릭하여, 두 개의 CSV 파일을 선택하고 중복된 항목을 제거하거나 추출할 수 있습니다.
     - 중복 제거 및 중복 추출된 결과를 새로운 CSV 파일로 저장할 수 있습니다.

   - **CSV 병합**:
     - "CSV 병합" 버튼을 클릭하여, 두 개의 CSV 파일을 공통 열을 기준으로 병합할 수 있습니다.
     - 병합된 결과를 새로운 CSV 파일로 저장할 수 있습니다.

## 프로젝트 구조

- `main.py`: 애플리케이션의 메인 진입점으로, 전체 UI와 기능을 관리합니다.
- `csv_converter.py`: Excel 파일을 CSV로 변환하는 기능을 담당하는 모듈입니다.
- `csv_deduplicator.py`: CSV 파일 간의 중복을 제거하거나 중복된 항목을 추출하는 기능을 담당하는 모듈입니다.
- `csv_merger.py`: 두 개의 CSV 파일을 병합하는 기능을 담당하는 모듈입니다.
- `requirements.txt`: 필요한 의존성 목록을 포함한 파일입니다.
- `README.md`: 프로젝트 개요와 사용법이 포함된 파일입니다.

## 의존성

- **pandas**: Excel 및 CSV 파일 작업을 처리하기 위해 사용됩니다.
- **PyQt5**: 애플리케이션의 그래픽 사용자 인터페이스를 제공합니다.
- **PyInstaller** (선택 사항): 독립 실행형 실행 파일을 생성하기 위해 사용됩니다.