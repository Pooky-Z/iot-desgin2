from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index/')
def index():
    return render_template('test2.html')

@app.route('/search/')
def search():
    # arguments
    condition = request.args.get('q')
    print(condition)
    return '用户提交的查询参数是: {}'.format(condition)

# 默认的试图函数， 只能采用get请求
# 如果你想采用post请求，那么要写明
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print("ok")
        # return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        print('username: {}, password: {}'.format(username, password))
        return 'name = {}, password = {}'.format(username, password)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
