from app import app, db
from flask import request, render_template, jsonify
from app.models import User


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/login/', methods=['GET'])
def u_login():
    account = request.args.get("account")
    password = request.args.get("password")
    data = db.session.query(User).filter(User.u_account == account).first()
    result = data.to_dict()
    if password == result['u_password']:
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0})


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/userReg/', methods=['GET'])
def userReg():
    name = request.args.get("name")
    account = request.args.get("account")
    password = request.args.get("password")
    user = User(account,password,name)
    db.session.add(user)
    db.session.commit()
    app.logger.info(account+"用户注册")
    return "register success"
