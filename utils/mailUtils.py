# Import smtplib for the actual sending function
import smtplib
from email.message import EmailMessage
from django.contrib.auth import get_user_model
import signal
from contextlib import contextmanager

@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


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
    with timeout(7):
        try:
            s = smtplib.SMTP(SMTP_SERVER)
            s.starttls()
            s.login(MY_ADDRESS,PASSWORD)
            s.send_message(msg)
            s.quit()
            return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1

def sendWeekReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    with timeout(7):
        try:
            s = smtplib.SMTP(SMTP_SERVER)
            s.starttls()
            s.login(MY_ADDRESS,PASSWORD)
            s.send_message(msg)
            s.quit()
            return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1


def sendDayReminderMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie haben demnächst einen Termin bei uns!")
    msg['Subject'] = "Termin Erinnerung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    with timeout(7):
        try:
            s = smtplib.SMTP(SMTP_SERVER)
            s.starttls()
            s.login(MY_ADDRESS,PASSWORD)
            s.send_message(msg)
            s.quit()
            return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1


def sendOverdueMail(recipient,checkupName):
    msg = EmailMessage()
    msg.set_content("Sie nehmen bei einer Studie an unserem Institut teil und sind für ihre Untersuchung \"" + str(checkupName) + "\" überfällig!")
    msg['Subject'] = "Termin überfällig"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    with timeout(7):
        try:
            s = smtplib.SMTP(SMTP_SERVER)
            s.starttls()
            s.login(MY_ADDRESS,PASSWORD)
            s.send_message(msg)
            s.quit()
            return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1

def deleteNotify(user):
    with timeout(7):
        try:
            s = smtplib.SMTP(SMTP_SERVER)
            s.starttls()
            s.login(MY_ADDRESS, PASSWORD)
            msg = EmailMessage()
            msg.set_content("Der Patient\": " + user.username + " hat einen Termin abgebrochen!")
            msg['Subject'] = "Patient hat Termin ABGEBROCHEN"
            msg['From'] = "kapTest@web.de"
            for doc in DOCTORS:
                msg['To'] = doc.email
                s.send_message(msg)
            msg['Subject'] = "Termin ABGEBROCHEN"
            msg.set_content("BENACHRICHTIGUNG: Ihr Termin bei uns wurde abgebrochen!")
            msg['To'] = user.email
            s.send_message(msg)
            s.quit()
            return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1


def VIPreminder(vip):
    with timeout(7):
        try:
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
                return 0
        except Exception as err:
            print("error sending email: {0}".format(err))
            return -1
    return -1