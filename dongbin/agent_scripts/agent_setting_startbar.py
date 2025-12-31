import os
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.common_actions import click_make_button

from utils.driver_setup import login_driver
from utils.login_module import perform_login

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)



LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
STARTER_FIELD = (By.XPATH, '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]')
MAX_STARTERS = 4
ADDITIONAL_STARTERS = ["대중교통","서울", "맛집", "길 찾기"]

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)
print("--- 에이전트 생성 프로세스 시작 ---")
    
    #만들기 버튼 클릭
try:
    click_make_button(driver, wait_time=10)
 
    # 2. 4개 필드를 모두 생성 반복문
    for i in range(MAX_STARTERS): 
        current_starter_text = ADDITIONAL_STARTERS[i]
        expected_count = i + 1 
        
        def specific_field_appears(driver: WebDriver):
            elements = driver.find_elements(*STARTER_FIELD)
    
            if len(elements) >= expected_count and elements[i].is_displayed():
                return elements[i]
            return False

        current_field = WebDriverWait(driver, 5).until(
            specific_field_appears,
            message=f"{expected_count}번째 필드가 5초 내에 나타나지 않았습니다."
        )

        # 2-2. 대화 입력
        current_field.send_keys(current_starter_text)
        print(f"[SUCCESS] {expected_count}번째 시작 대화 입력 성공: '{current_starter_text}'")

        if expected_count < MAX_STARTERS:    
            next_expected_count = expected_count + 1
            def next_field_appears(driver: WebDriver):
                elements = driver.find_elements(*STARTER_FIELD)
                return len(elements) >= next_expected_count

  
            WebDriverWait(driver, 3).until(
                next_field_appears,
                message=f"{next_expected_count}번째 필드가 3초 내에 나타나지 않았습니다."
            )
            print(f"[INFO] {next_expected_count}번째 입력 필드 출현 확인.")
            
    
    # 최종 필드 개수 확인
    final_fields = driver.find_elements(*STARTER_FIELD)
    final_count = len(final_fields)
    
    if final_count == MAX_STARTERS:
        print(f"\n[PASS] 최종적으로 {MAX_STARTERS}개 필드 생성 확인.")
       
        time.sleep(1) 
        current_count = len(driver.find_elements(*STARTER_FIELD))
        
        if current_count == MAX_STARTERS:
            print(f"[PASS] {MAX_STARTERS}개 초과 시 필드 추가 생성 제한 확인.")
        else:
            print(f"[FAIL] {MAX_STARTERS}개 초과 제한 실패! 현재 필드 개수: {current_count}")
    else:
        print(f"[FAIL] 최종 필드 개수가 {MAX_STARTERS}개가 아닙니다. (현재 {final_count}개)")
        
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")