# Import smtplib for the actual sending function
import smtplib
from email.message import EmailMessage
from django.contrib.auth import get_user_model

User = get_user_model()

MY_ADDRESS = "kapTest@web.de"
PASSWORD = 'kappasswort'
SMTP_SERVER = "smtp.web.de"
TIMEOUT = 7


def sendTestMail(recipient):
    msg = EmailMessage()
    msg.set_content("TestBody")
    msg['Subject'] = "TestSubject"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    try:
        s = smtplib.SMTP(SMTP_SERVER,timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS,PASSWORD)
        s.send_message(msg)
        s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1

def sendWeekReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    try:
        s = smtplib.SMTP(SMTP_SERVER,timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS,PASSWORD)
        s.send_message(msg)
        s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1


def sendDayReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    try:
        s = smtplib.SMTP(SMTP_SERVER,timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS,PASSWORD)
        s.send_message(msg)
        s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1


def sendOverdueMail(recipient,checkupName):
    msg = EmailMessage()
    msg.set_content("Sie nehmen bei einer Studie an unserem Institut teil und sind für ihre Untersuchung \"" + str(checkupName) + "\" überfällig!")
    msg['Subject'] = "Termin überfällig"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    try:
        s = smtplib.SMTP(SMTP_SERVER,timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS,PASSWORD)
        s.send_message(msg)
        s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1

def deleteNotify(user):
    try:
        s = smtplib.SMTP(SMTP_SERVER,timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)
        for doc in User.objects.filter(groups__name="Doctor"):
            msg = EmailMessage()
            msg.set_content("Der Patient\": " + user.username + " hat einen Termin abgebrochen!")
            msg['Subject'] = "Patient hat Termin ABGEBROCHEN"
            msg['From'] = "kapTest@web.de"
            msg['To'] = doc.email
            s.send_message(msg)
        msg = EmailMessage()
        msg['From'] = "kapTest@web.de"
        msg['Subject'] = "Termin ABGEBROCHEN"
        msg.set_content("BENACHRICHTIGUNG: Ihr Termin bei uns wurde abgebrochen!")
        msg['To'] = user.email
        s.send_message(msg)
        s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1


def VIPreminder(vip):
    print("AAAAAAAAAAAAAH")
    try:
        s = smtplib.SMTP(SMTP_SERVER, timeout=TIMEOUT)
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)
        for doc in User.objects.filter(groups__name="Doctor"):
            msg = EmailMessage()
            msg.set_content("Ein \"Very Important Patient\": " + vip.username +" hat sich für einen Termin angemeldet!")
            msg['Subject'] = "VIP Terminanmeldung"
            msg['From'] = "kapTest@web.de"
            msg['To'] = doc.email
            s.send_message(msg)
            s.quit()
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1