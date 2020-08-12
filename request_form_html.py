from roof_terms import re_phone, group_name, indi_name


def html_str(request_to_parse, phone, date, time, amount, price, partners_html, request_type):
    return f'''<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Экскурсии по крышам</title>
    </head>
    <body>
    <div class="lBox">
        <form action="/" method="get" name="parser">
            <p>
                <textarea name="text" placeholder="Текст заявки" rows="5" cols="30">{'' if request_to_parse is None else request_to_parse}</textarea></p>
            <p><input type="submit" value="Распознать заявку"></p>
        </form>
    </div>
    <div class="rBox">
        <form action="/" method="post" name="request">
            <p>
                Тел.: 
                <input type="tel" name="phone"
                       pattern={re_phone}
                       title="Российский номер телефона" 
                       value="{'' if phone is None else phone}"
                       required>
            </p>
            <p>
                <input type="date" name="date" value="{'' if date is None else date}" required>
                <input type="time" name="time" value="{'' if time is None else time}" required>
            </p>
            <p>
                <input type="number" name="amount" style="width: 5em" value="{'' if amount is None else amount}" required>
                x
                <input type="number" name="price" style="width: 5em" value="{'' if price is None else price}" required>
                &#8381
            </p>
            <p>
                Партнёр: 
                <select name="partner" required>
                    {partners_html}
                </select>
            </p>
            <p>Предоплата: <input type="number" name="prepaid">&#8381</p>
            <p>
                <input type="radio" name="request_type" id="type1" value="Группа" {'checked' if request_type == group_name else ''}>
                <label for="type1">Группа</label>
                <input type="radio" name="request_type" id="type2" value="Инди" {'checked' if request_type == indi_name else ''}>
                <label for="type2">Инди</label>
            </p>
            <p><input type="submit" value="Отправить"></p>
        </form>
    </div>
    </body>
    </html>
    '''
