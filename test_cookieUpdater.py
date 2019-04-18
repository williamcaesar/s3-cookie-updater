from unittest import TestCase
from updater import CookieUpdater


class TestCookieUpdater(TestCase):
    def test___update_local(self):
        updater = CookieUpdater()
        updater.update_local('.')
