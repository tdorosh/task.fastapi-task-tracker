import smtplib

from project.conf import settings
from project.logger import logger


def send_email(email_address: str, message: str):
    try:
        with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as server:
            server.login(settings.smtp_login, settings.smtp_password)
            server.sendmail(settings.smtp_sender, [email_address], message)

        logger.info(f"Notification email was sent successfully to {email_address}")
    except Exception as error:
        logger.error(f"Error during sending notification email: {error}")
