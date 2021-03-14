# csb
##### Repository for MOOC's [Cyber Security Base Project 1](https://cybersecuritybase.mooc.fi/module-3.1)


<br>This web application contains 5 [OWASP Top Ten 2017](https://owasp.org/www-project-top-ten/) Vulnerabilities


##### Disclaimer:
Web application is extremely vulnerable and should not be accessible from internet and code should not be reused.

Link: https://github.com/AnonymousHobbit/csb
# Installation
### Requirements
* python3
* pip3

### Install
* pip3 install flask
* To use the scripts in tools/:
  * pip3 install requests

### Usage
* python3 app.py
* Project should be running on http://localhost:5000/

# Vulnerabilities
## 1. A2:2017-Broken Authentication
#### Source
User credentials location: https://github.com/AnonymousHobbit/csb/blob/master/static/files/users.json#L8<br>
Credentials validation: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L55

#### Description
The flaw is Broken authentication which allows us to sign into authorized pages with default credentials.

I made a page /api/admin with some info for developers about finished pages. You cannot access the page without credentials, but if you make a get request with correct parameters username=Admin and password=Admin you can access it.

1. Go to page http://localhost:5000/api/admin?username=Admin&password=Admin

#### Fix
1. Change default credentials of api in users.json file.

## 2. A3:2017-Sensitive Data Exposure
#### Source
Function to render users.json file: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L43

#### Description
The flaw is sensitive data exposure which means there is some sensitive data accessible.

In this web application you can use the broken authentication vulnerability to find out page /api/admin/users which contains all users and passwords
1. Go to page with default credentials as parameters http://localhost:5000/api/admin?username=Admin&password=Admin
2. Page shows that /api/admin/users page is available.
3. Navigate to http://localhost:5000/api/admin/users?username=Admin&password=Admin and once again remember to use default credentials to access the page.
4. Page will show a list of users, passwords, their homefolders and their permission levels.

Some of this data could be used to escalate privileges in the website or in the server.

#### Fix
There are multiple ways to fix this vulnerability
1. Change default credentials of api in users.json file.
2. Do not store sensitive data on API unencrypted.
  * Store these information on the server (database) without public access.

## 3. A6:2017-Security Misconfiguration
#### Source
Configuration: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L115
#### Description

This flaw is security misconfiguration which means, user is able to exploit the web application because some flaw in software or development environment is left in production.

Website has blog system which decides which blog to show by url /blog/<id>. If id doesn't exist website will go to Werkzeug debugger environment which allows python commands in Server.

1. Go to http://localhost:5000/blog/0
2. Change /blog/0 to /blog/1337
3. When Werkzeug page has loaded, open interactive console by clicking on little console icon on the right when hovering.
4. You can now execute any python command on the server
5. Vulnerability now escalated from Security misconfiguration to Remote Code Execution (RCE).

#### Fix
1. Navigate to app.py and remove line 115.
2. Remember to remove debug=True from line 116 when in production.

## 4. A1_2017-Injection
#### Source
Function which includes injection: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L90

#### Description
The flaw allows user to have Remote Code Execution or make unauthorized actions by injecting malicious data.

When path is entered that doesn't exist, it will throw an error message. However user entered path is directly rendered into the html without sanitization. This allows what is called server side template injection (SSTI)

The injection is possible because page is using jinja2 as a view engine, all python code used in html should be inside {{}}. Therefore because input is not sanitized properly and rendered straight to html, user can execute python inside html.

Reproduce the bug:
1. Go to http://localhost:5000/leet_haxor
2. It shows an error message, after that go to http://localhost:5000/{{7*7}}
3. Now the page should show "Page 49 not found" because it executed the python code.

Basically now this vulnerability allows an attacker to execute commands on server to achieve a reverse shell or fetching SSH private keys.

#### Fix
To fix this error you need to pass data into html file instead of directly render it into html.

On app.py file
1. Move html code inside template variable into error.html file. The file is inside templates/error.html
2. Replace line 110:
  * return render_template("error.html", error=f"Page {path} not found")


## 5. A7:2017-Cross-Site Scripting (XSS)
#### Source
Function which includes xss: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L90

#### Description
The flaw allows user to execute javascript on the website. When user can execute js, its possible to steal some secrets stored in variables, make requests to the server etc.

In this website vulnerability works kind of the same as the templation injection does. Because error page doesn't sanitize input and renders it with html. it allows cross site scripting.

Reproduce the bug:
1. Go to http://localhost:5000/leet_haxor
2. After you see the error message, go to http://localhost:5000/<script>alert("Leet haxor")</script>
3. Now you have working xss, feel free to play around with it.

#### Fix
To fix this error you need to pass data into html file instead of directly render it into html.

On app.py file
1. Move html code inside template variable into error.html file. The file is inside templates/error.html
2. Replace line 110 with:
  * return render_template("error.html", error=f"Page {path} not found")

## 6. A8:2017-Insecure Deserialization
#### Source
Function which deserializes: https://github.com/AnonymousHobbit/csb/blob/master/app.py#L72

#### Description
##### Serialization explained
Serialization is a process which makes complex object data into simpler bytes data to send everywhere and to handle within requests.

For example if we have data: {'name': 'CSB', 'grade': 4} we could serialize and base64 encode it into gAN9cQAoWAQAAABuYW1lcQFYAwAAAENTQnECWAUAAABncmFkZXEDSwR1Lg==. Now its much easier to send with requests.

Deserialization process now would decode the base64 and then deserialize the bytes back into readable data.

To test the process:
  * python tools/serialize.py test

##### Explaining the vulnerability
So in this web application when navigated to http://localhost:5000/backup there is a search form. The application takes the form data and tries to use python pickle library to deserialize and base64 encode the data.

This means the code deserializes anything if the data is valid and already serialized + base64 encoded.

##### Exploitation
When serializing an object, pickle needs information on how to serialize the object, so it will find a __reduce __() method to get some information. When the data is unpickled the __reduce __() is called with function as a first argument and tuple of arguments for the function.

We can create a python class which contains the reduce method that includes system commands and when the server unpickles and decodes the data, the malicious commands will be executed.

###### Automated exploitation
I made a tool which crafts the payload and exploits it:
* python3 tools/exploit.py whoami

Running it will return a result that includes server username.

###### Manual exploitation:
1. Go to http://localhost:5000/backup
2. Craft the serialized payload:
  * python3 tools/serialize.py payload
3. Copy the payload into clipboard
4. On the backup page enter the payload into the search bar and press enter
5. The response should be your own username now because the app is running on your user.

## Fix
Simple fix for this issue is to never pickle data from untrusted source.

On app.py
1. Remove line 81 and 82
2. Handle the search data better without pickling it.
