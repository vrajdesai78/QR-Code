import base64
from io import BytesIO
from flask import Flask, render_template, request, send_file, url_for, redirect
from pyrebase import initialize_app
import qrcode

app = Flask(__name__)

firebaseConfig = {
    "apiKey": "AIzaSyBx-p6-8oVzUYGeC0B18zhP5SEf91E0L8c",
    "authDomain": "qr-code-gen-project.firebaseapp.com",
    "projectId": "qr-code-gen-project",
    "databaseURL": "https://qr-code-gen-project-default-rtdb.firebaseio.com",
    "storageBucket": "qr-code-gen-project.appspot.com",
    "messagingSenderId": "55659146859",
    "appId": "1:55659146859:web:1164eb05a26f39378d0b2e",
    "measurementId": "G-R363WWCLRL"
}

firebase=initialize_app(firebaseConfig)
auth=firebase.auth()

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.sign_in_with_email_and_password(email, password)
        return redirect('/home')
    return render_template('registration.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['re_pass']
        if password == c_password:
            auth.create_user_with_email_and_password(email,password)
            return redirect('/home')
        return render_template('registration.html')
    return render_template('registration.html')

@app.route("/show_qr", methods=['POST','GET'])
def show_qr():
    if request.method == "POST":
        name = request.form['name']
        en_number = request.form['en_number']
        address = request.form['address']
        phone_number = request.form['phone_no']
        blood_grp = request.form['blood_grp']
        stream = request.form['stream']
        msg = f"""Name: {name}
Enrollment No. {en_number}
Address: {address}
Phone Number: {phone_number}
Blood Group: {blood_grp}
Stream: {stream}"""
        buffer = BytesIO()
        img = qrcode.make(msg)
        img.save(buffer)
        buffer.seek(0)
        encoded_img = base64.b64encode(buffer.getvalue())
        return render_template('showQR.html', img = encoded_img.decode('utf-8'))
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True)
