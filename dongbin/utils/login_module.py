# login_module.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 엘리스 로그인 페이지의 요소 이름을 사용합니다. (실제 페이지에 따라 다를 수 있음)
EMAIL_INPUT_NAME = "loginId"
PASSWORD_INPUT_NAME = "password"
LOGIN_BUTTON_SELECTOR = "button[type='submit']" 

def perform_login(driver: WebDriver, email: str, password: str):
   
    try:
        # WebDriverWait 설정: 요소가 나타날 때까지 명시적으로 기다립니다.
        wait = WebDriverWait(driver, 15)
        
        # 1. 이메일 입력 필드가 DOM에 나타날 때까지 기다립니다.
        email_field = wait.until(EC.presence_of_element_located((By.NAME, EMAIL_INPUT_NAME)))
        email_field.send_keys(email)
        
        # 2. 비밀번호 입력
        password_field = driver.find_element(By.NAME, PASSWORD_INPUT_NAME)
        password_field.send_keys(password)
        
        # 3. 로그인 버튼 클릭
        login_button = driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)
        login_button.click()
        
        time.sleep(3) # 로그인 후 페이지 전환 대기
        
        print(f"[SUCCESS] {email} 계정으로 로그인 완료.")
        
    except Exception as e:
        print(f"[ERROR] 로그인 실패: {e}")
        # 실패 시 디버깅을 위해 브라우저를 닫지 않고 유지합니다.