# Import smtplib for the actual sending function
import smtplib
from email.message import EmailMessage

def sendTestMail(recipient):
    msg = EmailMessage()
    msg.set_content("TestBody")
    msg['Subject'] = "TestSubject"
    msg['From'] = "kapTest@web.de"
    msg['To'] = recipient
    # Send the message via our own SMTP server.
    username = "kapTest@web.de"
    passwort = "kappasswort"
    s = smtplib.SMTP('smtp.web.de')
    s.starttls()
    s.login(username, passwort)
    s.send_message(msg)
    s.quit()