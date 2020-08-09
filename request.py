import re
import datetime
from roof_terms import partners_names, group_name, indi_name, date_name, re_phone


class Request:

    def __init__(self, phone, date, partner, amount, price, request_type, prepaid=0):
        self.phone, self.date, self.partner, self.amount, self.price, self.request_type = \
            phone, date, partner, amount, price, request_type
        self.prepaid = prepaid
        self.is_valid = self.check_validity()

    def check_validity(self):
        if self.phone is None or not re.search(re_phone, self.phone):
            return False
        if type(self.date) is not datetime.datetime:
            return False
        if self.partner not in partners_names:
            return False
        if type(self.amount) is not int:
            return False
        if type(self.price) is not int:
            return False
        if self.request_type != group_name and self.request_type != indi_name and self.request_type != date_name:
            return False
        if type(self.prepaid) is not int:
            return False
        return True

    def __repr__(self):
        return str((self.phone, self.date, self.partner, self.amount, self.price, self.request_type))
