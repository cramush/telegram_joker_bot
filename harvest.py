import pymongo
import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

client = pymongo.MongoClient(f"mongodb://{config.login}:{config.password}@{config.host}/{config.db_name}")
db = client["users_info_db"]
info_collection = db["info"]

# import schedule
# schedule.every().day.at("10:00").do(harvest)
# add cron


def harvest_info():
    box = info_collection.find().sort([("date", pymongo.ASCENDING)])
    box = [str(el["date"]) + " {info: " +
           str(el["first_name"]) + ", " +
           str(el["username"]) + ", " +
           str(el["user_id"]) + "} content: " +
           str(el["content"]) for el in box]

    with open("daily_users_info.txt", "w") as f:
        for element in box:
            f.write(element + "\n")

    send_daily_info()
    info_collection.drop()


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
    harvest_info()
