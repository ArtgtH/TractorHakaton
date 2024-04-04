import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_USER = "peterburgskiytraktorniyzavod@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PASSWORD = "pbvwcxtvpdhzasay"
SMTP_PORT = 587


def send_email(receiver: str, result, topic):

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()

    try:
        server.login(SMTP_USER, SMTP_PASSWORD)
        message = MIMEMultipart()
        message['From'] = SMTP_USER
        message['To'] = receiver

        message['Subject'] = topic

        body = f"""
        {result}
        """

        message.attach(MIMEText(body, 'plain'))

        server.sendmail(SMTP_USER, receiver, message.as_string())
    except Exception as exc:
        return exc
    finally:
        server.quit()


if __name__ == '__main__':
    send_email('vsevolod.bogodist@gmail.com', 1, '1111')
