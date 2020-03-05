import json

from werkzeug.utils import secure_filename

from app import app, db
from flask import request, render_template, jsonify
import os

from app.api.utils import Pic_str, Reptile
from app.models import WellPaper

basedir = os.path.abspath(os.path.dirname(__file__))


# __file__ 表示当前文件的绝对路径
# os.path.dirname(__file__)当前文件的绝对路径


@app.route('/index')
def show():
    return render_template("index.html")


@app.route('/upload')
def showUp():
    return render_template("upload.html")


@app.route('/manage')
def showManage():
    return render_template("manage.html")


@app.route('/reptile')
def showReptile():
    return render_template("reptile.html")


# 图片的上传
@app.route('/uploads', methods=['POST'])
def savePaper():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']
    fname = secure_filename(f.filename)  # secure_filename模块
    ext = fname.rsplit('.', 1)[1]
    new_filename = Pic_str().create_uuid() + '.' + ext
    # 保存到本地
    f.save(os.path.join(file_dir, new_filename))
    # 记录到数据库
    paper = WellPaper(new_filename, '无', os.path.join(file_dir, new_filename))
    db.session.add(paper)
    db.session.commit()
    # 日志
    app.logger.info(new_filename + "上传到服务器")
    return jsonify({"success": 0, "msg": "上传成功"})


# 从数据库中获取壁纸的信息（id,type,url）
@app.route('/getInfo', methods=['POST'])
def getInfo_from_database():
    data = WellPaper.query.all()  # all()以列表的形式返回查询结果
    result = {}
    for i, element in enumerate(data):
        result[i] = element.to_dict()
    return json.dumps(result)


# 修改数据库中壁纸的信息
@app.route('/changeInfo', methods=['POST'])
def change_paper_info():
    data = json.loads(request.data)
    paper = db.session.query(WellPaper).filter(WellPaper.wp_id == data['id']).first()
    if paper is None:
        app.logger.warning("非法操作")
        return jsonify({"success": 1})
    else:
        well = paper.to_dict()
        if well['wp_type'] is not data['type']:
            paper.wp_type = data['type']
            db.session.add(paper)
            db.session.commit()
            app.logger.info(well['wp_id'] + "类别改为：" + data['type'])
        return jsonify({"success": 0})


# 根据id删除壁纸
@app.route('/toggleDelete', methods=['POST'])
def paper_delete():
    data = json.loads(request.data)
    # 需要改进
    for d in data:
        paper = db.session.query(WellPaper).filter(WellPaper.wp_id == d['id']).first()
        db.session.delete(paper)
        # 删除本地的对应图片
        os.remove(paper.wp_url)
        app.logger.info(paper.wp_id+"已经被删除")
    db.session.commit()
    return jsonify({"success": 0})


# 爬虫写入图片
@app.route('/reptile_img', methods=['POST'])
def reptileImg():
    data = json.loads(request.data)
    url = data.get('url')
    start = data.get('start')
    end = data.get('end')
    type = data.get('type')
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    r = Reptile(file_dir)
    for i in range(int(start), int(end)):
        name = r.crawling(url.replace(start, str(i)))
        paper = WellPaper(name, type, os.path.join(file_dir, name))
        db.session.add(paper)
        app.logger.info(name + "上传到服务器;种类:" + type)
    db.session.commit()
    return jsonify({"success": 0})
