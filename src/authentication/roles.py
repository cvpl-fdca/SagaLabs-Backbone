# authentication/roles.py
import json


class UserRole:
    """Base class for all roles"""

    def __init__(self, user):
        self.user = user


class SuperAdmin(UserRole):
    def has_access_to_range(self, range_name):
        # A SuperAdmin has access to all ranges
        return True


class RangeAdmin(UserRole):
    def has_access_to_range(self, range_name):
        # A RangeAdmin has access to ranges they are assigned
        return range_name in self.user['ranges']


class RangeUser(UserRole):
    def has_access_to_range(self, range_name):
        # A RangeUser has access to ranges they are assigned
        return range_name in self.user['ranges']
