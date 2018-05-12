from flask import Flask, render_template, request
import requests
import json
import os
from secretsharing import SecretSharer as Shamir
import numpy as np
import time
from werkzeug.contrib.cache import SimpleCache
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
logging.basicConfig()

cache = SimpleCache()
app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)  # DEBUG

# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)


@app.route('/')
def hello_world():
    return 'Welcome to test'

#request function that receive clients' vectors with jason form
@app.route('/server_0_uploader', methods = ['POST'])
def upload_request_():
	if request.method == 'POST':
		request_json  = request.get_json()
		#print request_json
		u_0 = np.array(request_json.get('u_0'))
		u_1 = np.array(request_json.get('u_1'))
		u_2 = np.array(request_json.get('u_2'))
		v_0 = np.array(request_json.get('v_0'))
		v_1 = np.array(request_json.get('v_1'))
		v_2 = np.array(request_json.get('v_2'))
		# v1_square_0 = np.array(request_json.get('v_0_square'))
		# v1_square_1 = np.array(request_json.get('v_1_square'))
		# v1_square_2 = np.array(request_json.get('v_2_square'))
		# use reshape to perform 1-d array transpose
		u_0_v_0 = u_0.reshape([-1,1]).dot(v_0.reshape([1,-1]))
		u_1_v_1 = u_1.reshape([-1,1]).dot(v_1.reshape([1,-1]))
		u_2_v_2 = u_2.reshape([-1,1]).dot(v_2.reshape([1,-1]))

		# u_0_v_0_square = u_0.reshape([-1,1]).dot(v1_square_0.reshape([1,-1]))
		# u_1_v_1_square = u_1.reshape([-1,1]).dot(v1_square_1.reshape([1,-1]))
		# u_2_v_2_square = u_2.reshape([-1,1]).dot(v1_square_2.reshape([1,-1]))

		batch_list = np.array([u_0_v_0,u_1_v_1,u_2_v_2])
		# batch_square_list = [u_0_v_0_square,u_1_v_1_square,u_2_v_2_square]
		# batch_list = np.array([batch_list, batch_square_list])
		batch_result_save(batch_list)

		return 'message sent'

#batch function that used to save client's results
def batch_result_save(batch_list):
	batch_result = get_batch_result()
	if (type(batch_result) is not np.ndarray):
		set_batch_result(batch_list)
	else:
		for i in range(0,3):
			batch_result[i] = batch_result[i] + batch_list[i]
		set_batch_result(batch_result)

#used to print result for simple demo, will be replaced if database is implemented
def batch_result():
	batch_result = get_batch_result()
	if (type(batch_result) is not np.ndarray): 
		print "message is empty"
	else:
		print recover(batch_result)
		set_batch_result(None)


#recover function perform database reconstruction
def recover(s):
	db = []

	for i in range(np.shape(s)[1]):
		for j in range(np.shape(s)[2]):
			tmp1 = []
			for k in range(np.shape(s)[0]):
				tmp1.append(str(k+1)+"-"+str(hex(s[k][i][j]))[2:-1])
			answer = Shamir.recover_secret(tmp1)
			if len(answer) % 2 == 1:
				answer = '0' + answer
			db.append(answer.decode('hex'))
	return db

def get_batch_result():
	return cache.get('batch_result')

def set_batch_result(batch_input):
	cache.set('batch_result', batch_input, timeout=5 * 60)

scheduler.add_job(
    func=batch_result,
    trigger=IntervalTrigger(seconds=8),
    id='batch_result',
    name='Print datebase with 5s batch',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)


