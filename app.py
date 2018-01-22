from flask import Flask, render_template, request, flash,redirect,url_for
import pandas as pd
import numpy as np

 
#data file
data_file_template = 'static/data/match_results_{}.csv'

#Facebook image path
fb_image_path = '/static/facebook_images/'

#Twitter image path
tw_image_path = '/static/twitter_images/'

#init data
data = pd.DataFrame({'A' : []})

app = Flask(__name__)

@app.route("/")
def home():
	return redirect(url_for('index', page=1))

@app.route("/index/<int:page>")
def index(page):
	loadData(page)
	# print(page)
	status = request.args.get('status', '')
	return render_template('index.html', profiles=data, status=status, page=page)

@app.route('/save', methods= ['POST'])
def saveResults():
	global data
	results = request.form
	
	for key, value in results.items():
		if key.isdigit():
			data['label'][int(key)] = value

		if 'observation' in key and value != '':
			key = key.split('_')[1]
			# print(value)

			value = value.replace('\r\n', ' ')
			value = ''.join(ch for ch in value if ch.isalnum() or ch == ' ')
			data['observation'][int(key)] = value

	current_page = results['current_page']
	next_page = results['action']
	
	if results['action'] == 'Next':
		next_page = int(current_page) + 1
	elif results['action'] == 'Previous':
		next_page = int(current_page) - 1
	elif results['action'] == 'Save':
		next_page = int(current_page)

	next_page = str(next_page)

	data_file = data_file_template.format(current_page)
	data.to_csv(data_file,index=False, header=None, columns=['rId','fbId','twId','twUsername','label', 'observation'])

	return redirect(url_for('index', page=next_page, status='success'))

def loadData(page):
	#Update the global varaible
	global data 
	data_file = data_file_template.format(page)
	data = pd.read_csv(data_file,header=None,dtype=np.str)
	data.columns = ['rId','fbId','twId','twUsername', 'label', 'observation']
	data.set_index('rId')
	data.replace("'","")
	data['fbImage'] =  fb_image_path + data['fbId'].astype(str) + '.jpg'
	data['fbUrl'] =  'https://www.facebook.com/' + data['fbId'].astype(str)
	data['twImage'] =  tw_image_path + data['twId'].astype(str) + '.jpg'
	data['twUrl'] =  'https://twitter.com/' + data['twUsername'].astype(str) 	
	


if __name__ == "__main__":
	app.run()