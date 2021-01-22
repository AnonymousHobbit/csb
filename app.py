import os
import pickle
from flask import Flask, request, render_template_string,render_template, jsonify, redirect, make_response
import base64

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

users = [
    {'id': 0,
     'username': 'root',
     'password': '#G3T_PwN3D!',
     'home_location': '/root/',
     'permissions_level': '*'},
    {'id': 1,
     'username': 'Admin',
     'password': 'Admin',
     'home_location': '/home/admin',
     'permissions_level': 2},
    {'id': 2,
     'username': 'Hobbit',
     'password': 'CSB{BR0K3N_AU7TH3NT1C4T10N}',
     'home_location': '/home/hobbit',
     'permissions': 1}
]

pages = [
    {'id': 0,
     'page': "/api/admin/development",
     'status': "Not finished"
     },
    {'id': 1,
     'page': "/api/admin/users",
     'status': "Ready"
     },
    {'id': 2,
     'page': "/api/admin/panel",
     'status': "Not finished"
     }
]

#2. Broken Authentication
#3. Sensitive Data Exposure
@app.route("/api/admin/users", methods=["GET"])
def user_api():
    if request.args.get("username") == "Admin" and request.args.get("password") == "Admin":
        return jsonify(users)
    else:
        return "You are not allowed to view this page", 301

@app.route("/api/admin", methods=["GET"])
def admin_api():
    if request.args.get("username") == "Admin" and request.args.get("password") == "Admin":
        return jsonify(pages)
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
@app.route("/backup", methods=["GET"])
def backup():
    info = request.args.get("info")
    if info == None:
        return "This is a secure backup service"
    try:
        data = base64.b64decode(info)
        deserialized = pickle.loads(data)
        return f"{deserialized.decode().strip()}"
    except:
        return f"No backup files found for {info}"

#1. Server Sided Template Injection
#7. Cross-Site Scripting
@app.errorhandler(404)
def not_found(e):
    data = {'flag':"CSB{SST1_INJ3C7I0N}"}
    path = request.path[1:]
    template = f'''Page {path} not found'''
    return render_template_string(template, data=data), 404

@app.route('/')
def main():
    template = '''Webapp powered by Flask/Jinja2'''
    return render_template_string(template)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
