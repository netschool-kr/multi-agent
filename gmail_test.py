import os
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from dotenv import load_dotenv

# 환경변수 로드 (.env 파일에서 Gmail SMTP 계정 정보 읽기)
load_dotenv()  # .env 파일의 내용이 환경변수로 설정됨

# Gmail SMTP 계정 및 수신자 설정 (환경변수에서 가져옴)
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
GMAIL_RECEIVER = os.getenv('GMAIL_RECEIVER')

# 로깅 설정: INFO 레벨 이상의 메시지를 출력하도록 설정
logging.basicConfig(level=logging.INFO)

def send_alert_node(subject: str, message: str):
    """외환 트레이딩 에이전트의 알림을 이메일로 전송하는 함수."""
    try:
        # 이메일 MIME 메시지 구성
        mime_msg = MIMEText(message)
        mime_msg['Subject'] = subject
        mime_msg['From'] = GMAIL_USER
        mime_msg['To'] = GMAIL_RECEIVER

        # Gmail SMTP 서버에 SSL로 연결 (smtp.gmail.com:465)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465  # SSL 포트 (TLS 사용시 587 + starttls)
        context = ssl.create_default_context()  # 기본 SSL 컨텍스트 생성

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)             # Gmail SMTP 로그인
            server.send_message(mime_msg)                        # 이메일 전송
            # 서버 연결 종료는 with 블록 종료 시 자동 수행 (QUIT)
        logging.info("✅ 알림 이메일을 성공적으로 발송하였습니다.")
    except Exception as e:
        # 전송 중 예외 발생 시 로그 기록
        logging.error(f"❌ 알림 이메일 발송 실패: {e}")
        # 필요에 따라 예외를 다시 발생시켜 상위 로직에서 처리할 수도 있음
        # raise

# --- 예제 실행 (직접 실행 시 테스트용) ---
if __name__ == "__main__":
    test_subject = "테스트 알림: 이동평균 교차 발생"
    test_body = "외환 트레이딩 에이전트에서 이동평균 교차 신호가 발생했습니다. (테스트 메시지)"
    send_alert_node(test_subject, test_body)
