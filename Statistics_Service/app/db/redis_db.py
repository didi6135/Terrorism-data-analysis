import os
import redis
from dotenv import load_dotenv

load_dotenv(verbose=True)


redis_client = redis.StrictRedis(
    host=os.environ['REDIS_HOST'],
    port=6379,
    db=0
)




