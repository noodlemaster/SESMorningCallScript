import urllib.request
import requests
from bs4 import BeautifulSoup


url = 'https://www.fifa.com/worldcup/matches/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
head = {'User- Agent': user_agent}
'''
response = requests.get(url, head)
tree = html.fromstring(response.content)
print(tree)
'''
response = urllib.request.urlopen(url, head)
html = response.read().decode('utf-8')
print(html)
#target = BeautifulSoup(html, 'lxml')
#arget = target.find(class_ = 'fi-mu-list today')
#target = target.find_all('a')
#print(target)