from flask import Flask, render_template, request
from db import db_session, User, Account
import datetime

app = Flask(__name__)

u = User


@app.route("/")
def index():
    # Period

    get_start_data = request.args.get('get_start_data')
    get_end_data = request.args.get('get_end_data')
    if get_start_data == None or get_end_data == None:
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
        #print(account)
        outcome_query_accounts = u.query.filter(u.outcome_account == account.account).filter(u.date >= start_data).filter(u.date <= end_data).all()
        for row in outcome_query_accounts:
            #print(row)
            if row.outcome_currency == 'RUB':
                outcome_account_list.append(row.outcome)
            elif row.outcome_currency == 'USD':
                usd_in_rub = row.outcome * 66.9
                outcome_account_list.append(usd_in_rub)
            elif row.outcome_currency == 'EUR':
                eur_in_rub = row.outcome * 76.73
                outcome_account_list.append(eur_in_rub)

        #print(outcome_account_list)

        income_query_accounts = u.query.filter(u.income_account == account.account).filter(u.date >= start_data).filter(u.date <= end_data).all()
        for row in income_query_accounts:
            #print(row)
            if row.income_currency == 'RUB':
                income_account_list.append(row.income)
            elif row.income_currency == 'USD':
                usd_in_rub = row.income * 66.9
                income_account_list.append(usd_in_rub)
            elif row.income_currency == 'EUR':
                eur_in_rub = row.income * 76.73
                income_account_list.append(eur_in_rub)
        #print(income_account_list)
        value = round(sum(income_account_list) - sum(outcome_account_list), 2)
        percent_value = int(value * 100 / balance)
        value_all += value
        account_value.append([account.account, value, percent_value])
    account_value = sorted(account_value, key=lambda tup: tup[1], reverse=True)
    for acc_val in account_value:
        acc_val[1] = format(acc_val[1], ',.2f')

    #print(account_value)
    #print(value_all)

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
            # print(row)
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
            # print(row)
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
        #percent_value = int(value * 100 / balance)
        #value_all += value
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

    # Date-Time
    #start_data = datetime.datetime.strptime('2016.12.15', '%Y.%m.%d')
    #end_data = datetime.datetime.strptime('2017.12.20', '%Y.%m.%d')
    #mydate = u.query.filter(u.date >= start_data).filter(u.date <= end_data)
    #for row in mydate:
    #    print(row.date)


    return render_template('index.html', all_period_outcome=all_period_outcome, all_period_income=all_period_income,
                           all_period_outcome_percent=all_period_outcome_percent,
                           all_period_income_percent=all_period_income_percent,
                           balance=balance, account_value=account_value, red_category=red_category,
                           green_category=green_category)


@app.route("/income")
def income():
    if request.args.get('account') is not '' and request.args.get('account') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'), request.args.get('category'), request.args.get('comment'),
                        request.args.get('account'), float(request.args.get('outcome')), "RUB", request.args.get('account'),
                        float(request.args.get('income')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('income.html')


@app.route("/outcome")
def outcome():
    if request.args.get('account') is not '' and request.args.get('account') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'), request.args.get('category'), request.args.get('comment'),
                        request.args.get('account'), float(request.args.get('outcome')), "RUB", request.args.get('account'),
                        float(request.args.get('income')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('outcome.html')


@app.route("/remittance")
def remittance():
    if request.args.get('from') is not '' and request.args.get('from') is not None:
        new_transaction = User(datetime.datetime.strptime(request.args.get('date'), '%d.%m.%Y'), request.args.get('category'), request.args.get('comment'),
                        request.args.get('from'), float(request.args.get('remitt')), "RUB", request.args.get('to'),
                        float(request.args.get('remitt')), "RUB")
        db_session.add(new_transaction)
        db_session.commit()
    return render_template('remittance.html')


#@app.route("/<page>")
#def other(page):
#    return render_template(page)


if __name__ == "__main__":
    app.run(debug=True)
