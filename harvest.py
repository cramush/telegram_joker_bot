# add cron
import pymongo
from config import login, password, host, db_name
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from config import ya_password, yandex, google
from datetime import date, timedelta

client = pymongo.MongoClient(f"mongodb://{login}:{password}@{host}/{db_name}?authSource=admin")
db = client["my_mongo"]
info_collection = db["info"]


def harvest_info():
    box = info_collection.find().sort([("date", pymongo.ASCENDING)])
    box = [str(el["content"]) + ": {" +
           str(el["first_name"]) + ", " +
           str(el["username"]) + ", " +
           str(el["user_id"]) + ", " +
           str(el["time"]) + "}" for el in box]

    with open("daily_users_info.txt", "w") as f:
        for element in box:
            f.write(element + "\n")

    send_daily_info()
    info_collection.drop()


def send_daily_info():
    pwd = ya_password
    user = yandex
    recipients = google
    file = "daily_users_info.txt"
    yesterday = date.today() - timedelta(days=1)
    text = f"отчет за {yesterday}"

    msg = MIMEMultipart()
    msg["From"] = user
    msg["Subject"] = "daily users info"

    text = MIMEText(text, "plain")
    msg.attach(text)

    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(open(file, "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={file}')
    msg.attach(attachment)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(user, pwd)
    server.sendmail(user, recipients, msg.as_string())
    server.quit()


if __name__ == "__main__":
    harvest_info()
