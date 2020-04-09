import json

from app import app, db
from flask import request, jsonify, Response

from app.dbUtils import config
from app.models import WellPaper, UserPaper, UserLoad

# redis
redis = config.conn()


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
    print(result)
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
    # wp = data.get('wp')
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
        # 所有用户收藏的物品列表
        # redis.hset('items', wp, json.dumps({'wp_id': wp_id, 'wp_url': wp_url}))
        # 添加用户的收藏记录
        # redis.hset('user_item', u_id, json.dumps({wp: 1.0}))
        # 将收藏记录添加到redis
        # val = redis.hget('hot', wp)
        # if val is None:
        #     redis.hset('hot', wp, 1)
        # else:
        #     redis.hset('hot', wp, int(val) + 1)
        return jsonify({'success': '1'})


# search user favorate
@app.route('/getFavorate', methods=['POST'])
def getFavorate():
    data = json.loads(request.data)
    u_id = data.get('u_id')
    mid = db.session.query(UserPaper).filter(UserPaper.u_id == u_id).all()
    db.session.close()
    result = dict()
    for i, element in enumerate(mid):
        result[i] = element.to_dict()
    return json.dumps(result)


# record user behavior
@app.route('/record', methods=['POST'])
def record():
    data = json.loads(request.data)
    print(data)
    return jsonify({'success': '1'})


# user download image
@app.route('/download', methods=['POST'])
def download():
    data = json.loads(request.data)
    wp_id = data.get('id')
    u_id = data.get('u_id')
    wp_url = data.get('wp_url')
    load = db.session.query(UserLoad).filter(UserLoad.u_id == u_id, UserLoad.wp_id == wp_id).first()
    if not load:
        load = UserLoad(u_id, wp_id, wp_url)
        db.session.add(load)
        db.session.commit()
    db.session.close()
    return jsonify({'success': 1})


# user download record
@app.route('/getLoad', methods=['POST'])
def getLoad():
    data = json.loads(request.data)
    u_id = data.get('u_id')
    mid = db.session.query(UserLoad).filter(UserLoad.u_id == u_id).all()
    db.session.close()
    result = dict()
    for i, element in enumerate(mid):
        result[i] = element.to_dict()
    return json.dumps(result)


# 从redis中读取壁纸信息
paper = redis.hgetall("metadata")


# recommend function
@app.route('/getRec', methods=['POST'])
def getRec():
    data = json.loads(request.data)
    u_id = data.get('u_id')
    res = redis.zrange(str(u_id), start=0, end=-1)
    result = dict()
    j = 0
    for i in res:
        result[j] = paper[i]
        j += 1
    return json.dumps(result)
