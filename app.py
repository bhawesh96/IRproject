# -*- coding: utf-8 -*-
import traceback, warnings
warnings.filterwarnings("ignore")
import requests
import finalCode


from flask import Flask, render_template, redirect, json, request, session, Markup, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 

res = {}


@app.route('/')
def main():
	return render_template('question.html')
	
@app.route('/', methods=['POST'])
def query():
	query = request.form['query']
	session['queryx'] = query
	return redirect('/evaluated')

def extract(res):
	term = []
	vb = []
	gap = []
	post = []
	for x in res:
		term.append(str(res[x][0]))
		vb.append(res[x][1])
		gap.append(res[x][2])
		post.append(res[x][3])
	return term, vb, gap, post

@app.route('/evaluated')
def cc():
	# term = Markup(['bhawesh', 'ramesh'])
	fruits = Markup(['apple', 'mango'])
	res = finalCode.myIR_Model(session.get('queryx'))
	ret = extract(res)
	term = Markup(ret[0])
	vb = Markup(ret[1])
	gap = Markup(ret[2])
	post = Markup(ret[3])
	print "term : " + str(term)

	return render_template('evaluated.html', term = term, vb = vb, gap = gap, post = post)

def evaluate():
	print 'hey'


if __name__ == "__main__":
	app.run(debug=True,port=5005,use_evalex=False)
	# app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)