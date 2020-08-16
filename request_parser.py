import dateparser
import phonenumbers
import re
from notion_factory import NotionFactory
from request import Request
from roof_terms import partners_names
from roof_terms import re_ignore, re_phone, re_time, re_price


def find_partner(text):
    text = text.lower()
    partner = None
    for short_name in partners_names:
        r = r'(^|\s)' + short_name.lower() + '($|\s)'
        name_search = re.search(r, text)
        if name_search:
            partner = short_name
            break
    if partner is None:
        partner = 'Егор'
    return partner


def parse_numbers_only(text):
    text = re.sub(r'\D', ' ', text).lower()
    try:
        n1, n2 = map(int, text.split())
        if n1 < 50:
            amount = n1
            price = n2
        else:
            price = n1
            amount = n2
    except Exception:
        amount = None
        price = None
    return amount, price


def phone_to_text(phone):
    p = str(phone.national_number)
    return f'+7({p[:3]}){p[3:6]}-{p[6:8]}-{p[8:10]}'


def parse_old_request(text):
    text = text.lower()
    for re_to_ignore in re_ignore:
        text = re.sub(re_to_ignore, ' ', text)

    partner = find_partner(text)
    text = re.sub(partner.lower(), ' ', text)

    try:
        lines = text.split('\n')
        time_line = -1
        for i in range(len(lines)):
            if re.search(re_time, lines[i]):
                time_line = i
                break
        date_to_parse = ' '.join(lines[:time_line + 1])
        text = ' '.join(lines[time_line + 1:])
        date = dateparser.parse(date_to_parse)
    except Exception:
        date = None

    try:
        phone_search = re.search(re_phone, text)
        phone = phone_to_text(phonenumbers.parse(phone_search.group(0), 'RU'))
        text = text[:phone_search.start()] + text[phone_search.end():]
    except Exception:
        phone = None

    amount, price = parse_numbers_only(text)

    return phone, date, partner, amount, price, False


def parse_new_request(text):
    text = text.lower()
    if text.endswith('+'):
        came = True
        text = text[:-1]
    else:
        came = False
        if text.endswith('-'):
            text = text[:-1]
    partner = find_partner(text)
    text = re.sub(partner.lower(), ' ', text)
    phone_search = re.search(re_phone, text)
    price_search = re.search(re_price, text)
    if len(re.findall(re_price, text)) > 1:
        print("\033[91mWarning: multiple pricing!!!\033[0m")
    try:
        phone = phone_to_text(phonenumbers.parse(phone_search.group(0), 'RU'))
        date = dateparser.parse(text[:min(phone_search.start(), price_search.start())])
        amount, price = parse_numbers_only(price_search.group(0))
    except Exception:
        phone = None
        date = None
        amount = None
        price = None
        request_type = None

    return phone, date, partner, amount, price, came


def parse(text):
    if re.search(r'\n[^$]', text):
        phone, date, partner, amount, price, came = parse_old_request(text)
    else:
        phone, date, partner, amount, price, came = parse_new_request(text)

    if phone is None and date is None and amount is None:
        partner = None

    return Request(phone, date, partner, amount, price, came=came)


if __name__ == '__main__':
    factory = NotionFactory()
    f = open('a.txt', encoding='UTF-8')
    requests_str = f.read().split('\n\n')
    all_requests = 0
    requests_failed = 0
    for request_str in requests_str:
        request = parse(request_str)
        all_requests += 1
        # print(request.__repr__().replace('None', '\033[93mNone\033[0m'))
        try:
            factory.push_request(request)
        except TypeError:
            print('Failed:' + request.__repr__().replace('None', '\033[93mNone\033[0m'))
            requests_failed += 1
    print(all_requests, requests_failed)
