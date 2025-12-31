from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utills import (
    open_signup_page,
    fill_signup_form,
    type_text,
)

# ------------------------
# 체크박스 테스트 공통 입력 함수
# ------------------------
def checkbox_fill_signup(driver, email=None, password=None, name=None):
    if email is not None:
        type_text(driver, "Email", email)
    if password is not None:
        type_text(driver, "Password", password)
    if name is not None:
        type_text(driver, "Name", name)


# ------------------------
# TC11: 약관 전체 동의 시 가입 가능
# ------------------------
def test_agree_all_check(driver,valid_signup_data):
    print("TC11: agree all 체크하기")

    open_signup_page(driver) #회원가입 창으로 이동

    fill_signup_form(driver, **valid_signup_data)#회원가입 창에서 유효한 이메일, 비번, 이름 입력 휴 이용약관까지 클릭해줌

    create_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Create account')]") #Create account라는 문구가 있는 버튼이 있는지 찾음
        )
    )

    assert create_btn.is_enabled()# 화면에 보이면 테스트 통과
    print("✔ Create account 버튼 활성화 확인")


# ------------------------
# TC12: 필수 항목 미동의 시 가입 불가
# ------------------------
def test_required_option_unchecked(driver,valid_signup_data):
    print("TC12: 필수 항목 미동의 시 가입 불가")

    open_signup_page(driver)

    checkbox_fill_signup(driver,**valid_signup_data)

    # 필수(나이) 체크
    age_check = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[text()=\"I'm 14 years or older.\"]]")
        )
    )
    age_check.click()

    # 선택 약관 체크
    optional_check = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//label[.//span[text()='[Optional] Receive updates and promotional emails.']]")
        )
    )
    optional_check.click()

    create_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert not create_btn.is_enabled(), "❌ 필수 항목 미동의인데 버튼이 활성화됨" #create_btn이 활성화 되지 않으면 테스트 통과
    print("✔ Create account 버튼 비활성화 확인")
