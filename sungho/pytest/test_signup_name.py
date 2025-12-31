from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import signup,generate_unique_username,save_screenshot


# TC08: 이름 미입력
def test_space_name(driver):
    print("\n▶ TC008: 이름 공란 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = ""

    signup(driver, email, password, name)

    #이름 공란시 나오는 문구 확인
    name_input = driver.find_element(By.XPATH, "//input[@placeholder='Name']")
    msg = driver.execute_script(
        "return arguments[0].validationMessage;", name_input
    )
    print("오류 메세지:", msg)
    #문구가 ""가 아니면 테스트 통과
    assert msg !=""
    print("TC008: 이름 공란 입력 테스트 성공")


# TC09: 이름 너무 김
def test_too_long_name(driver):
    print("\n▶ TC009: 긴 이름 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = "가나다라마바사아자차카타파하아야어여오유우이"

    signup(driver, email, password, name)
    save_screenshot(driver, "signup_name", "TC09_long_name_input")
    #이름이 너무 깁니다 라는 문구가 나오면 테스트 통과
    try:
        error =  WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'your name is too long')]")
        )
    )
        assert "too long" in error.text
        
        #이름이 너무 길다는 문구를 찾지 못한다면, 테스트 실패. 실패한 화면 스크린샷 찍음,실패한 원인 출력
    except TimeoutException:
        save_screenshot(driver, "signup_name", "TC09_long_name_fail")
        print("TC009: 긴 이름 입력 테스트 실패")
        pytest.fail("이름 길이 제한 에러 메시지 없음, 정상 계정처럼 로그인이 되어버림")


# TC10: 정상 이름
def test_right_name(driver,valid_signup_data):
    print("\n▶ TC010: 정상적인 이름 입력 테스트")

    signup(driver, **valid_signup_data)

    WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    assert icon.is_displayed()
    print("TC010: 정상적인 이름 입력 테스트 성공")
