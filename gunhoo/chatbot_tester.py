import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

class ChatBotTester:
    """
    챗봇 테스트를 위해 공통으로 사용하는 동작 모음 클래스.
    메시지 전송, 답변 대기, 새 대화 버튼 클릭 등을 담당한다.
    """

    def __init__(self, browser):
        self.browser = browser

    # ------------------------------------------------
    # 1. 메시지 전송
    # ------------------------------------------------
    def send_message(self, message):

        ignored_exceptions = (StaleElementReferenceException,)

        lines = message.split("\n")

        for idx, line in enumerate(lines): # 텍스트 입력 전, 입력 가능한 상태인지 확인하고 요소 찾기
        
            textarea = WebDriverWait(self.browser, 10, ignored_exceptions=ignored_exceptions).until(      # 조건 참이 될 때까지 반복 확인, 에러가 발생해도 즉시 실패하지 않고 재시도하도록 설정
                EC.element_to_be_clickable(                                                               # 클릭 가능한 상태인지 확인
                    (By.CSS_SELECTOR, "textarea[name='input']")
                )
            )
            textarea.send_keys(line)

            # 마지막 줄이 아니면 줄바꿈만
            if idx < len(lines) - 1:                                # 현재 처리 중인 줄의 번호가 마지막 번호보다 작다면
                # 줄바꿈 키를 보내기 전에도 반드시 요소를 다시 찾음
                textarea = WebDriverWait(self.browser, 10, ignored_exceptions=ignored_exceptions).until(   # textarea 똑같이 값을 넣어 할당해 최신 주소로 갱신, 요소 참조 오류 방어
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "textarea[name='input']")
                    )
                )
                textarea.send_keys(Keys.SHIFT, Keys.ENTER)

        # 마지막 전송(Enter) 전에도 요소를 다시 찾음
        textarea = WebDriverWait(self.browser, 10, ignored_exceptions=ignored_exceptions).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "textarea[name='input']")
            )
        )
        textarea.send_keys(Keys.ENTER)

    # ------------------------------------------------
    # 2. 모든 답변 요소 가져오기
    # ------------------------------------------------
    def get_all_answers(self):
        return self.browser.find_elements(
            By.CSS_SELECTOR, ".elice-aichat__markdown"
        )

    # ------------------------------------------------
    # 3. 답변 대기 (멈춤 방지 핵심 로직)
    # ------------------------------------------------
    def wait_for_answer(
        self,
        prev_answer_count,
        spinner_selector="svg.MuiCircularProgress-svg",
        answer_selector=".elice-aichat__markdown",
        min_wait_time=5.0,
        stable_duration=1.0,
        max_total_wait=60.0,
    ):

        
        # 스피너가 뜨거나 OR 답변 개수가 늘어날 때까지 기다림 (최대 min_wait_time 만큼)
        try:
            WebDriverWait(self.browser, min_wait_time).until(
                lambda driver: (
                    # 조건 A: 로딩 스피너가 화면에 나타남
                    len(driver.find_elements(By.CSS_SELECTOR, spinner_selector)) > 0
                ) or (
                    # 조건 B: 답변 요소의 개수가 이전보다 많아짐
                    len(driver.find_elements(By.CSS_SELECTOR, answer_selector)) > prev_answer_count
                )
            )
            print("⏳ 챗봇 반응 감지됨 (스피너 또는 새 답변)")
        except Exception:
            print("ℹ️ 반응 감지 시간 초과 (이미 답변이 완료되었거나 반응이 없음)")

        # 2️⃣ 스피너가 있다면 사라질 때까지 (있을 때만)
        try:
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            WebDriverWait(self.browser, 30).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            print("⏳ 스피너 종료 감지")
        except Exception:
            print("ℹ️ 스피너 미감지 (즉시 답변)")

        # 3️⃣ 새 답변 DOM 증가 감지 (실패 허용)
        try:
            WebDriverWait(self.browser,5).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, answer_selector))    # d는 브라우저 객체, lambda 는 일회용 조건함수
                > prev_answer_count                                                 # 이전 답변보다 많으면 새 답변 DOM이 추가됨
            )
            print("⏳ 새 답변 DOM 감지")
        except Exception:
            print("⚠️ 답변 DOM 증가 감지 실패 → 기존 답변 사용")

        # 4️⃣ 마지막 답변 텍스트 안정화 (타임아웃 필수)
        answers = self.get_all_answers()

        if not answers:
            print("⚠️ 답변 요소 없음")
            return

        
        prev_text = ""                                      # 이전 확인 시점 텍스트 저장
        stable_start = None                                 # 텍스트 안 변하는 시점 시작 기록
        deadline = time.time() + max_total_wait             # 최대 대기 시간

        while time.time() < deadline:                       
            answers = self.get_all_answers()                # 루프에서 get_all_answers 를 호출, DOM 갱신 감지
            if not answers:                                 # 답변 없다면 대기 후 다시 확인
                time.sleep(0.3)
                continue

            last_answer = answers[-1]                       # 역순으로 넣어서 가장 최근 답변


            try:
                current_text = last_answer.text.strip()     # 텍스트 추출 후 앞뒤 공백 제거
            except (StaleElementReferenceException, WebDriverException):
                # 요소가 화면 갱신으로 사라졌거나(Stale), 텍스트 변환 중 오류(Deserialize) 발생 시
                # 당황하지 않고 잠시 대기 후 재시도 (continue)
                time.sleep(0.1)
                continue

            if current_text != prev_text:                   # 이전 확인 시점과 다르면
                prev_text = current_text                    # 현재 텍스트로 변경
                stable_start = time.time()                  # 안정화 시작 시간 기록
            else:                                                                   # 이전 텍스트와 같다면 (변동없다면) 
                if stable_start and time.time() - stable_start >= stable_duration:  # 이어서 상태가 stable_duration 이상이라면 답변 안정화 완료
                    print("✅ 답변 안정화 완료")                                     
                    return

            time.sleep(0.3)

        print("⚠️ 답변 안정화 타임아웃 → 강제 진행")

    # ------------------------------------------------
    # 4. 마지막 답변 가져오기
    # ------------------------------------------------
    def get_last_answer(self):
        answers = self.get_all_answers()
        return answers[-1].text if answers else ""          # 답변 없다면 빈 문자열 "" 을 반환, 테스트 코드가 지속되게 함

    # ------------------------------------------------
    # 5. 새 대화 시작 버튼 클릭
    # ------------------------------------------------
    def new_chat(self):
        try:
            ignored_exceptions = (StaleElementReferenceException,)
            btn = WebDriverWait(self.browser, 10, ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[.//span[contains(text(), '새 대화')]]")
                )
            )
            btn.click()

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea[name='input']")
                )
            )
            print("🆕 새 대화 시작")
        except Exception as e:
            print("❌ 새 대화 버튼 클릭 실패:", e)      # e 는 실제 발생한 에러 객체이며 안의 에러 로그를 보여줌



    