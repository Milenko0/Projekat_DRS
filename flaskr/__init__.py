from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/auth/login.html', methods=['GET'])
def homepage():
    return render_template('auth/login.html')

@app.route('/', methods=['POST'])  
@app.route("/auth/login.html", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email!='g@g.com':
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)