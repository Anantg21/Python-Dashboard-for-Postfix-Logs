from flask import Flask, render_template, Blueprint
import socket
import re

host_name = socket.getfqdn()
# Get the dates from the maillog file ##

errors = Blueprint('error', __name__)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
	file = open('maillog', 'r').read()
	# find month and dates and only all string lines in file
	match_all = re.findall(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{2})', file)
	match_sf = re.findall(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{2}).*(sent|failed|deferred)', file)
	# group unique dates and store as list
	uniq_list_all = sorted(list(set(match_all)))
	uniq_list_sf = list(match_sf)
	v = []
	for item in uniq_list_all:
		# Join first 6 characters in line
		uniq_item = ''.join(item)
		# print(uniq_item)
		# initiate count to zero for each unique date
		count = 0
		count1 = 0
		count2 = 0
		for jtem in uniq_list_sf:
			if ''.join(jtem)[:5] == uniq_item:
				if jtem[2] == 'sent':
					count = count + 1
				elif jtem[2] == 'failed':
					count1 = count1 + 1
				else:
					count2 = count2 + 1
		vs = (' '.join(item[:6]), count, count1, count2 )
		v.append(vs)
		# print(v)
	return render_template('testing.html', sample=v, sample1=host_name, sample2=0, sample3=0)


@app.route("/about/")
def about():
	msg = "Welcome"
	return render_template('about.html', msg=msg)


@app.errorhandler(404)
def not_found_error():
	message1 = "404"
	return render_template('404.html', message1=message1), 404


@app.errorhandler(403)
def not_found_error():
	message1 = "403"
	return render_template('404.html', message1=message1), 403


@app.errorhandler(500)
def not_found_error():
	message1 = "500"
	return render_template('404.html', message1=message1), 500


if __name__ == "__main__":
	app.run(debug=True)