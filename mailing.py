import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_daily_info():
    password = config.ya_password
    user = config.yandex
    recipients = config.google
    file = "daily_users_info.txt"

    msg = MIMEMultipart()
    msg["From"] = user
    msg["Subject"] = "daily users info"

    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(open(file, "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={file}')
    msg.attach(attachment)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(user, password)
    server.sendmail(user, recipients, msg.as_string())
    server.quit()


if __name__ == "__main__":
    send_daily_info()
