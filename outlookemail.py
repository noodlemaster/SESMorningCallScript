<<<<<<< HEAD
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

# try:
msg=MIMEText("Hello World!",'plain')
msg['From']=formataddr(['SES-Morning Call', 'sesmorningcall@outlook.com'])
msg['To']=formataddr(['noodles', 'shukawak@stedwarsoxford.org'])
msg['Subject']='Good morning'

server = smtplib.SMTP('smtp.office365.com', 587)
server.ehlo()
server.starttls()
server.login('sesmorningcall@outlook.com', 'Worldtradekoji!')
print(msg.as_string())
server.sendmail('sesmorningcall@outlook.com','shukawak@stedwarsoxford.org',msg.as_string())
server.quit()
# except Exception:
# 	ret=False
# print(ret)
=======
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

# try:
msg=MIMEText("Hello World!",'plain')
msg['From']=formataddr(['SES-Morning Call', 'sesmorningcall@outlook.com'])
msg['To']=formataddr(['noodles', 'shukawak@stedwarsoxford.org'])
msg['Subject']='Good morning'

server = smtplib.SMTP('smtp.office365.com', 587)
server.ehlo()
server.starttls()
server.login('sesmorningcall@outlook.com', 'WorldtradeGandy!')
print(msg.as_string())
server.sendmail('sesmorningcall@outlook.com','shukawak@stedwarsoxford.org',msg.as_string())
server.quit()
# except Exception:
# 	ret=False
# print(ret)
>>>>>>> d44e66a559022b47b901bb97ec39aa6a2741919d
