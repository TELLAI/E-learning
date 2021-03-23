from flask import Flask, render_template, request, redirect, url_for
import logging
from logging import FileHandler
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(
    host="mysqlContainer",
    user=os.environ.get("userDB"),
    password=os.environ.get('passwordBD'), 
    database= os.environ.get('database')
                )

mycursor = mydb.cursor()

app = Flask(__name__)
CORS(app)

# setting logger
app.logger.setLevel("INFO")
for h in app.logger.handlers:
    app.logger.removeHandler(h)
handler = FileHandler("app.log")
handler.setLevel("INFO")
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(threadName)s :: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
print(app.logger.handlers)
logging.getLogger("werkzeug").addHandler(handler)
# logger set

# homepage
@app.route('/')
def greeting():
    app.logger.info("opening homepage")
    return render_template('index.html')

# section python
@app.route('/sections/python/')
def select_python():
    app.logger.info("choosing python section")
    mycursor.execute("use learning;")
    mycursor.execute("SELECT * FROM Python")
    result = mycursor.fetchall()
    return render_template('sectionPython.html', result=result, section='Python', \
                            description='Python is a leader programming language. \
                            It’s one of the world’s most popular high-level programming\
                            languages and remains a firm favorite among many programmers.\
                            It is easy to learn and use, it is suitable for any tasks and \
                            it is incredibly reliable. Learn Pyhton with the collection of \
                            good quality videos we gathered for you from Youtube')

# section Cloud
@app.route('/sections/cloud/')
def select_cloud():
    app.logger.info("choosing cloud section")
    mycursor.execute("use learning;")
    mycursor.execute("SELECT * FROM Cloud")
    result = mycursor.fetchall()
    return render_template('sectionCloud.html', result=result, section='Cloud', description='Cloud \
                            refers to servers that are accessed over the Internet, and the software and databases \
                            that run on those servers. Cloud servers are located in data centers all over the world. \
                            By using cloud computing, users and companies don\'\t have to manage physical servers \
                            themselves or run software applications on their own machines.')

# section Docker
@app.route('/sections/docker/')
def select_docker():
    app.logger.info("choosing sectionDocker section")
    mycursor.execute("use learning;")
    mycursor.execute(f"SELECT * FROM Docker")
    result = mycursor.fetchall()
    return render_template('sectionDocker.html', result=result, section='Docker', description='Docker is \
                            Vestibulum magna massa, rutrum et justo eget, rhoncus dapibus lorem. \
                            Nulla facilisis erat non turpis tempor, vitae porta enim posuere. \
                            Nam pretium at nulla at volutpat. Vestibulum vitae nibh ac enim \
                            tempor tincidunt. Ut purus massa, laoreet non consectetur ac, ornare \
                            ut nisi. Maecenas euismod varius odio. Ut in dictum ligula.')

#section js
@app.route('/sections/js/')
def select_js():
    app.logger.info("choosing js section")
    mycursor.execute("use learning;")
    mycursor.execute(f"SELECT * FROM Javascript")
    result = mycursor.fetchall()
    return render_template('sectionJS.html', result=result, section='JavaScript', description='JavaScript is \
                            Vestibulum magna massa, rutrum et justo eget, rhoncus dapibus lorem. \
                            Nulla facilisis erat non turpis tempor, vitae porta enim posuere. \
                            Nam pretium at nulla at volutpat. Vestibulum vitae nibh ac enim \
                            tempor tincidunt. Ut purus massa, laoreet non consectetur ac, ornare \
                            ut nisi. Maecenas euismod varius odio. Ut in dictum ligula.')

#section add video
@app.route('/add', methods=['POST', 'GET'])
def add_page():
    if request.method == 'POST':
        name = request.form["name"]
        chaine = request.form["chaine"]
        categorie = request.form["menu"]
        description = request.form["description"]
        url = request.form["url"]
        val = [name, chaine, url, description]
        sql = f"INSERT INTO {categorie} (name, chaine, url, description) VALUES ("
        for ii, i in enumerate(val):
            if ii == 3:
                sql = sql + "'" + i + "');"
            else:
                sql = sql + "'" + i + "', "
        mycursor.execute("use learning;")
        mycursor.execute(sql)
        mydb.commit()
        mycursor.execute(f"SELECT MAX(id) from {categorie};")
        data = mycursor.fetchall()
        id = data[0][0]
        if categorie == "Python":
            return redirect(url_for("watch_python", id=id))
        if categorie == "Cloud":
            return redirect(url_for("watch_cloud", id=id))
        if categorie == "Docker":
            return redirect(url_for("watch_Docker", id=id))
        if categorie == "Javascript":
            return redirect(url_for("watch_js", id=id))
    else:
        return render_template('addPage.html')

app.route('/add/submit_video/')
def submit_video():
    app.logger.info("start insert of video in bdd")
    mycursor.execute(f"SELECT * FROM Javascript")
    result = mycursor.fetchall()

# ##########################################################
# # endpoint + parameter Python
@app.route('/sections/python/watch/<id>')
def watch_python(id):
    app.logger.info("choosing video from python section")
    mycursor.execute("use learning;")
    mycursor.execute(f'SELECT * FROM Python WHERE ID={id}')
    result = mycursor.fetchall()
    return render_template('watch.html', result=result)

# # endpoint + parameter Cloud
@app.route('/sections/cloud/watch/<id>')
def watch_cloud(id):
    app.logger.info("choosing video from cloud section")
    mycursor.execute("use learning;")
    mycursor.execute(f'SELECT * FROM Cloud WHERE ID={id}')
    result = mycursor.fetchall()
    return render_template('watch.html', result=result)

# # endpoint + parameter Docker
@app.route('/sections/docker/watch/<id>')
def watch_Docker(id):
    app.logger.info("choosing video from Docker section")
    mycursor.execute("use learning;")
    mycursor.execute(f'SELECT * FROM Docker WHERE ID={id}')
    result = mycursor.fetchall()
    return render_template('watch.html', result=result)

# # endpoint + parameter JS
@app.route('/sections/js/watch/<id>')
def watch_js(id):
    app.logger.info("choosing video from js section")
    mycursor.execute("use learning;")
    mycursor.execute(f'SELECT * FROM Javascript WHERE ID={id}')
    result = mycursor.fetchall()
    return render_template('watch.html', result=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4020, debug=True)
