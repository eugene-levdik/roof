import dateparser
import phonenumbers
import re
from notion_factory import NotionFactory
from request import Request
from roof_terms import partners_names
from roof_terms import re_ignore, re_phone, re_time
from roof_terms import group_name, indi_name


def find_partner(text):
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
        request_type = group_name if price < 900 else indi_name
    except Exception:
        amount = None
        price = None
        request_type = None
    return amount, price, request_type


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

    amount, price, request_type = parse_numbers_only(text)

    return phone, date, partner, amount, price, request_type


def parse_new_request(text):
    text = text.lower()
    phone_search = re.search(re_phone, text)
    phone = phone_to_text(phonenumbers.parse(phone_search.group(0), 'RU'))
    date = dateparser.parse(text[:phone_search.start()])
    text = text[phone_search.end():]

    partner = find_partner(text)

    amount, price, request_type = parse_numbers_only(text)

    return phone, date, partner, amount, price, request_type


def parse(text, f='new'):
    if f == 'new':
        phone, date, partner, amount, price, request_type = parse_new_request(text)
    elif f == 'old':
        phone, date, partner, amount, price, request_type = parse_old_request(text)
    else:
        raise ValueError('Unknown request format')

    return Request(phone, date, partner, amount, price, request_type)


if __name__ == '__main__':
    factory = NotionFactory()
    # text = input()
    # print(parse(text).__repr__().replace('None', '\033[93mNone\033[0m'))
    f = open('requests1.txt', encoding='UTF-8')
    requests_str = f.read().split('\n\n')
    all_requests = 0
    requests_failed = 0
    for request_str in requests_str:
        request = parse(request_str, f='old')
        print(request.__repr__().replace('None', '\033[93mNone\033[0m'))
    #     try:
    #         factory.push_request(request)
    #     except TypeError:
    #         print('Failed:' + request.__repr__().replace('None', '\033[93mNone\033[0m'))
    #         requests_failed += 1
    #     all_requests += 1
    # print(all_requests, requests_failed)
