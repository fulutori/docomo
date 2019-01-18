#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import types
import os
import sys
import re
import datetime

#docomo対話API
KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#エンドポイントの設定
endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
url = endpoint.replace('REGISTER_KEY', KEY)
headers = {'Content-type': 'application/json'}
payload = {'utt' : '', 'context': ''}

while True:
	status.created_at += datetime.timedelta(hours=9)
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	data = r.json()

	payload['utt'] = utt_content #uttを更新
	payload['context'] = context #contextを更新

	response = data['utt']
	context = data['context']
	user_check(user, context) #user_listにユーザー名とcontextを関連付けて格納

	print ("context: %s" %(context))
	print ("response: %s" %(response))
