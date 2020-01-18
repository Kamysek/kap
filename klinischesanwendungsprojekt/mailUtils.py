# Import smtplib for the actual sending function
import smtplib
from email.message import EmailMessage
from django.contrib.auth import get_user_model

User = get_user_model()

MY_ADDRESS = "kapTest@web.de"
PASSWORD = 'kappasswort'
SMTP_SERVER = "smtp.web.de"
DOCTORS = User.objects.filter(groups__name="Doctor")


def sendTestMail(recipient):
    msg = EmailMessage()
    msg.set_content("TestBody")
    msg['Subject'] = "TestSubject"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS,PASSWORD)
    s.send_message(msg)
    s.quit()


def sendWeekReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
    s.quit()

def sendDayReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
    s.quit()

def sendOverdueMail(recipient,checkupName):
    msg = EmailMessage()
    msg.set_content("Sie nehmen bei einer Studie an unserem Institut teil und sind für ihre Untersuchung \"" + str(checkupName) + "\" überfällig!")
    msg['Subject'] = "Termin überfällig"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
    s.quit()

def VIPreminder(vip):
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    for doc in DOCTORS:
        msg = EmailMessage()
        msg.set_content("Ein \"Very Important Patient\": " + vip.username +" hat sich für einen Termin angemeldet!")
        msg['Subject'] = "VIP Terminanmeldung"
        msg['From'] = "kapTest@web.de"
        msg['To'] = doc.email
        s.send_message(msg)
    s.quit()

def VIPcancel(vip):
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    for doc in DOCTORS:
        msg = EmailMessage()
        msg.set_content("Ein \"Very Important Patient\": " + vip.username +" hat einen Termin abgebrochen!")
        msg['Subject'] = "VIP Termin ABGEBROCHEN"
        msg['From'] = "kapTest@web.de"
        msg['To'] = doc.email
        s.send_message(msg)
    s.quit()
