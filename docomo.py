#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import types
import tweepy
import os
import sys
import re
import datetime


#twitterのAPIとか
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#apiを取得
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#docomo対話API
KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#エンドポイントの設定
endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', KEY)
headers = {'Content-type': 'application/json'}
payload = {'utt' : '', 'context': ''}

#ユーザーのcontextを格納
user_list = {}
def user_check(user,context) :
	global user_list
	user_list[user] = context

class Listener(tweepy.StreamListener):
	def on_status(self, status):
		status.created_at += datetime.timedelta(hours=9)
		print ("--------------------------------")
		print (status.text)

		# リプライが来たら返信
		if str(status.in_reply_to_screen_name)=="ツイッターID":
			utt_content = status.text #送られてきたツイート本文
			user = status.user.screen_name #ユーザー名
			print (user_list)
			if (user in user_list.keys()):
				context = user_list[user]
			else:
				context = ''

			payload['utt'] = utt_content #uttを更新
			payload['context'] = context #contextを更新

			#送信
			r = requests.post(url, data=json.dumps(payload), headers=headers)
			data = r.json()

			response = data['utt']
			context = data['context']
			user_check(user, context) #user_listにユーザー名とcontextを関連付けて格納

			#print ("context: %s" %(context))
			#print ("response: %s" %(response))

			tweet = "@" + str(status.user.screen_name) + " " + response + "\n"
			api.update_status(status=tweet,in_reply_to_status_id=status.id)
		return True

	def on_error(self, status_code):
		print('Got an error with status code: ' + str(status_code))
		return True

	def on_timeout(self):
		print('Timeout...')
		return True


listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.userstream()
