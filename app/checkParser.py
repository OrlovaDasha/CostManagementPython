import re

import datetime


def common_parse(text):
    text[0] = " ".join(text[0].split())

    index = 0

    regexps = ['^ф[нh]:.*', '^фд:.*', 'фпд:.*', '^[нh]д[сc] .*', '.* [нh][aа]л[оo]г[оo][оo]бл[oо]же[hн]ия: .*',
               '.* [kк][kк][tт]:.*', '^з[аa]в[оo]д.*',
               '^и[нh][нh].*', '^[кk][аa][сc][сc]и[рp] .*', '^ч[eе][кk] .*', '^[сc]м[еe][hн][aа] .*',
               '^п[рp]и[xх][оo]д']

    for row in text:
        for regexp in regexps:
            regex = re.compile(regexp)
            if regex.match(row.lower()):
                text[index] = ""
        index = index + 1

    text = list(filter(None, text))

    shop_name = re.compile(
        '^(?:(?:[oо0][oо0][oо0])|(?:[оo]бщ[еe][сc][тt][вb][оo] [сc] [oо]г[рp][аa][нh]ич[еe]нн[оo]й [оo][тt]в[еe]'
        '[тt][сc][тt][вb][еe][нh][hн][oо][cс][tт]ью))\s?.*?(\w+\s?\w*).*?$')
    data_regex = re.compile('^^([0-9]{2})[,‚..]?\s?([0-9]{2})[,‚..]?\s?([0-9]{4}).*$')
    all_sum_regex = re.compile('([0-9]{0,3},?[0-9]{0,3}\.[0-9]{2})$')
    all_regex = re.compile('^(?:и[тt][оo]г[оo])|(?:.*[kк][аa][рp][тt][аa])|(?:[нh][aа][лп]ич[hн]ы[eе])')
    item_regex = re.compile('^[0-9]*(.*?)\s*([0-9]{0,3},?[0-9]{1,3}\.[0-9]{2})\s*([0-9]*?\.[0-9]{1,2})\s*'
                            '([0-9]{0,3},?[0-9]{0,3}\.[0-9]{2})$')
    regexp = {1: 'и[тt][оo]г[оo]', 2: '[kк][аa][рp][тt][аa]', 3: '[нh][aа][лп]ич[hн]ы[eе]'}

    address = None
    data = None
    buy_date = None
    all_sum = None
    items = []
    prev = ''
    shop = None
    card_sum = None
    money_sum = None
    payment_type = 'cash'

    print(text[2])
    for row in text:

        if shop_name.match(row.lower()):
            data = shop_name.findall(row.lower())[0]
            shop = data.title()

        if data_regex.match(row):
            data = data_regex.findall(row)
            buy_date = datetime.datetime.strptime("{}{}{}".format(data[0][0], data[0][1], data[0][2]), "%d%m%Y").date()

        if all_regex.match(row.lower()):
            data = all_sum_regex.findall(row.lower())[0]
            for key, regex in regexp.items():
                r = re.compile(regex)
                if r.match(row.lower()):
                    if key == 1:
                        all_sum = data
                        all_sum = all_sum.replace(',','')
                    if key == 2:
                        card_sum = data
                        card_sum = card_sum.replace(',', '')
                    if key == 3:
                        money_sum = data
                        money_sum = money_sum.replace(',', '')
            if card_sum is not None and float(card_sum) > 0:
                payment_type = 'card'

        if item_regex.match(prev):
            data = item_regex.findall(prev)[0]
            item_name = data[0]
            item_price = data[1]
            item_price = item_price.replace(',', '')
            item_number = data[2]
            item_cost = data[3]
            item_cost = item_cost.replace(',', '')

            if not (all_regex.match(row.lower())) and not (item_regex.match(row)):
                item_name = item_name + ' ' + row

            item = {'name': item_name, 'price': item_price, 'number': item_number, 'cost': item_cost}
            items.append(item)

        prev = row

    if all_sum is None:
        if card_sum is not None and float(card_sum) > 0:
            all_sum = card_sum
        elif money_sum is not None and float(money_sum) > 0:
            all_sum = money_sum

    return text, shop, address, buy_date, all_sum, items, payment_type
