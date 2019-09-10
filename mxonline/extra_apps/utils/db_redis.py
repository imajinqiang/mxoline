

import redis
db = redis.Redis(host='127.0.0.', password='123456', port=6379, db=0, charset='utf8', decode_responses=True)

db.set('code', '123111')

print(db.get('code'))
