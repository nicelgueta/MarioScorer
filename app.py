from flask import Flask, jsonify,abort,make_response,request, render_template, redirect, url_for
import os
import time
import sys
from config import  X
from mongologger import MongoLogger, readabledate
from mongo import BotDB
from mariokeezy import MarioKeezy
from MarioEnterScores import MarioBoard
import pandas as pd

BOTENV = os.environ.get('BOTENV')

class app(Flask):
    def __init__(self,name=__name__):
        super(app,self).__init__(name)
        print('Initialising Bot')
#auth
app = app()
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.MK = MarioKeezy()

#SSL encryption not working on dev server
if BOTENV != 'DEV':
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.route('/logs')
def get_logs():
    list_lines = app.MK.db.printLogs()
    body = '<title>Mario Logs</title><code><h3>LOGS</h3><code>'
    for line in list_lines:
        body+=line
    body+='</code>'
    return body,200

@app.route('/ping')
def ping():
    ret = {'ping':readabledate(time.time()),'version':X['botVersion']}
    return jsonify(ret),200


@app.route('/play')
def mario():
    return render_template('mario.html')

@app.route('/')
def standings():
    with open('templates/mariostandings_raw.html','r') as f:
        html_str = f.read()

    a = MarioBoard(app.MK.db)
    df = a.playerdf.drop(['sigma','draws'],1)
    dfstr = df.to_html(index=False,index_names=False)
    new_str = html_str%dfstr
    with open('templates/mariostandings.html','w') as f:
        f.write(new_str)
        f.close()
    return render_template('mariostandings.html')

@app.route('/mariosubmit',methods=['POST'])
def mariosubmit():
    app.MK.db.log.info('Mario enter score - Request IP: '+str(request.remote_addr))
    print(str(request.form))
    api_txt = request.form['marioSubmit']
    apistr = app.MK.convert_api_string_to_tweet_version(api_txt)
    df = app.MK.runtweetfunc(apistr)
    df = df.drop(['sigma','draws'],1)
    with open('templates/mariosubmit_raw.html','r') as f:
        html_str = f.read()
    dfstr = df.to_html(index=False,index_names=False)
    new_str = html_str%dfstr
    with open('templates/mariosubmit.html','w') as f:
        f.write(new_str)
        f.close()
    return render_template('mariosubmit.html')

@app.route('/getPodium')
def getPodium():
    a = MarioBoard(app.MK.db)
    df = a.playerdf
    print(df)
    df['mu'] = pd.to_numeric(df['mu'])
    df = df.sort_values(['mu'],ascending=False)
    print(df)
    names = list(df.Name)
    return jsonify({'podium':names}),200

def check_type(key,new_value):
    # check value is right Type
    typ = type(V[key])
    #don't eval if meant to be sttr
    if isinstance(V[key],str):
        if '<' in new_value:
            return '__error'
    else:
        new_value = eval(new_value)
    #check type
    if isinstance(new_value,type(V[key])):
        return new_value
    else:
        return '__error'


if __name__ == '__main__':
    app.run()
