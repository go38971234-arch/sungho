import os
from dotenv import load_dotenv

# .env 파일의 내용을 환경 변수로 로드합니다.
load_dotenv()

# 환경 변수에서 값을 가져옵니다.
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")