from flask import Flask, request, render_template, Markup
from flask_mobility import Mobility
from request_parser import parse, phone_to_text
import phonenumbers
from roof_terms import partners_names, re_phone
from notion_factory import NotionFactory
import dateparser
from request import Request

app = Flask(__name__, static_url_path='')
Mobility(app)


@app.route('/', methods=['GET', 'POST'])
def upload_request():
    message = ''
    if request.method == 'POST':
        phone = phone_to_text(phonenumbers.parse(request.form.get('phone'), 'RU'))
        date = dateparser.parse(request.form.get('date') + ' ' + request.form.get('time'))
        amount = int(request.form.get('amount'))
        price = int(request.form.get('price'))
        partner = request.form.get('partner')
        prepaid_str = request.form.get('prepaid')
        prepaid = 0 if len(prepaid_str) == 0 else int(prepaid_str)
        r = Request(phone, date, partner, amount, price, prepaid=prepaid)
        try:
            factory = NotionFactory()
            factory.push_request(r)
            message = Markup('<span style="color: green">Успешно</span>')
        except Exception:
            message = Markup('<span style="color: red">Ошибка</span>')

    request_to_parse = request.args.get('text')
    if request_to_parse is None:
        request_to_parse = ''

    r = parse(request_to_parse)
    phone = '' if r.phone is None else r.phone
    if r.date is None:
        date_str = ''
        time_str = ''
    else:
        s = r.date.isoformat()
        date_str = s[:10]
        time_str = s[11:-3]
    amount = '' if r.amount is None else r.amount
    price = '' if r.price is None else r.price
    partner = '' if r.partner is None else r.partner

    partners_html = ['<option value="" hidden disabled selected>Партнёр</option>']
    for short_name in partners_names:
        partners_html.append(f'<option{" selected" if partner == short_name else ""}>')
        partners_html.append(short_name)
        partners_html.append('</option>')
    partners_html = Markup(''.join(partners_html))
    if request.MOBILE:
        return render_template('mobile_request_form.html', request_to_parse=request_to_parse, phone=phone,
                               date=date_str, time=time_str, amount=amount, price=price, partners_html=partners_html,
                               re_phone=re_phone, message=message)
    return render_template('request_form.html', request_to_parse=request_to_parse, phone=phone, date=date_str,
                           time=time_str, amount=amount, price=price, partners_html=partners_html, re_phone=re_phone,
                           message=message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
