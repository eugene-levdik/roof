import re
import datetime
from roof_terms import partners_names, group_name, indi_name, indi_sep, re_phone


class Request:

    def __init__(self, phone, date, partner, amount, price, prepaid=0, came=False):
        self.phone, self.date, self.partner, self.amount, self.price = \
            phone, date, partner, amount, price
        self.prepaid = prepaid
        self.came = came
        if price is None:
            self.request_type = None
        else:
            self.request_type = group_name if price < indi_sep else indi_name
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
        if type(self.prepaid) is not int:
            return False
        return True

    def __repr__(self):
        return str((self.phone, self.date, self.partner, self.amount, self.price, self.request_type, self.prepaid, self.came))
