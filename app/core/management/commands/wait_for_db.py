import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """django command to pause execution until db is ready"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('DB unavailable, waiting for 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Db is already available!'))
