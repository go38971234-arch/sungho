### 이미지 생성 테스트

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

# --- 변수명 및 선택자 유지 ---
TARGET_URL = "https://qaproject.elice.io/ai-helpy-chat"
PLUS_BUTTON = (By.CSS_SELECTOR, "div.e1826rbt2 button")
IMAGE_GEN_MENU = (By.XPATH, "//span[contains(text(), '이미지 생성')]")
TEXTAREA = (By.NAME, "input")

IMAGE_RESULT = (By.CSS_SELECTOR, "div.elice-aichat__markdown img")

def test_ai_image_generation(driver):
    """AI 이미지 생성 도구 진입 및 이미지 생성 결과 검증 테스트"""
    # 이미지 생성은 시간이 걸리므로 넉넉하게 45초 대기 사용
    wait = WebDriverWait(driver, 20)
    wait_long = WebDriverWait(driver, 45)

    # 1. 페이지 접속
    driver.get(TARGET_URL)
    print(f"\n[INFO] 접속 완료: {driver.current_url}")

    # 2. + 버튼 클릭
    print("--- 이미지 생성 도구 진입 시작 ---")
    plus_btn = wait.until(EC.element_to_be_clickable(PLUS_BUTTON))
    plus_btn.click()
    print("[SUCCESS] '+' 버튼 클릭 완료")

    # 3. '이미지 생성' 메뉴 클릭
    image_menu = wait.until(EC.element_to_be_clickable(IMAGE_GEN_MENU))
    image_menu.click()
    print("[SUCCESS] '이미지 생성' 모드 선택 완료")

    # 4. '사과' 입력 및 엔터
    print("\n--- 프롬프트 입력 시작 ---")
    input_box = wait.until(EC.element_to_be_clickable(TEXTAREA))
    input_box.send_keys("사과")
    input_box.send_keys(Keys.ENTER)
    print("[SUCCESS] 프롬프트('사과') 전송 완료")

    # 5. 이미지 생성 대기 및 확인
    print("[WAIT] AI가 이미지를 생성 중입니다. (최대 45초 대기)...")
    
    try:
        # 이미지가 생성되어 화면에 나타날 때까지 대기
        generated_image = wait_long.until(
            EC.visibility_of_element_located(IMAGE_RESULT)
        )
        
  
        image_url = generated_image.get_attribute("src")
        
        assert generated_image.is_displayed(), "생성된 이미지가 화면에 보이지 않습니다."
       
        assert image_url, "이미지 URL(src)이 비어있습니다."
        
        print("\n--- [이미지 생성 성공] ---")
        print(f"이미지 경로: {image_url[:60]}...") # 

    except TimeoutException:
     
        driver.save_screenshot("image_gen_failed.png")
        pytest.fail(f"[FAIL] 45초 이내에 이미지 생성 결과를 찾을 수 없습니다. (선택자: {IMAGE_RESULT[1]})")