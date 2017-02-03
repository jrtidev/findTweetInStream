from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

#function responsible for sending message with found tweet
def send_message(entity, word):
    recipient = 'RECIPIENT_EMAIL'
    sender_lgn = 'SENDER_EMAIL'
    sender_pwd = 'SENDER_PASSWORD'
    subj = 'Update on #%s' % (word)
    email_body = 'Hello, Artem!\nThis is what happened:\n'+entity  

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

#twitter application credentials
at = 'ACCESS_TOKKEN'
ats = 'ACCESS_TOKKEN_SECRET'
ckey = 'CONSUMER_KEY'
cs = 'CONSUMER_SECRET'

twitter_stream = TwitterStream(auth=OAuth(at, ats, ckey, cs), domain='stream.twitter.com')
iterator = twitter_stream.statuses.sample()
count = 0
curr_count=0

word = raw_input('Input word you need to find: ')
word = word.decode('utf-8')
print(word)

for i in iterator:
	try:
		text = i['text']
		text=text.lower()
	except KeyError:
		text = 'None'
	try:
		user_id = i['user']['id']
	except KeyError:
		user_id = 'None'
	try:	
		name = i['user']['screen_name']
	except KeyError:
		name = 'None'
	try:	
		location = i['user']['location']
	except KeyError:
		location = 'None'
	try:	
		followers = i['user']['followers_count']
	except KeyError:
		followers = 'None'
	
	#find word in twitter stream
	if word in text:
		entity = 'Usrer ID: %s, \n User Name: %s, \n Location: %s, \n Followers: %s, \n Message: %s, \n' % (user_id, name, location, followers, text)
		entity = entity.encode('utf-8')
		count+=1
		print(count)
		store_tweet(word, entity)
		send_message(entity, word)