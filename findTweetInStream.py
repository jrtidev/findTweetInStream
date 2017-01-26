from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

at = '157335588-G8zEwfkKJat0QzPuV77iww1PVU5BtXBlbGITIeZP'
ats = 'V5bVrrGqgmdZ3xFsKFig9VWKU9Lvfepm0Ii9JTKfzG3DG'
ckey = 'R74IN04Adp1NKtTA1Cc6J4NeJ'
cs = 'u6qk0emnADqY9c3Yzr7Z5GCqnUpfpTxhX5IIEp3EjdhtRUGKGu'

twitter_stream = TwitterStream(auth=OAuth(at, ats, ckey, cs), domain='stream.twitter.com')
iterator = twitter_stream.statuses.sample()
count = 0
curr_count=0

print('NEW')
word = raw_input('Input word you need to find: ')
word = word.decode('utf-8')
print(word)

def send_message(count):
    recipient = 'jrtidev@gmail.com'
    sender_lgn = 'jrtidev@gmail.com'
    sender_pwd = 'Goo979198033'
    subj = 'Tweet count update'
    email_body = 'Hello, Artem!\nThis crazy world made another 100,000 tweets since '+str(localtime)+'! \n'+ str(count)+ ' in total!'  

    msg = MIMEMultipart('alternative')
    smtpsrvr = smtplib.SMTP('smtp.gmail.com', 587)
    smtpsrvr.ehlo()
    smtpsrvr.starttls()
    smtpsrvr.ehlo()
    smtpsrvr.login(sender_lgn, sender_pwd)

    msg['Subject'] = subj
    msg['From'] = sender_lgn
    body = email_body

    content = MIMEText(body, 'plain')
    msg.attach(content)
    smtpsrvr.sendmail(sender_lgn, recipient, msg.as_string())
    smtpsrvr.close()

#save tweet into file
def store_tweet(word, entity):
	with open(word+'.txt', 'a') as tw_str:
		try:
			tw_str.write(entity+'\n')
		except UnicodeEncodeError:
			tw_str.write('Encoding Error \n')

for i in iterator:
	try:
		text = i['text']
		print(text)
	except KeyError:
		# print('there is no such data')
		text = 'None'
	try:
		user_id = i['user']['id']
	except KeyError:
		# print('there is no such data')
		user_id = 'None'
	try:	
		name = i['user']['screen_name']
	except KeyError:
		# print('there is no such data')
		name = 'None'
	try:	
		location = i['user']['location']
	except KeyError:
		# print('there is no such data')
		location = 'None'
	try:	
		followers = i['user']['followers_count']
	except KeyError:
		# print('there is no such data')
		followers = 'None'
	#find word in twitter stream
	# curr_count = count
	if word in text:
		entity = 'Usrer ID: %s, \n User Name: %s, \n Location: %s, \n Followers: %s, \n Message: %s, \n' % (user_id, name, location, followers, text)
		count+=1
		print(count)
		store_tweet(word, entity)
	# print (count, text)
	#count all tweets
	# localtime = time.asctime( time.localtime(time.time()) )
	# count+=1
	# curr_count+=1
	# if curr_count >=100000:
	# 	send_message(count)
	# 	curr_count=0