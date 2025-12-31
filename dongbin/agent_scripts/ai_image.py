import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

# --- 설정 및 선택자 ---
TARGET_URL = "https://qaproject.elice.io/ai-helpy-chat"
PLUS_BUTTON = (By.CSS_SELECTOR, "div.e1826rbt2 button")
IMAGE_GEN_MENU = (By.XPATH, "//span[contains(text(), '이미지 생성')]")
TEXTAREA = (By.NAME, "input")
# 생성된 이미지가 담기는 컨테이너
IMAGE_RESULT = (By.CSS_SELECTOR, "div.elice-aichat__markdown img")

driver = login_driver(TARGET_URL)
driver.maximize_window()

try:
    # 1.로그인 수행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    wait = WebDriverWait(driver, 20)
    print(f"접속 완료: {driver.current_url}")

    # 2.+ 버튼 클릭
    print("--- 이미지 생성 도구 진입 시작 ---")
    plus_btn = wait.until(EC.element_to_be_clickable(PLUS_BUTTON))
    plus_btn.click()
    print("[SUCCESS] '+' 버튼 클릭 완료")

    # 3.'이미지 생성' 메뉴 클릭
    image_menu = wait.until(EC.element_to_be_clickable(IMAGE_GEN_MENU))
    image_menu.click()
    print("[SUCCESS] '이미지 생성' 모드 선택 완료")

    # 4.'사과' 입력 및 엔터
    print("\n--- 프롬프트 입력 시작 ---")
    input_box = wait.until(EC.element_to_be_clickable(TEXTAREA))
    
    input_box.send_keys("사과")
    input_box.send_keys(Keys.ENTER)
    print("[SUCCESS] 프롬프트('사과') 전송 완료")

    # 5. 이미지 생성 대기 및 확인
    print("AI가 이미지를 생성 중입니다. (약 30초 대기)...")
    
    # 이미지가 생성되어 화면에 나타날 때까지 대기
    try:
      
        generated_image = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(IMAGE_RESULT)
        )
        
        # 이미지의 주소 가져오기
        image_url = generated_image.get_attribute("src")
        print("\n--- [이미지 생성 성공] ---")
        print(f"이미지 경로: {image_url}")
        
    except Exception as e:
        print(f"[FAIL] 이미지 생성 확인 실패 또는 타임아웃: {e}")

except Exception as e:
    print(f"\n[CRITICAL ERROR] {e}")
    
finally:
    driver.quit()