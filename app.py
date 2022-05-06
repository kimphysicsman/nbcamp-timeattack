from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbtimeattack


app = Flask(__name__)

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_confirm():
    id = request.args.get('id')
    pw = request.args.get('pw')

    user = db.users.find_one({'id': id, 'pw': pw})
    login_status = 0

    if user is None:
        msg = '로그인 실패'
    else:
        msg = '로그인 성공'
        login_status = 1

    return jsonify({'result': login_status, 'msg': msg})

@app.route('/signup', methods=['POST'])
def signup():
    id = request.form['id_give']
    pw = request.form['pw_give']

    user = db.users.find_one({'id': id})
    if user is None:
        doc = {'id': id, 'pw': pw}
        db.users.insert_one(doc)
        msg = '회원가입 성공'
    else :
        msg = '회원가입 실패'

    return jsonify({'msg': msg})


@app.errorhandler(401)
def error_handling_401(error):
    return jsonify({'Error': "Some Error.."}, 401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)