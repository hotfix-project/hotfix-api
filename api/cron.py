import redis
from .models import Patch
from django.db import transaction


@transaction.atomic
def store_from_redis():
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, max_connections=10)
    rds = redis.Redis(connection_pool=pool)

    for patch in Patch.objects.select_for_update().all():
        result = rds.hget("apply_count_hash", "report_update?patch_id=%d" % (patch.id))
        if result is not None:
            count = int(result)
            if count > patch.apply_count:
                patch.apply_count = count
                patch.supersave()
        

def main():
    store_from_redis()

if __name__ == '__main__':
    main()
