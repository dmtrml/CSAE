from flask import Flask, render_template, request
from db import db_session, User, Account, Category, Subcategory
import datetime
import time

import requests
from requests.auth import HTTPBasicAuth

import re

app = Flask(__name__)

u = User


@app.route("/")
def index():
    # Period

    get_start_data = request.args.get('get_start_data')
    get_end_data = request.args.get('get_end_data')
    if get_start_data is None or get_end_data is None:
        get_start_data = '16.03.2016'
        get_end_data = datetime.datetime.now().strftime('%d.%m.%Y')
    print(get_start_data, type(get_start_data))
    start_data = datetime.datetime.strptime(get_start_data, '%d.%m.%Y')
    end_data = datetime.datetime.strptime(get_end_data, '%d.%m.%Y')

    # Income-Outcome
    outcome_operations = []
    outcome_query = u.query.filter(u.outcome != 0).filter(u.date >= start_data).filter(u.date <= end_data).all()
    for row in outcome_query:
        if row.category != '':
            outcome_operations.append(row.outcome)
    all_period_outcome = round(sum(outcome_operations), 2)

    income_operations = []
    income_query = u.query.filter(u.income != 0).filter(u.date >= start_data).filter(u.date <= end_data).all()
    for row in income_query:
        if row.category != '':
            income_operations.append(row.income)
    all_period_income = round(sum(income_operations), 2)

    if all_period_outcome > all_period_income:
        all_period_outcome_percent = 100
        all_period_income_percent = int(all_period_income * 100 / all_period_outcome)
    else:
        all_period_income_percent = 100
        all_period_outcome_percent = int(all_period_outcome * 100 / all_period_income)

    # Balance
    balance = round(all_period_income - all_period_outcome, 2)

    # Account balance
    list_of_accounts = Account.query.all()
    account_value = []
    value_all = 0
    for account in list_of_accounts:
        income_account_list = []
        outcome_account_list = []
        outcome_query_accounts = u.query.filter(u.outcome_account == account.account).filter(u.date >= start_data).filter(u.date <= end_data).all()
        for row in outcome_query_accounts:
            if row.outcome_currency == 'RUB':
                outcome_account_list.append(row.outcome)
            elif row.outcome_currency == 'USD':
                usd_in_rub = row.outcome * 66.9
                outcome_account_list.append(usd_in_rub)
            elif row.outcome_currency == 'EUR':
                eur_in_rub = row.outcome * 76.73
                outcome_account_list.append(eur_in_rub)

        income_query_accounts = u.query.filter(u.income_account == account.account).filter(u.date >= start_data).filter(u.date <= end_data).all()
        for row in income_query_accounts:
            if row.income_currency == 'RUB':
                income_account_list.append(row.income)
            elif row.income_currency == 'USD':
                usd_in_rub = row.income * 66.9
                income_account_list.append(usd_in_rub)
            elif row.income_currency == 'EUR':
                eur_in_rub = row.income * 76.73
                income_account_list.append(eur_in_rub)
        value = round(sum(income_account_list) - sum(outcome_account_list), 2)
        percent_value = int(value * 100 / balance)
        value_all += value
        account_value.append([account.account, value, percent_value])
    account_value = sorted(account_value, key=lambda tup: tup[1], reverse=True)
    for acc_val in account_value:
        acc_val[1] = format(acc_val[1], ',.2f')

    # List of category
    set_of_category = set()
    all_data = u.query.filter(u.date >= start_data).filter(u.date <= end_data).all()
    for row in all_data:
        if row.category != '':
            set_of_category.add(row.category)
    print(set_of_category)

    # category value
    green_category = []
    red_category = []
    for category in set_of_category:
        income_category_list = []
        outcome_category_list = []
        query_category = u.query.filter(u.category == category).filter(u.date >= start_data).filter(u.date <= end_data).all()
        for row in query_category:
            if row.outcome_currency == 'RUB':
                outcome_category_list.append(row.outcome)
            elif row.outcome_currency == 'USD':
                usd_in_rub = row.outcome * 66.9
                outcome_category_list.append(usd_in_rub)
            elif row.outcome_currency == 'EUR':
                eur_in_rub = row.outcome * 76.73
                outcome_category_list.append(eur_in_rub)

        print(outcome_category_list)

        for row in query_category:
            if row.income_currency == 'RUB':
                income_category_list.append(row.income)
            elif row.income_currency == 'USD':
                usd_in_rub = row.income * 66.9
                income_category_list.append(usd_in_rub)
            elif row.income_currency == 'EUR':
                eur_in_rub = row.income * 76.73
                income_category_list.append(eur_in_rub)
        print(income_category_list)
        value = round(sum(income_category_list) - sum(outcome_category_list), 2)
        if value > 0:
            green_category.append([category, value])
        elif value < 0:
            red_category.append([category, value])
    red_category = sorted(red_category, key=lambda tup: tup[1])
    green_category = sorted(green_category, key=lambda tup: tup[1], reverse=True)
    for cat_val in red_category:
        cat_val[1] = format(cat_val[1], ',.2f')
    for cat_val in green_category:
        cat_val[1] = format(cat_val[1], ',.2f')

    return render_template('index.html', all_period_outcome=all_period_outcome, all_period_income=all_period_income,
                           all_period_outcome_percent=all_period_outcome_percent,
                           all_period_income_percent=all_period_income_percent,
                           balance=balance, account_value=account_value, red_category=red_category,
                           green_category=green_category)


@app.route("/income")
def income():
    list_of_accounts = Account.query.all()
    if request.args.get('account') is not '' and request.args.get('account') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'),
                               request.args.get('category'), request.args.get('comment'),
                               request.args.get('account'), float(request.args.get('outcome')), "RUB",
                               request.args.get('account'), float(request.args.get('income')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('income.html', list_of_accounts=list_of_accounts)


@app.route("/outcome")
def outcome():
    list_of_accounts = Account.query.all()
    if request.args.get('account') is not '' and request.args.get('account') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'),
                               request.args.get('category'), request.args.get('comment'),
                               request.args.get('account'), float(request.args.get('outcome')), "RUB",
                               request.args.get('account'), float(request.args.get('income')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('outcome.html', list_of_accounts=list_of_accounts)


@app.route("/remittance")
def remittance():
    list_of_accounts = Account.query.all()
    if request.args.get('from') is not '' and request.args.get('from') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'),
                               request.args.get('category'), request.args.get('comment'),
                               request.args.get('from'), float(request.args.get('remitt')), "RUB",
                               request.args.get('to'), float(request.args.get('remitt')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('remittance.html', list_of_accounts=list_of_accounts)


@app.route("/fns", methods=['GET', 'POST'])
def fns():
    items = list()
    list_of_accounts = Account.query.all()
    list_of_category = Category.query.all()
    list_of_subcategory = Subcategory.query.all()
    print(request.form)

    if request.form.get('outcome') != 0 and request.form.get('outcome') is not None:
        print(request.form)
        list_of_item_id = request.form.getlist('item_id')
        print(list_of_item_id)
        list_of_comments = request.form.getlist('comment')
        list_of_outcomes = request.form.getlist('outcome')
        for item_id in list_of_item_id:
            new_transaction = User(datetime.datetime.strptime(request.form.get('date'), '%d.%m.%Y'),
                                   request.form.get('category'), list_of_comments[int(item_id)],
                                   request.form.get('account'), float(list_of_outcomes[int(item_id)]), "RUB",
                                   request.form.get('account'),
                                   float(request.form.get('income')), "RUB")
            db_session.add(new_transaction)
        db_session.commit()

    # list of items after selecting a part of them
        index_comment = 0
        item_id = 0
        for comment in list_of_comments:
            if str(index_comment) not in list_of_item_id:
                items.append({'name': comment, 'sum': float(list_of_outcomes[index_comment])*100, 'item_id': item_id})
                item_id += 1
            index_comment += 1
    # request to the FNS
    try:
        decoded_qr = request.form.get('qrdata')
        print(decoded_qr)
        fn = re.search(r'&fn=(\d+)', decoded_qr)[0][4:]
        i = re.search(r'&i=(\d+)', decoded_qr)[0][3:]
        fp = re.search(r'&fp=(\d+)', decoded_qr)[0][4:]
        t = re.search(r't=(\d+.\d+)', decoded_qr)[0][2:]
        s = re.search(r'&s=(\d+...)', decoded_qr)[0][3:]
        n = re.search(r'&n=(\d+)', decoded_qr)[0][3:]
        s = re.sub('\.', '', s)
        print(fn, i, fp, t, s, n)

        headers = {
            'Device-Id': 'noneOrRealId',
            'Device-OS': 'Adnroid 5.1',
            'Version': '2',
            'ClientVersion': '1.4.4.1',
            'Host': 'proverkacheka.nalog.ru:9999',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.0.1'

        }
        #chek_fns = requests.get(
        #    'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/{}/operations/{}/tickets/{}?fiscalSign={}&date={}&sum={}'
        #        .format(fn, n, i, fp, t, s), headers=headers)
        #print(chek_fns.status_code, chek_fns.headers, chek_fns, chek_fns.text)
        #time.sleep(1)
        chek_fns = requests.get(
            'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/{}/operations/{}/tickets/{}?fiscalSign={}&date={}&sum={}'
                .format(fn, n, i, fp, t, s), headers=headers)
        print(chek_fns.status_code, chek_fns.headers, chek_fns, chek_fns.text)
        time.sleep(0.5)
        for m in range(0, 30):
            fns_data = requests.get(
                'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/{}/tickets/{}?fiscalSign={}&sendToEmail=no'
                    .format(fn, i, fp), auth=HTTPBasicAuth('+79776494088', '181218'), headers=headers)
            print(fns_data.text, fns_data.status_code)
            if fns_data.status_code == 200:
                print(fns_data.text, fns_data.status_code, fns_data.json())
                fns_json = fns_data.json()
                items = fns_json['document']['receipt']['items']

                item_id = 0
                for item in items:
                    item['item_id'] = item_id
                    item_id += 1
                break
            time.sleep(0.5)
    except Exception as e:
        print(e)

    return render_template('fns.html', list_of_accounts=list_of_accounts, items=items,
                           list_of_category=list_of_category, list_of_subcategory=list_of_subcategory)


if __name__ == "__main__":
    app.run(debug=True)
