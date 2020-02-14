import redis


def conn():
    pool = redis.ConnectionPool(host='120.77.203.242', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r
