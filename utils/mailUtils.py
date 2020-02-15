# Import smtplib for the actual sending function
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
"""
These functions are all wrapped in a try catch so that they won't interrupt any api calls.
Emails are sent using django Backend (see docs)
"""

User = get_user_model()

EMAIL_FROM = "kapTest@web.de"

def sendTestMail(recipient):
    try:
        msg = EmailMessage()
        msg.body = "TestBody"
        msg.subject = "TestSubject"
        msg.from_email = EMAIL_FROM
        msg.to = [recipient.email]
        msg.send(fail_silently=False)
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1

def sendWeekReminderMail(recipient):
    try:
        msg = EmailMessage()
        msg.body = "Sie haben demnächst einen Termin bei uns!"
        msg.subject = "Termin Erinnerung"
        msg.from_email = EMAIL_FROM
        msg.to = [recipient.email]
        msg.send(fail_silently=False)
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1


def sendDayReminderMail(recipient):
    try:
        msg = EmailMessage()
        msg.body = "Sie haben demnächst einen Termin bei uns!"
        msg.subject = "Termin Erinnerung"
        msg.from_email = EMAIL_FROM
        msg.to = [recipient.email]
        msg.send(fail_silently=False)
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1


def sendOverdueMail(recipient,checkupName):
    try:
        msg = EmailMessage()
        msg.body = "Sie nehmen bei einer Studie an unserem Institut teil und sind für ihre Untersuchung \"" + str(checkupName) + "\" überfällig!"
        msg.subject = "Termin überfällig"
        msg.from_email = EMAIL_FROM
        msg.to = [recipient.email]
        msg.send(fail_silently=False)
        return 0
    except Exception as err:
        print("error sending email: {0}".format(err))
        return -1

def deleteNotify(user):
    try:
        msg = EmailMessage()
        msg.body = "Der Patient\": " + user.username + " hat einen Termin abgebrochen!"
        msg.subject = "Patient hat Termin ABGEBROCHEN"
        msg.from_email = EMAIL_FROM
        msg.to = []
        for doc in User.objects.all().filter(groups__name="Doctor"):
            msg.to.append(doc.email)
        msg2 = EmailMessage()
        msg2.from_email = EMAIL_FROM
        msg2.subject = "Termin ABGEBROCHEN"
        msg2.body = "BENACHRICHTIGUNG: Ihr Termin bei uns wurde abgebrochen!"
        msg2.to = [user.email]
        msg.send(fail_silently=False)
    except Exception as err:
        print("error sending email: {0}".format(err))
    try:
        msg2.send(fail_silently=False)
    except Exception as err:
        print("error sending email: {0}".format(err))#


def VIPreminder(vip):
    try:
        msg = EmailMessage()
        msg.body = "Ein \"Very Important Patient\": " + vip.username + " hat sich für einen Termin angemeldet!"
        msg.subject = "VIP Terminanmeldung"
        msg.from_email = EMAIL_FROM
        msg.to = []
        for doc in User.objects.all().filter(groups__name="Doctor"):
            msg.to.append(doc.email)
        msg.send(fail_silently=False)
    except Exception as err:
        print("error sending email: {0}".format(err))
