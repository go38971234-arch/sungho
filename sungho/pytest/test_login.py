import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import login,save_screenshot






# -----------------------------
# TC1: 정상 로그인
# -----------------------------
def test_login_success(driver):
    print("\nTC13: 정상 로그인 테스트")
    login(driver,"qa3team03@elicer.com" ,"@qa12345")

    #상단에 유저 아이콘이 있는 지 확인
    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    #아이콘이 화면에 보이면 테스트 성공
    assert icon.is_displayed()
    print("TC13: 정상 로그인 테스트 성공")



#TC2: 잘못된 비밀번호

def test_wrong_password(driver):
    print("\nTC14: 잘못된 비밀번호 로그인 테스트")
    login(driver, "qa3team03@elicer.com", "!qa12345")

    #비밀번호 올바르지 않다는 문구 뜨는지 확인
    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Email or password does not match')]")
        )
    )
    # "Email or password does not match"라는 문구가 있으면 테스트 성공
    assert "Email or password does not match" in error.text
    print("TC14: 잘못된 비밀번호 로그인 테스트 성공")


# -----------------------------
# TC3: 8글자 미만 비밀번호
# -----------------------------
def test_short_password(driver):
    print("\nTC15: 8글자 미만 비밀번호 로그인 테스트")
    login(driver, "qateam03@alicer.com", "12345")

    # 최소 8글자 이상 입력해달라는 문구 뜨는지 확인
    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Please enter a password of at least 8 digits.')]")
        )
    )
    #at least 8 digits가 문구에 포함되어있으면 테스트 성공
    assert "at least 8 digits" in error.text
    print("TC15: 8글자 미만 비밀번호 로그인 테스트 성공")


# -----------------------------
# TC4: 미가입 계정 로그인
# -----------------------------
def test_nonexist_user_login(driver):
    print("\nTC16: 미가입 계정 로그인 테스트")
    login(driver, "nonexist@alicer.com", "@qa12345")

    try:
        error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'unsigned user')]")
        )
    )
        assert "unsigned user" in error.text #미등록된 유저 라는 문구가 있으면 테스트 통과
    except TimeoutException:
        print("TC016: 미가입 계정 로그인 테스트 실패")
        save_screenshot(driver, "signup_emmail", "TC16_nonexist_user_login_fail")
        pytest.fail("이메일이나 패스워드가 틀렸다는 메세지만 뜸, 미가입 계정인 지 알 수 없음")
