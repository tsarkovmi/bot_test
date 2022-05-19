import smtplib
import string
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup as bs


def send_mail(email, password, FROM, TO, msg):
    server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
    server.login(email, password)
    # server.starttls()
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()


# Процедура auth принимает на вход email получателя и код, который необходимо отправить.
# Результатом работы будет отправленное письмо с адреса deadlinebot@yandex.ru на email_to,
# содержимым которого будет полученный процедурой код
def auth(email_to, code):  # arguments format - string
    email = "deadlinebot@yandex.ru"
    password = "MEpy6DDSUD3HFDG"
    FROM = "deadlinebot@yandex.ru"
    TO = email_to
    subject = "Auth code"

    msg = MIMEMultipart("alternative")
    msg["From"] = FROM
    msg["To"] = TO
    msg["Subject"] = subject

    html = open("auth/mail.html").read()
    html = bs(html, "html.parser")
    html.strong.string.replace_with(code)
    html.prettify(formatter="html")
    text = ('Your code:\n{}'.format(code))

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")

    msg.attach(text_part)
    msg.attach(html_part)

    send_mail(email, password, FROM, TO, msg)
