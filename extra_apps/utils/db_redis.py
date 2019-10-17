

import redis
db = redis.Redis(host='127.0.0.1', port=6379, db=0, charset='utf8', decode_responses=True)


print(db.get(str(15614658856)))
