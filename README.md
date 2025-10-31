# AI 웹 구조 네비게이터

## 1. 프로젝트 목표
시각장애인 사용자가 스크린리더를 사용할 때, 복잡한 웹사이트의 구조(메뉴, 본문, 광고 등)를 파악하기 어렵다는 문제를 해결하고자 했습니다.

본 프로젝트는 사용자가 웹사이트의 HTML 코드를 입력하면, Google Gemini AI가 이 구조를 분석하여 "오디오용 길안내" 스크립트를 생성하고, TTS(Text-to-Speech) 기술을 통해 실제 음성 파일로 출력하는 간단한 데모입니다.

## 2. 핵심 기능 및 사용 기술

이 프로젝트는 단순 API 호출을 넘어, BeautifulSoup 라이브러리를 이용한 불필요한 태그 제거 및 TTS 기술을 결합한 시스템입니다.

1. HTML 전처리 : `BeautifulSoup` 라이브러리를 사용해 원본 HTML에서 `<script>`, `<footer>` 등 불필요한 노이즈 태그를 제거하고, `<nav>`, `<main>` 등 핵심 태그만 추출합니다.
2. AI 분석 : Google Gemini 모델에게 전달하여, 프롬프트 엔지니어링 한 것의 지시에 따라 페이지 구조를 분석하고 텍스트 스크립트를 생성합니다.
3. 음성 출력 : AI가 생성한 텍스트 스크립트를 `gTTS` 라이브러리를 이용해 `.mp3` 음성 파일로 변환하고 재생합니다.

- Language : Python 3.8+
- Libraries : google-generativeai, gTTS, BeautifulSoup4, python-dotenv, Jupyter Notebook

3. ⚙️ 설치 및 환경 설정

1. 가상 환경 생성 및 라이브러리 설치
Python 가상 환경을 생성하고 필요한 라이브러리를 설치합니다.

### 가상 환경 생성 (Windows)
python -m venv venv
### 가상 환경 활성화 (Windows)
.\venv\Scripts\activate

### 가상 환경 생성 (Mac/Linux)
python3 -m venv venv
### 가상 환경 활성화 (Mac/Linux)
source venv/bin/activate

### 필수 라이브러리 설치
pip install google-generativeai gTTS python-dotenv jupyter beautifulsoup4

### 3. API 키 설 정
프로젝트 루트 폴더에 .env 파일을 생성하고, 1단계에서 발급받은 Google AI Studio의 API 키를 입력합니다.

## 4. 실행 방법
1. Jupyter Notebook 실행
2. `AI_Web_Navigator_Demo.ipynb` 노트북 파일을 열고, 각 셀을 순서대로 실행합니다.
3. HTML 코드를 입력하면, AI가 분석한 페이지 구조에 대한 오디오 가이드가 생성되어 재생됩니다.

## 5. 향후 개선점

1. 자동 웹 스크래핑 도입: 현재는 HTML을 수동으로 복사-붙여넣기 하지만, BeautifulSoup이나 Selenium 라이브러리를 도입하여 사용자가 URL만 입력하면 자동으로 HTML을 가져오도록 개선할 수 있습니다.

2. 동적 웹사이트 대응: JavaScript로 컨텐츠가 로드되는 최신 웹사이트(SPA 등)는 Selenium이나 Playwright 같은 동적 크롤링 도구를 사용해야 정확한 HTML 분석이 가능합니다.

3. 고품질 TTS API 연동: 현재 사용 중인 gTTS 대신, Google Cloud TTS (WaveNet)나 다른 유료 TTS API를 연동하여 훨씬 더 자연스럽고 듣기 편한 고품질 음성을 제공할 수 있습니다.

4. 브라우저 확장 프로그램 개발: 궁극적으로 이 기능을 Chrome/Firefox 확장 프로그램으로 패키징하여, 사용자가 실제 웹 서핑 중에 버튼 하나만 누르면 즉시 현재 페이지의 오디오 가이드를 들을 수 있도록 만들 수 있습니다.