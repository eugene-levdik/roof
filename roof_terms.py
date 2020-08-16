import re


partners_names = ['ГПК', 'Т', 'Ан', 'Э', 'Пр', 'А', 'В', 'Егор']

re_ignore = [r'\.\.\.', r'=\s*[0-9]*', 'в55']
re_phone = r'(\+7|7|8)[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}'
re_time = r'([0-1][0-9]|[2][0-3]):([0-5][0-9])'
re_price = r'\d+\s?[*xх×]\s?\d+'

group_name = 'Группа'
indi_name = 'Инди'
date_name = 'Свидание'
indi_sep = 900

if __name__ == '__main__':
    text = open('a.txt', encoding='UTF-8').read()
    p = re.findall(re_price, text)
    print(p)
    print(len(p))
