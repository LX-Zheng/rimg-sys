from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='', server='120.77.203.242', database='webmanager')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 设置图片地址
UPLOAD_FOLDER = '../static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 设置编码
app.config['JSON_AS_ASCII'] = False

# 创建数据库对象
db = SQLAlchemy(app)

# 跨域
CORS(app, supports_credentials=True)


@app.after_request
def af_request(resp):
    """
    #请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


from app.api import routers
from app.api import index
from app.api import client
