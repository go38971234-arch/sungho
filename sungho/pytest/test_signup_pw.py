
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utills import (
    signup,
    save_screenshot,
    fill_signup_form,
    generate_unique_username,
    open_signup_page,
    submit_signup)


# TC05: 8자 미만 비밀번호 테스트
def test_short_password(driver):
    print("\n▶ TC005: 비밀번호 8자 미만 테스트")
    email = generate_unique_username() + "@naver.com"
    password = "@qa1234"   # 7자
    name = "김성호"

    signup(driver, email, password, name) #회원가입 입력필드에 입력값 넣고 약관체크, create account까지 한번에 해주는 함수

    
    error = WebDriverWait(driver, 5).until(   #create acoount 누른 뒤 오류 메시지 뜨는 지 확인
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
        )
    )

    assert "Please make your password stronger!" in error.text # 더 강하게 pw를 만들어라 라는 문구가 error.text에 있으면 테스트 성공 
    print("TC005 테스트 성공")


# TC06: 비밀번호 조합 규칙 테스트
def test_wrong_rule_password(driver):
    print("\n▶ TC006: 여러 비밀번호 조합 테스트")
    invalid_passwords = [
        "qa123456",   # 특수문자 없음
        "qa@qaqaqa",  # 숫자 없음
        "12345678"    # 숫자만
    ]

    open_signup_page(driver) #회원가입 창 열어주는 함수

    email = generate_unique_username() + "@naver.com" #임의로 테스트할 이메일을 만들어주는 함수
    name = "김성호"
    fill_signup_form(driver, email=email, name=name) #회원가입 입력필드에 입력과 이용약관까지 체크 해주는 함수. signup과는 다르다

    for password in invalid_passwords:
        password_input = driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']")
        password_input.send_keys(Keys.CONTROL, "a")
        password_input.send_keys(Keys.BACKSPACE)
        password_input.send_keys(password)  #invaild_passwords의 값 자동으로 초기화, 입력 반복 

        submit_signup(driver) #create account 버튼 누르는 함수 

        error = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
            )
        )

        save_screenshot(driver, "signup_pw", f"TC06_wrong_rule_{password}")
        assert "Please make your password stronger!" in error.text
        print("TC006 테스트 성공")


# TC07: 정상 비밀번호 입력
def test_right_password(driver,valid_signup_data): # valid_signup_data= confitest.py에서 fixture로 만들어놓은 데이터
    print("\n▶ TC007: 정상 비밀번호 입력 테스트")
    
    #회원가입창에 이메일, 비번, 이름 입력 후 약관 체크 후, create acoount 클릭
    signup(driver,**valid_signup_data)

    #url 바뀌는지 확인
    WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
    #아이콘이 상단에 뜨는지 확인
    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    #화면에 아이콘이 보이면 테스트 성공
    assert icon.is_displayed()
    print("TC007 테스트 성공")
    
