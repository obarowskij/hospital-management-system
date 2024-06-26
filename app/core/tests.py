"""
Test custom Django management commands.
"""

from unittest.mock import patch
import pytest

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


@pytest.mark.django_db
@patch("core.management.commands.wait_for_db.Command.check")
class TestWaitForDbCommand:
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_db_not_ready(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 2 + [True]
        
        call_command('wait_for_db')

        assert patched_check.call_count == 5

        patched_check.assert_called_with(databases = ['default'])

class TestTest(TestCase):
    
    def test_test(self):
        self.assertEqual(1,1)


