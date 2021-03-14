import os
import pickle
from flask import Flask, request, render_template_string,render_template, jsonify, redirect, make_response
import base64
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Security misconfiguration
@app.route("/blog/<id>")
def get_blog(id):
    if not id.isnumeric():
        template = f'''
        <head>
            <title>Page not found</title>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
          <nav class="navbar">
            <a href="/">Home</a>
            <a href="/backup">Backups</a>
            <a href="/blogs">Blogs</a>
          </nav>
          <section id="page">
             <h2>Id must be an integer and more than 0</h2>
          </section>
        </body>'''
        return render_template_string(template)
    f = open('static/files/blogs.json',"r")
    data = json.loads(f.read())
    return render_template("blog.html", blog=data["blogs"][int(id)])

@app.route("/blogs")
def get_blogs():
    f = open('static/files/blogs.json',"r")
    data = json.loads(f.read())
    return render_template("blogs.html", blogs=data["blogs"])

#2. Broken Authentication
#3. Sensitive Data Exposure
@app.route("/api/admin/users", methods=["GET"])
def user_api():
    f = open('static/files/users.json',"r")
    data = json.loads(f.read())
    if request.args.get("username") == data["users"][1]["username"] and request.args.get("password") == data["users"][1]["password"]:
        return jsonify(data)
    else:
        return "You are not allowed to view this page", 301

@app.route("/api/admin", methods=["GET"])
def admin_api():
    f = open('static/files/users.json',"r")
    data = json.loads(f.read())
    if request.args.get("username") == data["users"][1]["username"] and request.args.get("password") == data["users"][1]["password"]:
        f = open('static/files/api-pages.json',"r")
        data = json.loads(f.read())
        return jsonify(data)
    else:
        return "You are not allowed to view this page", 301

#3. Sensitive Data Exposure
@app.route("/api/note.txt")
def info():
    template = """
    <p>Hey Steve! We should definetly create some kind of login form for our API. Credentials with url is not secure. - Chris  10.12.2020</p>\n\n
    <p>Hey Jack! Did you remember to change the credentials for /api/admin API? - Chris  12.12.2020</p>\n\n
    <p>I mean those credentials are easily found from some wordlist like rockyou. - Chris 13.12.2020</p>\nCSB{S3NS1T1V3_D47A}"""
    return render_template_string(template)

#6. Insecure Deserialization
@app.route("/backup", methods=["GET", "POST"])
def backup():

    if request.method == "GET":
        return render_template("backup.html")
    if request.method == "POST":
        info = request.form["search"]
        try:

            data = base64.b64decode(info)
            deserialized = pickle.loads(data)
            return render_template("backup.html", error_data=deserialized.decode().strip())
        except:
            msg = f"No backup files found for {info}"
            return render_template("backup.html", error_data=msg)

#7. Cross-Site Scripting
#1. Server Sided Template Injection
@app.errorhandler(404)
def not_found(e):
    data = {'flag':"CSB{SST1_INJ3C7I0N}"}
    path = request.path[1:]
    template = f'''
    <head>
        <title>Page not found</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
      <nav class="navbar">
        <a href="/">Home</a>
        <a href="/backup">Backups</a>
        <a href="/blogs">Blogs</a>
      </nav>
      <section id="page">
         <h2>Page {path} not found</h2>
      </section>
    </body>'''
    #return render_template("error.html", error=f"Page {path} not found")
    return render_template_string(template, data=data), 404

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
    os.environ["WERKZEUG_DEBUG_PIN"] = "off"
    app.run(debug=True, host='0.0.0.0')
