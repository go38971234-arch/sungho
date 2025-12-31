import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException





# 기본 설정
BASE_LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
BASE_SIGNUP_URL ="https://accounts.elice.io/accounts/signup/method?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%3FisFirstLogin%3Dtrue&lang=en-US&org=qaproject"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
# -----------------------------
# 드라이버 생성
# -----------------------------

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


#스크린샷 설정
def save_screenshot(driver, test_type: str, name: str):
    """
    test_type: signup_email / signup_pw / signup_name
    name: TC명
    """

    test_dir = os.path.join(SCREENSHOT_DIR, test_type)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(test_dir, filename)

    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {filepath}")

    return filepath



# -----------------------------
# 로그인 페이지 이동
# -----------------------------
def navigate_to_login(driver):
    driver.get(BASE_LOGIN_URL)
    time.sleep(2)
# 회원가입 창 이동    
def navigate_to_signup(driver):
    driver.get(BASE_SIGNUP_URL)
    time.sleep(2)


# -----------------------------
# 요소 기다리기
# -----------------------------
def wait_for_element(driver, selector,by=By.CSS_SELECTOR,timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, f"[placeholder='{selector}']"))
        )

def wait_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by,selector))
    )
#클릭할 수 있는 요소를 찾고 찾으면 자동으로 클릭해주는 함수
def click_element(driver, selector: str):
    """Click element with data-testid."""
    element = wait_clickable(driver, selector)
    element.click()
    return element

#입력필드를 찾고 자동으로 타이핑 해주는 함수
def type_text(driver, selector: str, text: str):
    """Type text into element with data-testid."""
    element = wait_for_element(driver, selector)
    element.clear()
    element.send_keys(text)
    return element

#임의의 회원가입 테스트 이메일 생성
def generate_unique_username():
    num = random.randint(10000, 99999)
    return f"testuser{num:05d}"

# 공통 로그인 함수
# -----------------------------
def login(driver, email, password):
    navigate_to_login(driver)
    type_text(driver, "Email", email)
    type_text(driver, "Password", password)
    click_element(driver, "[type='submit']")


# -----------------------------
# 로그아웃 기능
# -----------------------------
def logout(driver):
    print("\n▶ 로그아웃 진행 중...")

    wait_clickable(driver, '[data-testid="PersonIcon"]').click()
    time.sleep(1)
    wait_clickable(driver, "//p[contains(text(), '로그아웃')]", by=By.XPATH).click()
    welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
    assert welcome_text.is_displayed()
    
#회원가입 기능 
def open_signup_page(driver):
    navigate_to_signup(driver)
    click_element(driver, "[type='button']")

#회원가입 입력필드에 입력해주고 agree all 체크박스 눌러주는 기능
def fill_signup_form(driver, email=None, password=None, name=None):
    if email is not None:
        type_text(driver, "Email", email)
    if password is not None:
        type_text(driver, "Password", password)
    if name is not None:
        type_text(driver, "Name", name)

    driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()

#회원가입 create acoount 버튼 눌러주는 기능
def submit_signup(driver):
    click_element(driver, "button[type='submit']")

#위의 것들을 합쳐 회원가입이 한번에 되는 회원가입 브라우저 생성->함수 입력필드에 타이핑 후 agree all체크->create account눌러주는 함수 
def signup(driver, email, password, name):
    open_signup_page(driver)
    fill_signup_form(driver, email, password, name)
    submit_signup(driver)
    






    

