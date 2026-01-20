from django.core.management.base import BaseCommand
import redis


class Command(BaseCommand):
    help = "Flushesh Redis DB data"

    def handle(self, *args, **kwargs):
        try:
            r = redis.Redis(host="localhost", port=6379, db=1)
            if len(r.keys()) > 0:
                del_input = input(
                    f"Redis DB is not emtpy: {r.keys()}; Do you want to delete? (Y/N) "
                )
                if del_input.lower() == "y":
                    r.flushdb()
                    return f"Redis DB flushed successfully"
            else:
                return "No Redis records found! Nothing to clean"
        except redis.exceptions.ConnectionError as e:
            return f"{e}; Please check connection settings!"
