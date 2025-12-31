import time
import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.chat_utils import wait_for_AI_complete

LOGIN_URL = "https://qaproject.elice.io/ai-helpy-chat/tools/98b00265-c2fb-43cc-8785-5330e18f8c28"
#객관식 드롭다운
OPTION_TYPE_DROPDOWN = (By.ID, "mui-component-select-quiz_configs.0.option_type")
#난이도 드롭다운
DIFFICULTY_DROPDOWN = (By.ID, "mui-component-select-quiz_configs.0.difficulty")
#퀴즈 텍스트
QUIZ_TEXTAREA = (By.NAME, "content")
# 1차 버튼: sizeLarge 포함
FIRST_SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].MuiButton-sizeLarge")
# 2차 버튼: sizeMedium 포함
SECOND_SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit'].MuiButton-sizeMedium")
#생성 결과 최상위 div
QUIZ_RESULT_CONTAINER = (By.CSS_SELECTOR, "div.MuiStack-root.css-1id3s5p")

def select_dropdown_option(driver, dropdown_locator, option_text):
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.element_to_be_clickable(dropdown_locator))
    dropdown.click()
    time.sleep(0.5) 
    
    option_xpath = f"//li[@role='option' and contains(text(), '{option_text}')]"
    option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
    option.click()
    time.sleep(0.5)

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

try:
    #로그인 실행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    wait = WebDriverWait(driver, 10)

    print("--- 퀴즈 생성 생성 프로세스 시작 ---")
    
    # 유형 선택: '객관식 (단일 선택)'
    select_dropdown_option(driver, OPTION_TYPE_DROPDOWN, "객관식 (단일 선택)")
    print("[SUCCESS] 유형 선택 완료")

    # 난이도 선택: '하'
    select_dropdown_option(driver, DIFFICULTY_DROPDOWN, "하")
    print("[SUCCESS] 난이도 선택 완료")
    
    textarea = wait.until(EC.element_to_be_clickable(QUIZ_TEXTAREA))
    textarea.click()
    textarea.send_keys(Keys.CONTROL + "a")
    textarea.send_keys(Keys.BACKSPACE)
    print("기존 내용을 삭제했습니다.")
    
    textarea.send_keys("ISTQB")
    print(f"[SUCCESS] 주제 입력 완료: 'ISTQB'")
    
    print("\n--- 1차 생성 시작 ---")
    first_btn = wait.until(EC.element_to_be_clickable(FIRST_SUBMIT_BTN))
    
    # 클릭 방해를 피하기 위해 JavaScript 클릭 사용
    driver.execute_script("arguments[0].click();", first_btn)
    print("[SUCCESS] 1차 버튼 클릭 완료")

    # 1차 클릭 후 데이터가 한 번 나올 때까지 잠시 대기 및 이전 텍스트 저장
    time.sleep(3) 
    old_result_text = ""
    try:
        old_result_text = driver.find_element(*QUIZ_RESULT_CONTAINER).text
    except:
        pass
    
    print("\n--- 2차 '다시 생성' 대기 및 클릭 ---")
    # 버튼이 Medium 사이즈(SECOND_SUBMIT_BTN)로 바뀔 때까지 대기
    second_btn = wait.until(EC.presence_of_element_located(SECOND_SUBMIT_BTN))
    
    # 레이어가 가로막고 있을 확률이 높으므로 무조건 JavaScript로 클릭
    driver.execute_script("arguments[0].click();", second_btn)
    print("[SUCCESS] 2차 '다시 생성' 버튼 클릭 완료")

    # 3. 데이터 갱신 대기 (이전 텍스트와 달라질 때까지)
    print("새로운 퀴즈 데이터를 생성 중입니다...")
    
    
    
    
    
    try:
        # 이전 텍스트와 현재 텍스트가 다르고, '생성했습니다'라는 문구가 포함될 때까지 대기
        wait.until(lambda d: d.find_element(*QUIZ_RESULT_CONTAINER).text != old_result_text 
                   and "생성했습니다" in d.find_element(*QUIZ_RESULT_CONTAINER).text)
        
        # 텍스트가 완전히 뿌려질 시간을 2~3초 더 줌
        time.sleep(3)
        
        final_quiz_result = driver.find_element(*QUIZ_RESULT_CONTAINER).text
        print("\n--- [최종 데이터 수집 완료] ---")
        
    except Exception as e:
        print(f"[WARNING] 데이터 갱신 대기 중 타임아웃 혹은 오류 발생: {e}")
        final_quiz_result = driver.find_element(*QUIZ_RESULT_CONTAINER).text
    
    print("AI가 퀴즈를 생성 중입니다...")
    
    
    
    try:
        WebDriverWait(driver, 60).until(
            lambda d: d.find_element(*QUIZ_RESULT_CONTAINER).text != old_result_text 
            and len(d.find_element(*QUIZ_RESULT_CONTAINER).text) > 50
        )
        
        print("AI가 답변을 마무리하고 있습니다...")
        time.sleep(12)

        # 최종 결과 수집
        final_quiz_result = driver.find_element(*QUIZ_RESULT_CONTAINER).text
        print("\n--- [최종 데이터 수집 완료] ---")
        print(f"내용 요약: {final_quiz_result[:200].replace('\n', ' ')}...")

        # 6. JSON 데이터 구조화
        conversation_history = [{
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_input": "ISTQB 퀴즈 생성",
            "quiz_content": final_quiz_result,  # 수집된 전체 텍스트
            "config": {
                "type": "객관식 (단일 선택)",
                "difficulty": "하"
            }
        }]

        # 2. 파일 저장 경로 설정 (dongbin/results/quiz_gen_log.json)
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)
        file_path = os.path.join(results_dir, "quiz_gen_log.json")

        # 3. 기존 파일이 있으면 읽어와서 추가 저장(Append)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list): data = [data]
                except:
                    data = []
        else:
            data = []

        data.append(conversation_history[0])

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"\n[SUCCESS] 모든 프로세스 완료! 결과가 저장되었습니다: {file_path}")
    except Exception as e:
        print(f"[FAIL] 퀴즈 결과 영역을 찾을 수 없습니다: {e}")
        
    
except Exception as e:
  
        print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
        print(f"오류 클래스: {e.__class__.__name__}")
        print(f"오류 메시지: {e}")
        
# finally:
#     if 'driver' in locals() and driver:
#         # 최종 상태 확인을 위해 3초 대기 후 종료
#         driver.quit()
#         print("\n[INFO] 드라이버 종료.")