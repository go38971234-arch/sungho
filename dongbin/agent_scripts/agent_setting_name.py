import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.common_actions import click_make_button


VALID_NAME = "동빈"
LONG_NAME = "0"*101
VALIDATION_MESSAGE_TEXT = "이름은 최대 100자입니다"
VALIDATION_XPATH = f"//*[contains(text(), '{VALIDATION_MESSAGE_TEXT}')]"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)

agent_make_btn = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
print("--- 에이전트 생성 프로세스 시작 ---")

try:    
    click_make_button(driver, wait_time =10)
       
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )
    
    # 3. 이름 정상 입력과 비정상 입력(101자)
    agent_make_name.send_keys(LONG_NAME)
    print(f"[SUCCESS] 1차 이름 입력 성공! ({len(LONG_NAME)}자 입력 완료)")
    
    validation_message = wait.until(
        EC.presence_of_element_located((By.XPATH, VALIDATION_XPATH))
    )
    
    print(f"[VALIDATION SUCCESS] 길이 제한 메시지 확인: '{VALIDATION_MESSAGE_TEXT}'")
       
    agent_make_name.send_keys(Keys.CONTROL, "a")
    agent_make_name.send_keys(Keys.DELETE)
    
    agent_make_name.send_keys(VALID_NAME)
    print("[SUCCESS] 2차 이름 입력 성공.")
    
    wait.until(
        EC.invisibility_of_element_located((By.XPATH, VALIDATION_XPATH))
    ) 
    
    print("[SUCCESS] 유효성 검사 메시지 사라짐 확인 완료.")
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")

finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")    
    
    

