# Import smtplib for the actual sending function
import smtplib
from email.message import EmailMessage

MY_ADDRESS = "kapTest@web.de"
PASSWORD = 'kappasswort'
SMTP_SERVER = "smtp.web.de"

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


def sendReminderMail(recipient):
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

def sendOverdueMail(recipient):
    msg = EmailMessage()
    msg.set_content("Sie nehmen bei einer Studie an unserem Institut teil und sind für eine Untersuchung überfällig!")
    msg['Subject'] = "Termin überfällig"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
    s.quit()

def VIPreminder(vip,recipient):
    msg = EmailMessage()
    msg.set_content("Ein \"Very Important Patient\": " + vip.username +" hat sich für einen Termin angemeldet!")
    msg['Subject'] = "VIP Terminanmeldung"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient.email
    s = smtplib.SMTP(SMTP_SERVER)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
    s.quit()
