import sqlite3
import urllib.parse
import pycurl

conn = sqlite3.connect('/home/ubuntu/django/SESMorningCallServer/db.sqlite3')
c = conn.cursor()
i = 0
for row in c.execute('SELECT email FROM userdata_user'):
	email_name = row[0]
	if email_name.endswith('@stedwardsoxford.org'):
		payload = {
			'Flag' : '3',
			'Login' : 'SpamDigest',
			#'Sdr' : 'info@sesmorningcallandeveningcall.co.uk',
			'Sdr' : 'sesmorningcaill@outlook.com',
			'Rcpt' : email_name,
			'Server' : 'g64.mailwallremote.com',
			'lst' : '0'
		}
		curl = pycurl.Curl()
		field_data = urllib.parse.urlencode(payload)	
		curl.setopt(pycurl.URL, 'https://myaccount.mailwallremote.com/mw08/BlockMail.asp?' + field_data)
		print(field_data)	
		curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
		curl.setopt(pycurl.POSTFIELDS, field_data)
		curl.setopt(pycurl.VERBOSE, True)
		curl.perform()
		i = i + 1
print(i)
