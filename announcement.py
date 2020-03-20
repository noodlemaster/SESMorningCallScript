import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


text = 'Dear users,'+'\n'+''+'\n'+"As you may have noticed, the emails haven't benn sent in past two days. This is because of some technical issues with the sending email which have now been fixed."+'\n'+''+'\n'+'Apologize for the inconvenience.'+'\n'+'Gandy'


conn = sqlite3.connect('/home/ubuntu/django/SESMorningCallServer/db.sqlite3')
c = conn.cursor()
for row in c.execute('SELECT firstname,lastname,guid,email,mailing FROM userdata_user'):
    user_firstname = row[0].capitalize()
    user_lastname = row[1].capitalize()
    user_name = user_firstname + ' ' + user_lastname
    user_email = row[3]



    my_sender = 'sesmorningcall@outlook.com'
    my_pass = 'Worldtradekoji!'

    my_user = user_email


    def mail():
        ret = True
        try:
            msg = MIMEText(text, 'plain')
            msg['From'] = formataddr(['SES-Morning Call', my_sender])
            msg['To'] = formataddr([user_name, my_user])
            msg['Subject'] = 'IMPORTANT ANNOUNCEMENT'

            server = smtplib.SMTP('smtp.office365.com', 587)
            server.ehlo()
            server.starttls()
            server.login(my_sender, my_pass)
            server.sendmail(my_sender, my_user, msg.as_string())
            server.quit()
        except Exception:
            ret = False
        return ret


    ret = mail()
    if ret:
        print('Successfully sent')
    else:
        print('Error')
