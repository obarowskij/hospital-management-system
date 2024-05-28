from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        db_ready=False
        while db_ready is False:
            try:
                self.check(databases=["default"])
                db_ready=True
                print("Database is ready!")
            except (Psycopg2OpError, OperationalError):
                print("Database not ready...")
                time.sleep(1)
