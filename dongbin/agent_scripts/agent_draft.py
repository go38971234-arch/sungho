import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

#초안 선택자 구분을 위해 일정값x
agent_name = f"test_{int(time.time())}"
agent_text = "test입니다."
agent_rule = "test"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
NAME_INPUT = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
RULE_TEXTAREA = (By.NAME, 'systemPrompt')
BACK_BUTTON = (By.XPATH, "//button[@aria-label='뒤로가기']")
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")


#초안 선택자
DRAFT_CARD_LOCATOR = (By.XPATH, f"//a[contains(@class, 'MuiCard-root')]//p[text()='{agent_name}']/ancestor::a//span[normalize-space()='초안']")


driver = login_driver(LOGIN_URL) 
driver.maximize_window()

#초안저장 확인

try:
    #로그인 실행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    wait = WebDriverWait(driver, 10)

    print("--- 에이전트 생성 프로세스 시작 ---")
    
    
    
    #만들기 버튼 클릭
    agent_btn = wait.until(EC.element_to_be_clickable(MY_AGENTS_BUTTON))
    
    agent_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")
    
    wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
    print("[INFO] '/mine' 페이지로 이동 확인.")

    time.sleep(1)
    
    make_btn = wait.until(EC.element_to_be_clickable(MAKE_BUTTON))
    make_btn.click()  
    print("[SUCCESS] 만들기 버튼 클릭 완료")
    
    #이름 입력
    name_field = wait.until(EC.visibility_of_element_located(NAME_INPUT))
    name_field.clear()
    name_field.send_keys(agent_name)
    print("[SUCCESS] 이름 입력 완료")
    
    #한줄소개입력
    summary_field = wait.until(EC.visibility_of_element_located(SUMMARY_INPUT))
    summary_field.clear()
    summary_field.send_keys(agent_text)
    print("[SUCCESS] 한 줄 소개 입력 완료")
    
    #규칙입력
    rule_field = wait.until(EC.visibility_of_element_located(RULE_TEXTAREA))
    rule_field.clear()
    rule_field.send_keys(agent_rule)
    print("[SUCCESS] 규칙 입력 완료")
    
    #저장 하기도 전에 뒤로가기를 눌러서 1초 대기 걸어둠
    time.sleep(1)
    
    #뒤로가기 클릭
    back_btn = wait.until(EC.element_to_be_clickable(BACK_BUTTON))
    back_btn.click()
    print("[INFO] '뒤로가기' 버튼 클릭.")
    
    wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
    print("[INFO] 에이전트 목록 페이지로 복귀 확인.")
    
    wait_long = WebDriverWait(driver, 30)
 
    private_view = wait_long.until(EC.visibility_of_element_located(DRAFT_CARD_LOCATOR))
    
    print(f"\n[PASS] 에이전트 저장 테스트 성공! 에이전트 '{agent_name}'의 '초안' 상태 확인 완료.")
    
except TimeoutException:
    print(f"\n[FAILURE] '{agent_name}' 이름의 '초안'을 찾지 못했습니다. (30초 대기 시간 초과)")
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 최종 상태 확인을 위해 3초 대기 후 종료
        time.sleep(3) 
        driver.quit()
        print("\n[INFO] 드라이버 종료.")