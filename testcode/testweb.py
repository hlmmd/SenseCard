from flask import Flask
from flask import request

app = Flask(__name__)

data = {
    'a':'11',
    'b':'22'
}

@app.route('/eventRcv', methods=['POST'])
def eventRcv():
    print(request.data)
    return '<h1>Home</h1>'

@app.route('/', methods=['GET'])
def home():
    return data

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run()