import pytest
import os
from dotenv import load_dotenv # .env 로딩

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chatbot_tester import ChatBotTester # 챗봇 동작 로직 클래스
from saveJson_gunhoo import save_json # json 저장 유틸
from chat_test_cases import TEST_CASES # 질문목록

# -----------------------------
# 환경 변수 로드 (.env 파일 읽기)
# -----------------------------
load_dotenv()

# -----------------------------
# 로그인 정보 / URL 설정
# -----------------------------
USERNAME = os.getenv("ELICE_USERNAME")
PASSWORD = os.getenv("ELICE_PASSWORD")
LOGIN_URL = os.getenv("ELICE_LOGIN_URL")

# -----------------------------
# pytest 브라우저 생성 FIXTURE (파이테스트 - 테스트 이전 미리 준비하는 것)
# -----------------------------
@pytest.fixture(scope="session") 
def browser(): # 테스트 전체(session) 동안 사용할 브라우저를 1개 생성하는 함수
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.implicitly_wait(10) # 기본 암시적 대기 설정
    yield driver # yield 를 기준으로 위 setup, 밑 teardown 실행
    driver.quit() # 세션 종료 후 브라우저 자동 종료

# -----------------------------
# 자동 로그인 FIXTURE
# -----------------------------

@pytest.fixture(scope="session", autouse=True)
def test_login(browser): # 테스트 시작 시 자동으로 로그인 처리
    browser.get(LOGIN_URL)

    WebDriverWait(browser, 10).until(                           
        EC.presence_of_element_located((By.NAME, "loginId"))
    )

    browser.find_element(By.NAME, "loginId").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )


# -----------------------------
# 여러 질문을 자동 반복 테스트
# -----------------------------
@pytest.mark.parametrize("tc", TEST_CASES)
def test_chatbot_by_tc(browser, tc):
    tester = ChatBotTester(browser)

    results = []                        # 질문 답변 리스트

    for question in tc["questions"]:    # tc 안의 질문들을 순서대로 실행
        prev_count = len(tester.get_all_answers())  # 답변 개수 기록

        # 질문 전송
        tester.send_message(question)

        # 답변 대기                     
        tester.wait_for_answer(prev_answer_count=prev_count)

        # 답변 추출
        answer = tester.get_last_answer()   # 마지막 답변

        results.append({
            "question": question,
            "answer": answer
        })

        

    # TC 단위로 JSON 저장
    save_json(f"{tc['tc_id']}.json", {      # 파일명
        "tc_id": tc["tc_id"],               # 저장구조
        "results": results
    })

    # TC 종료 시 새 채팅 (개별 / 연속 공통)
    tester.new_chat()
    

    