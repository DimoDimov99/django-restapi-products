### Course link - https://www.youtube.com/watch?v=6AEvlNgRPNc&list=PL-2EBeDYMIbSXhV8FMC1hVD32Fi6e4l2u
---
- Stopped at https://youtu.be/6AEvlNgRPNc?list=PL-2EBeDYMIbSXhV8FMC1hVD32Fi6e4l2u&t=1104\
- docker exec -it <container_name> psql -U <user> -d <db_name>
- https://stackoverflow.com/questions/26040493/how-to-show-data-in-a-table-by-using-psql-command-line-interface
\x SELECT * FROM <table>; LIMIT 10;
---
Resources:
- https://www.cdrf.co/ - Detailed descriptions, with full methods and attributes, for each of Django REST Framework's class-based views and serializers.
- jwt.io
- research cursor paginator
- Inside connected redis docker instance:
```
redis-cli -n 1 - connects to redis DB instance
KEYS * - returns all cached keys, blocking operation
GET <key_name> - returns value of the given key
```
- python3 manage.py test api.tests.UserOrderTestCase.test_user_order_api_retrieves_only_auth_user_orders