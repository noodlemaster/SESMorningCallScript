import re
import smtplib
import sqlite3
import sys
import time
import traceback
import urllib.parse
import urllib.request
import calendar
from email.mime.text import MIMEText
from email.utils import formataddr
from http import cookiejar
from bs4 import BeautifulSoup

#html_file = open('morningmail.html')
html_file = open('/home/ubuntu/SESMorningCallScript/morningmail.html')
email_html = html_file.read().split('{{}}')
html_file.close()

login_url = 'https://dashboard.stedwardsoxford.org/login/login.aspx?prelogin=https%3a%2f%2fdashboard.stedwardsoxford.org%2fpupil-dashboard&kr=ActiveDirectoryKeyRing'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
head = {'User-Agent': user_agent}
login_data = {}
login_data['username'] = '' #login details
login_data['password'] = ''
loginpostdata = urllib.parse.urlencode(login_data).encode('utf-8')
cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(cookie_support)
req_1 = urllib.request.Request(url=login_url, data=loginpostdata, headers=head)

data_url = 'https://dashboard.stedwardsoxford.org/pupil-dashboard'
req_2 = urllib.request.Request(url=data_url, headers=head)
response_1 = opener.open(req_1)
response_2 = opener.open(req_2)
html = response_1.read().decode('utf-8')

class_date = time.gmtime(time.time())
GMT_date = time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime(time.time())) + ' GMT'

log = open('morning.log', 'w')
#log = open('/home/ubuntu/SESMorningCallScript/morning.log', "w")

log.write(GMT_date + '\n')

#conn = sqlite3.connect('db.sqlite3')
#conn = sqlite3.connect('/home/ubuntu/django/SESMorningCallServer/db.sqlite3')

try:
    catering_url = 'https://dashboard.stedwardsoxford.org/catering'
    req_3 = urllib.request.Request(url=catering_url, headers=head)
    response_catering = opener.open(req_3)
    html_menu = response_catering.read().decode('utf-8')

    target_menu = BeautifulSoup(html_menu, 'lxml')
    judge_date = target_menu.find_all(class_='ff-navigationcomponent__label')

    for i in range(0, len(judge_date)):
        menu_url_date = str(judge_date[i])
        judge_date[i] = str(judge_date[i])
        judge_date[i] = judge_date[i].split('>')[1]

        list_date = []
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']
        lower_date = judge_date[i].split('-')[0]  # [0:2]
        lower_date = int(re.sub('\D', '', lower_date))
        upper_date = judge_date[i].split('-')[1]  # split('- ')[1][0:2]
        upper_date = int(re.sub('\D', '', upper_date))

        if upper_date > lower_date:
            for d in range(lower_date, upper_date + 1):
                list_date.append(d)
        else:
            lower_month = menu_url_date.split('>')[1].split(' ')[1]
            upper_month = menu_url_date.split('>')[1].split(' ')[4].split('<')[0]
            lower_month = re.sub('\W', '', lower_month)
            upper_month = re.sub('\W', '', upper_month)
            if lower_month in ['April','June','September','November','april','june','september','november']:
                for d in range(lower_date, 31):
                    list_date.append(d)
                for x in range(1, upper_date + 1):
                    list_date.append(x)
            elif lower_month in ['February', 'february']:
                if calendar.isleap(class_date.tm_year):
                    for d in range(lower_date, 30):
                        list_date.append(d)
                    for x in range(1, upper_date + 1):
                        list_date.append(x)
                else:
                    for d in range(lower_date, 29):
                        list_date.append(d)
                    for x in range(1, upper_date + 1):
                        list_date.append(x)
            else:
                for d in range(lower_date, 32):
                    list_date.append(d)
                for x in range(1, upper_date + 1):
                    list_date.append(x)
        #print(list_date)

        for e in list_date:
            if class_date.tm_mday != e:
                pass
            else:
                menu_url_date_final_month = menu_url_date
                menu_url_date = menu_url_date.split('>')[1].split(' ')
                for m in month:
                    if menu_url_date[1] == m:
                        menu_url_date_final_month = menu_url_date_final_month.split('>')[1].split(' ')[-1]
                        menu_url_date_final_month = re.split('\W', menu_url_date_final_month)[0]

                        menu_url = 'https://dashboard.stedwardsoxford.org/catering/' + menu_url_date[0] + '-' + \
                                   menu_url_date[1].lower() + '---' + menu_url_date[
                                       3] + '-' + menu_url_date_final_month
                        cooper_url = menu_url + 'coopers-cafe'

                        req_4 = urllib.request.Request(url=menu_url, headers=head)
                        response_menu = opener.open(req_4)
                        html_menu_today = response_menu.read().decode('utf-8')
                        # print(html_menu_today)

                        tables = []
                        rows = []
                        columns = []

                        while html_menu_today.find('<table') != -1:
                            table = html_menu_today[
                                    html_menu_today.find('<table'):html_menu_today.find('</table>') + 8]
                            html_menu_today = html_menu_today[html_menu_today.find('</table>') + 8:]
                            rows = []
                            while table.find('<tr>') != -1:
                                row = table[table.find('<tr>'):table.find('</tr>') + 5]
                                table = table[table.find('</tr>') + 5:]
                                columns = []
                                while row.find('<td') != -1:
                                    column = row[row.find('<td'):row.find('</td>') + 5]
                                    row = row[row.find('</td>') + 5:]

                                    column = column[:column.find('</')]
                                    column = column[column.rfind('>') + 1:]
                                    if column.strip():
                                        columns.append(column)
                                if columns:
                                    rows.append(columns)
                            tables.append(rows)
                        # class_date = time.gmtime(time.time())
                        index = class_date.tm_wday
                        #print(tables)
                        try:
                            lunch = tables[1][2][index + 1]
                        except IndexError:
                            lunch = 'null'
                        try:
                            lunch_2 = tables[1][4][index + 1]
                        except IndexError:
                            lunch_2 = 'null'
                        try:
                            supper = tables[2][0][index + 1]
                        except IndexError:
                            supper = 'null'
                        try:
                            supper_vegetarian = tables[2][1][index + 1]
                        except IndexError:
                            supper_vegetarian = 'null'

                        breakfast_l = ['Grilled back bacon, Fried Eggs, Potato Waffles, Grilled Tomatoes',
                                       'Butchers sausages, Baked beans, Scrambled egg, Saute Mushrooms',
                                       'Continental meats, Cheese, Rustic Wholemeal breads, Boiled egg, Danish pastries',
                                       'Grilled Back Bacon, Poached Egg, Black Pudding, Hash Browns',
                                       'Bacon rolls, sausages, fried eggs, hash browns',
                                       'Sausages, scrambled egg, plum tomatoes, fried bread, spaghetti hoops',
                                       'Brunch']
                        breakfast = tables[0][2][index]
                        #breakfast = breakfast_l[index]
                        lunch = lunch + ", " + lunch_2

                        req_5 = urllib.request.Request(url=cooper_url, headers=head)
                        response_menu = opener.open(req_4)
                        html_menu_cooper = response_menu.read().decode('utf-8')


                        menu = "Today's menu:" + '\n' + 'Breakfast: ' + breakfast + '\n' + 'Lunch: ' + lunch + '\n' + 'Hot Deli Bar: ' + lunch_2 + '\n' + 'Supper: ' + supper
                        print(menu)
                    else:
                        pass
except urllib.error.HTTPError:
    pass
log.write(breakfast + '' + '\n' + '' + lunch + '' + '\n' + '' + supper + '' + '\n')

c = conn.cursor()
for row in c.execute('SELECT name,guid,email,mailing FROM userdata_user'):
    try:
        mailing = row[3]
        if mailing == '1':
            user_name = row[0].capitalize()
            user_url = 'https://dashboard.stedwardsoxford.org/profile?guid=' + row[1]
            user_email = row[2]
            log.write(user_name + ',' + user_email + '\n')
            req = urllib.request.Request(url=user_url, headers=head)
            response = opener.open(req)
            html_1 = response.read()
            class_date = time.gmtime(time.time())
            if class_date.tm_wday != 6:
                target = BeautifulSoup(html_1, 'lxml')
                lesson_all = target.find(class_='ff-timetable-day ff-timetable-today')
                class_date = time.gmtime(time.time())
                lesson_list = []
                lesson_information = []
                lesson = lesson_all.find_all(class_='ff-timetable-lesson-subject')
                for i in range(0, len(lesson)):
                    lesson[i] = str(lesson[i])
                    lesson_list.append(lesson[i].split('>')[1].split('<')[0])

                l_time = []
                lesson_time = lesson_all.find_all(class_='ff-timetable-lesson-info')
                for i in range(0, len(lesson_time)):
                    lesson_time[i] = str(lesson_time[i]).split('"')[3].split(' in')[0]
                    l_time.append(lesson_time[i])

                for i in range(0, len(l_time) - 1):
                    if l_time[i] == l_time[i + 1]:
                        if lesson_list[i] == lesson_list[i + 1]:
                            lesson_list.pop(i + 1)
                        else:
                            lesson_list[i] = lesson_list[i] + ' / ' + lesson_list[i + 1]
                            lesson_list.pop(i + 1)

                lesson_teacher = lesson_all.find_all(class_='ff-timetavble-lesson-teacher')
                if len(lesson_teacher) >= len(lesson_list):
                    for i in range(0, len(lesson_list)):
                        match = lesson_teacher[0].previous_sibling.previous_sibling
                        match = str(match)
                        match = match.split('>')[1].split('<')[0]
                        name = lesson_teacher[0]
                        name = str(name).split('>')[1].split('<')[0]
                        if lesson_list[i] == 'IB meeting':
                            lesson_info = 'IB Meeting'
                            lesson_information.append(lesson_info)
                            lesson_teacher.remove(lesson_teacher[0])
                            lesson_teacher.remove(lesson_teacher[0])
                        else:
                            if lesson_list[i] == match:
                                lesson_info = lesson_list[i] + ',' + name
                                lesson_information.append(lesson_info)
                                lesson_teacher.remove(lesson_teacher[0])
                            else:
                                lesson_info = lesson_list[i]
                                lesson_information.append(lesson_info)

                elif len(lesson_teacher) == 0:  # For teachers
                    lesson_teacher = lesson_all.find_all('strong')
                    for i in range(0, len(lesson_list)):
                        match = lesson_teacher[0].next_sibling.next_sibling
                        match = str(match)
                        match = match.split('>')[1].split('<')[0]
                        name = lesson_teacher[0]
                        name = str(name).split('>')[1].split('<')[0]
                        if lesson_list[i] == match:
                            lesson_info = lesson_list[i] + ',' + name
                            lesson_information.append(lesson_info)
                            lesson_teacher.remove(lesson_teacher[0])
                        else:
                            lesson_info = lesson_list[i]
                            lesson_information.append(lesson_info)

                else:
                    lesson_teacher.insert(len(lesson_teacher), 'a><')
                    for i in range(0, len(lesson_list)):
                        try:
                            match = lesson_teacher[0].previous_sibling.previous_sibling
                            match = str(match)
                            match = match.split('>')[1].split('<')[0]
                        except AttributeError:
                            match = ''
                        name = lesson_teacher[0]
                        name = str(name).split('>')[1].split('<')[0]
                        if lesson_list[i] == 'IB meeting':
                            lesson_info = 'IB Meeting'
                            lesson_information.append(lesson_info)
                            lesson_teacher.remove(lesson_teacher[0])
                            lesson_teacher.remove(lesson_teacher[0])
                        else:
                            if lesson_list[i] == match:
                                lesson_info = lesson_list[i] + ',' + name
                                lesson_information.append(lesson_info)
                                lesson_teacher.remove(lesson_teacher[0])
                            else:
                                lesson_info = lesson_list[i]
                                lesson_information.append(lesson_info)

                free = []
                l_time = set(l_time)
                if (class_date.tm_wday + 1) % 2 == 0:
                    time_l = ['08:30 - 09:25', '09:30 - 10:25', '11:00 - 11:55', '12:00 - 12:55']
                    if len(time_l) == len(l_time):
                        pass
                    else:
                        for t in range(0, len(time_l)):
                            if time_l[t] not in l_time:
                                lesson_information.insert(t, 'STUDY PERIOD!!!!!')

                else:
                    time_l = ['08:30 - 09:25', '09:30 - 10:25', '11:00 - 11:55', '12:00 - 12:55', '14:30 - 15:25',
                              '15:30 - 16:25']
                    if len(time_l) == len(l_time):
                        pass
                    else:
                        for t in range(0, len(time_l)):
                            if time_l[t] not in l_time:
                                lesson_information.insert(t, 'STUDY PERIOD!!!!!')

                lesson_text = ''
                for x in lesson_information:
                    if len(x.split(',')) == 2:
                        lesson_text = lesson_text + '<tr id="footballinfo"><td>' + x.split(',')[0] + '</td><td id="footballinfo">' + x.split(',')[
                            1] + '</td></tr>'
                    else:
                        lesson_text = lesson_text + '<tr><td id="footballinfo">' + x + '</td></tr>'

            else:
                lesson_text = '<tr><td id="footballinfo">No lessons today</td></td>'

            url = 'https://www.bbc.com/weather/0/2640729'
            response = urllib.request.urlopen(url)
            html = response.read().decode('utf-8')
            target = BeautifulSoup(html, 'lxml')
            tem = str(target.find_all(class_='wr-value--temperature--c'))
            tem_high = tem.split('>')[1].split('<')[0]
            tem_low = tem.split('>')[3].split('<')[0]
            tem_final = tem_low + ' -- ' + tem_high
            tem_description = str(target.find(
            class_='wr-day__weather-type-description wr-js-day-content-weather-type-description wr-day__content__weather-type-description--opaque'))
            tem_description = tem_description.split('>')[1].split('<')[0]


            # weather_oxford = "Today's Oxford weather:" + '\n' + tem_high + '- ' + tem_low + '\n' + tem_description
            # weather_source = '(from BBC Weather)'

            # GMT_date = time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime(time.time())) + ' GMT'

            try:
                # text = GMT_date + '\n' + '' + '\n' + weather_oxford + '\n' + weather_source + '\n' + '' + '\n' + "Today's lessons: " + '\n' + lesson_text + '\n' + '' + '\n' + menu + '\n' + '' + '\n' + '' + '\n' + 'Click the link below to unsubscribe or resubscribe' + '\n' + 'http://sesmorningcall.co.uk/subscription/?email=' + user_email + '&guid=' + \
                #        row[1] + '&type=1' + '\n' + 'Made by Gandy'
                text = email_html[0] + tem_final + email_html[1] + tem_description + email_html[2] + lesson_text + email_html[3] + breakfast + email_html[4] + lunch + email_html[5] + supper + email_html[6] + 'http://sesmorningcall.co.uk/subscription/?email=' + user_email + '&guid=' + \
                       row[1] + '&type=1' + email_html[7]
            except NameError:
                # text = GMT_date + '\n' + '' + '\n' + weather_oxford + '\n' + weather_source + '\n' + '' + '\n' + 'Invalid username/password for Dashbaord.'
                text = email_html[0] + tem_final + email_html[1] + tem_description + email_html[2] + "Error with the dashboard" + email_html[3] + breakfast + email_html[4] + lunch + email_html[5] + supper + email_html[6] + 'http://sesmorningcall.co.uk/subscription/?email=' + user_email + '&guid=' + \
                       row[1] + '&type=1' + email_html[7]

            log.write(text + '\n')

            my_sender = 'sesmorningcall@outlook.com'
            my_pass = 'WorldtradeGandy!'

            my_user = user_email

            def mail():
                ret = True
                try:
                    msg = MIMEText(text, 'html')
                    msg['From'] = formataddr(['SES-Morning Call', my_sender])
                    msg['To'] = formataddr([user_name, my_user])
                    msg['Subject'] = 'Good morning, ' + user_name

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
            # ret = False
            if ret:
                log.write('Successfully sent' + '\n' + '')
                time.sleep(40)
                print('s')
            else:
                log.write('Error' + '\n' + '')
                print('x')
        else:
            pass
    except:
        my_sender = 'sesmorningcall@outlook.com'
        my_pass = '' #password for this email
        info = sys.exc_info()
        tbinfo = traceback.format_tb(info[2])
        message = ''
        for tbi in tbinfo:
            message = message + '\n' + str(tbi)
        text = "Error " + user_name + "\n" + message + "\n" + str(info[1])
        log.write(text + '\n' + '')

        def mail():
            ret = True
            try:
                msg = MIMEText(text, 'plain')
                msg['From'] = formataddr(['SES-Evening Call', my_sender])
                msg['To'] = formataddr([user_name, my_sender])
                msg['Subject'] = 'Error, ' + user_name

                server = smtplib.SMTP('smtp.office365.com', 587)
                server.ehlo()
                server.starttls()
                server.login(my_sender, my_pass)
                server.sendmail(my_sender, my_sender, msg.as_string())
                server.quit()
            except Exception:
                ret = False
            return ret
        ret = mail()
        if ret:
            log.write('Sent Error mail' + '\n' + '')
            print('xs')
        else:
            log.write('Error sending error mail' + '\n' + '')
            print('xx')

log.write('Completed' + '\n' + '')
log.close()
