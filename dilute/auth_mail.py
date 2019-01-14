# def send_email(user, pwd, recipient, subject, body):
#     import smtplib

#     gmail_user = user
#     gmail_pwd = pwd
#     FROM = user
#     TO = recipient if type(recipient) is list else [recipient]
#     SUBJECT = subject
#     TEXT = body

#     # Prepare actual message
#     message = """From: %s\nTo: %s\nSubject: %s\n\n%s
#     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(gmail_user, gmail_pwd)
#         server.sendmail(FROM, TO, message)
#         server.close()
#         return 'successfully sent the mail'
#     except Exception:
#         return "failed to send mail"

# def verification_mail(recipient, subject, body):
#     return send_email('donotreplyfairshare@gmail.com', 'holed.com', recipient, subject, body )        
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys, traceback
def send_email(user, pwd, recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = recipient
        msg['Subject'] = subject
        message = body
        msg.attach(MIMEText(message))
        
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(user, pwd)
        
        mailserver.sendmail(user,recipient,msg.as_string())
        
        mailserver.quit()
    except Exception:
        print(traceback.format_exc())
def verification_mail(recipient, subject, body):
   return send_email('donotreplydilute@gmail.com', '', recipient, subject, body ) 
