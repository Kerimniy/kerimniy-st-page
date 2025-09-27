from flask import Flask, request, jsonify, render_template, redirect
from flask import url_for
from flask import send_file,send_from_directory, abort
from datetime import datetime
import time
import threading  
import subprocess

def ping(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    return 1 if result.returncode == 0 else 0


from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

st = 1
all_st=1
c = 1
last_check_time = "XX:XX:XX"

def r2rgb(x):
        if (x <= 0.5):
            r = 0.9
            g = 1.4 * x
            b = 0.0
        else:
            r = 1.8 * (1 - x)
            g = 0.7
            b = 0.0
            
        r255 = round(r * 255)
        g255 = round(g * 255)
        b255 = round(b * 255)
        return (r255,g255,b255)

         

@app.route("/")
def index():
    global st
    global c
    global all_st
    global last_check_time

    hostname = request.scheme +"://" + request.host
    colors = r2rgb(int(all_st/c*1000)/1000)
    r =colors[0]
    g =colors[1]
    b =colors[2]

    all_time = int(all_st/c*1000)/10

    if st == 0:
        title = "Kerimniy Status Page - Всё плохо"
    else:
        title = "Kerimniy Status Page - Всё ок"

    if st == 0:
        stl_text = "Ничего не работает"
    elif 80 > all_time > 45:  
        stl_text = "Ну норм"
    elif 20 < all_time <= 45: 
        stl_text = "Ну плохо"
    elif all_time < 20:
        stl_text = "Ужасно, нестабильно"
    elif all_time >= 80:
        stl_text = "Ну хорошо"
	

    rgb = f"background-color: rgb({r}, {g}, {b});"
    return render_template("index.html",hostname=hostname,rgb=rgb,st=st,last_check_time=last_check_time,stl_text=stl_text,title=title, all_time=all_time )

@app.route("/get_st")
def get_st():
    global st
    global c
    global all_st
    global last_check_time
    
    r = {"current_st":st, "all_time":int(all_st/c*1000)/10,"last_check_time":last_check_time}
    js = jsonify(r)
    return js
@app.route("/<var>")
def red(var):
    if var != "/" and var != "/get_st":
        return redirect(request.scheme +"://" + request.host)
    else:
        return
        
def monitor():
    global st
    global c
    global all_st
    global last_check_time
    while True:
        current_time = datetime.now().time()
        current_time = current_time.strftime("%H:%M:%S")
        last_check_time = current_time
        c+=1
        st = ping(r"kerimniy.cloudpub.ru")
        all_st+=st
        time.sleep(10)

monitor_thread = threading.Thread(target=monitor, daemon=True)
monitor_thread.start()

if __name__ == '__main__':
   
    app.run(debug=True, host='localhost', port=5000)
    


