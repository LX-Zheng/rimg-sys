import json

from app import app, db
from flask import request, jsonify, Response
from app.models import WellPaper, UserPaper


@app.route('/getPaper', methods=['POST'])
def getPaper():
    data = json.loads(request.data)
    try:
        mid = db.session.query(WellPaper).filter(WellPaper.wp_type == data['type']).all()
        favorate = db.session.query(UserPaper).filter(UserPaper.u_id == data['u_id']).all()
    except:
        db.session.rollback()
        mid = db.session.query(WellPaper).filter(WellPaper.wp_type == data['type']).all()
        favorate = db.session.query(UserPaper).filter(UserPaper.u_id == data['u_id']).all()
    db.session.close()
    result = dict()
    fav = list()
    for i, element in enumerate(favorate):
        fav.append(element.to_dict().get('wp_id'))
    for i, element in enumerate(mid):
        e = element.to_dict()
        result[i] = e
        result.get(i)['wp_url'] = "http://127.0.0.1:5000/photo/" + result.get(i)['wp_id']
        if e.get('wp_id') in fav:
            result.get(i)['favorate'] = True
        else:
            result.get(i)['favorate'] = False
    return json.dumps(result)


# 客户端查看图片
@app.route('/photo/<imageId>.jpg')
def get_frame(imageId):
    with open(r"app/static/upload/{}.jpg".format(imageId), "rb") as f:
        image = f.read()
        resp = Response(image, mimetype="iamge/jpg")
        return resp


# 用户添加收藏
@app.route('/addPaper', methods=['POST'])
def addPaper():
    data = json.loads(request.data)
    u_id = data.get('u_id')
    wp_id = data.get('wp_id')
    wp_url = data.get('wp_url')
    paper = db.session.query(UserPaper).filter(UserPaper.wp_id == wp_id).first()
    # if paper exist execute delete else add new paper
    # return 0 execute delete
    # return 1 execute add
    if paper:
        db.session.delete(paper)
        db.session.commit()
        db.session.close()
        return jsonify({'success': '0'})
    else:
        paper = UserPaper(u_id, wp_id, wp_url)
        db.session.add(paper)
        db.session.commit()
        db.session.close()
        return jsonify({'success': '1'})


# search user favorate
@app.route('/getFavorate', methods=['POST'])
def getFavorate():
    data = json.loads(request.data)
    u_id = data.get('u_id')
    mid = db.session.query(UserPaper).filter(UserPaper.u_id == u_id).all()
    db.session.close()
    result = dict()
    for i,element in enumerate(mid):
        result[i] = element.to_dict()
    return json.dumps(result)
