import google.generativeai as genai     # 제미나이 API 호출
from gtts import gTTS                   # Google Test - to - Speech
import os                               # 환견 변스 접근
from dotenv import load_dotenv          # .env파일 로드
# from IPython.display import display, Audio, Markdown # .py 에서는 사용하지 않음
from bs4 import BeautifulSoup           # 전처리용

# API 키 설정
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    # 키가 없는 경우 에러 메시지
    print( "API 키 파일을 찾을 수 없습니다")

else:
    try:
        # API 키로 제미나이 설정
        genai.configure(api_key=API_KEY)
        print("API 키 및 라이브러리 설정 완료") # display(Markdown(...)) -> print(...)
    except Exception as e :
        print(f"API 키 설정 중 오류 발생: {e}")

print("--- 💡 내 API 키로 사용 가능한 모델 목록 ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"모델 목록 조회 중 오류: {e}") # genai.configure가 실패했을 경우를 대비
print("---------------------------------------")

model = None # model 변수 초기화
try:
    # 설정한 모델 로드.
    model = genai.GenerativeModel('models/gemini-pro-latest')
    print(f"{model.model_name} 로드 완료") # display(Markdown(...)) -> print(...)
except Exception as e :
    print(f"모델 불러오는 중 오류 발생, 오류 -> {e}")

# 프롬프트 엔지니어링
# 웹 접근성 전문가 역할 부여
# html을 분석해 '오디오 스크립트'를 생성하도록 지시.
def create_navigation_prompt(html_code):
    # 전처리된 HTML을 받습니다.
    return f"""
    당신은 20년 경력의 '웹 접근성 전문가'입니다.
    당신의 임무는 시각장애인 사용자를 위해, 이 복잡한 HTML 소스 코드를 분석하여 '오디오 네비게이션 가이드'를 생성하는 것입니다.

    [규칙]
    1.  당신은 전처리되어 '핵심'만 남은 HTML (nav, main 등)을 받았습니다.
    2.  `<nav>`, `<main>`, `<h1>`, `<h2>` 태그를 중심으로 분석하세요.

    [HTML 소스 코드]
    {html_code} # 전처리가 되었으니 3만자 한도도 제거

    [출력 포맷]
    위 HTML을 분석하여, 아래 4가지 질문에 대한 답변을 '오디오 스크립트' 형식으로만 생성해주세요. (그 외의 설명이나 인사말은 절대 넣지 마세요.)

    1.  페이지 제목 (Title): 이 페이지의 `<h1>` 또는 `<title>` 태그에 기반한 핵심 주제가 무엇인가요?
    2.  메인 메뉴 (Navigation): `<nav>` 태그 안의 주요 메뉴 항목(링크 텍스트)을 최대 5개까지 알려주세요.
    3.  핵심 본문 요약 (Main Summary): `<main>` 또는 `<article>` 태그 내부의 첫 번째 문단을 2~3문장으로 요약해주세요.
    """

input_file_path = 'inputHtml.html'  # 분석할 파일 이름
html_input = ""                     # 원본 HTML
html_cleaned = ""                   # 전처리한 HTML

try:
    # 1. 파일 읽기
    with open(input_file_path, 'r', encoding='utf-8') as f:
        html_input = f.read()

    if not html_input.strip():
        print(f"{input_file_path} 파일이 비어있음") # display(Markdown(...)) -> print(...)
    else:
        print(f"{input_file_path} 파일 읽기 성공(원본 크기 : {len(html_input)}") # display... -> print
        print(" 전처리 시작 ........") # display... -> print

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(html_input, 'html.parser')

        # 불필요한 태그 제거
        for tag in soup(["script", "style", "footer", "aside", "form", "button"]):
            tag.decompose()

        # 필요한 태그만 남김
        # 만약 <main>태그가 있으면 사용, else-> <body>전체 쓴다
        main_content = soup.find("main")
        nav_content = soup.find("nav")
        # 꺠끗한 HTML 조각을 모을 리스트
        cleaned_parts = []

        # <nav> 태그 내용 추가
        if nav_content:
            cleaned_parts.append(str(nav_content))

        # <main> 태그 내용 추가
        if main_content:
            cleaned_parts.append(str(main_content))

        elif soup.body:
            # <main>이 없다면, <body>에서 불필요한 걸 뺀 나머지 사용
            cleaned_parts.append(str(soup.body))
        else:
            # <main>, <body> 둘 다 없으면 그냥 원본의 축소판을 씀
            cleaned_parts.append(soup.get_text(separator="\n", strip=True)[:5000])

        # 전처리 된 데이터를 'html_cleaned'에 저장.
        html_cleaned = "\n".join(cleaned_parts)

        print(f"전처리 완료 (크기 : {len(html_cleaned)}") # display... -> print

except FileNotFoundError:
    print(f"'{input_file_path}' 파일을 찾을 수 없습니다.") # display... -> print
except Exception as e:
    print(f"파일 읽기 또는 전처리 중 오류 발생 -> {e}")

ai_script = ""
# 전처리 html 존재하고, 모델 로드 성공 시 AI 호출
if html_cleaned.strip() and model:
    try:
        print("제미나이가 HTML 구조 분석 중.....") # display... -> print
        # 전처리 데이터 담은 변수 -> 프롬프트 함수에 전달
        prompt = create_navigation_prompt(html_cleaned)
        response = model.generate_content(prompt)
        # 분석 결과
        ai_script = response.text
        print("-----분석 결과--------") # display... -> print
        print(ai_script) # display(Markdown(ai_script)) -> print(ai_script)

    except Exception as e :
        print(f"분석 중 오류 발생 -> {e}")
elif not model:
    print("모델 로드에 실패하여 AI 분석을 실행할 수 없습니다.")
else:
    print("현재 HTML 파일이 비어 있어 호출 실패.") # display... -> print

tts_file_path = 'web_summary.mp3'

# ai가 생성한 텍스트 스크립트가 존재 시 만 실행
if ai_script:
    try:
        print("HTML 분석 결과 음성으로 변환 중 ......"); # display... -> print

        # ai_script를 gTTS로 넘겨 mp3 파일로 저장.
        tts = gTTS(text=ai_script, lang='ko')
        tts.save(tts_file_path)

        print("mp3파일 생성 완료!!!!") # display... -> print

        # .py 에서는 자동 재생이 안되므로, 파일 생성 위치를 알려줍니다.
        print(f"'{os.path.abspath(tts_file_path)}' 파일이 생성되었습니다. 직접 열어서 확인해주세요.")

    except Exception as e :
        print(f"음성 변환 중 오류 발생 -> {e}")
else :
    print("AI 스크립트가 없어 음성 변환 실행 안함.") # display... -> print