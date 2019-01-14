from flask import Flask, render_template
from db import db_session, User, Account
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    # Income-Outcome
    outcome_operations = []
    outcome_query = User.query.filter(User.outcome != 0).all()
    for row in outcome_query:
        if row.category != '':
            outcome_operations.append(row.outcome)
    all_period_outcome = round(sum(outcome_operations), 2)

    income_operations = []
    income_query = User.query.filter(User.income != 0).all()
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
        outcome_query_accounts = User.query.filter(User.outcome_account == account.account).all()
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

        income_query_accounts = User.query.filter(User.income_account == account.account).all()
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
    all_data = User.query.all()
    for row in all_data:
        set_of_category.add(row.category)
    print(set_of_category)

    # category value
    category_value = []
    for category in set_of_category:
        income_category_list = []
        outcome_category_list = []
        query_category = User.query.filter(User.category == category).all()
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
        category_value.append([category, value])
    category_value = sorted(category_value, key=lambda tup: tup[1])
    for cat_val in category_value:
        cat_val[1] = format(cat_val[1], ',.2f')
    print(category_value)





    """
    set_of_account = set()
    all_data = User.query.all()
    for transaction in all_data:
        set_of_account.add(transaction.outcome_account)
        set_of_account.add(transaction.income_account)
    print(set_of_account)
    
    list_of_salary = []
    month_salary = 0
    list_of_months = []
    salary_category = User.query.filter(User.category=='Зарплата').all()

    for salary in salary_category:
        row_date = salary.date.strftime('%m.%Y')

        if row_date not in list_of_months:
            list_of_months.append(row_date)
            if month_salary != 0:
                list_of_salary.append(month_salary)
            month_salary = salary.amount
        else:
            month_salary += salary.amount
    else:
        list_of_salary.append(month_salary)
    print(list_of_months)
    print(list_of_salary)

    for month in list_of_months:
        User.query.filter(User.category == 'Зарплата', ).all()

#    for item in salary_category:
#       list_of_salary.append(item.amount)
#   print(list_of_salary)
        #.db_session.query(u.amount).all()
    #all_objects = [value for value, in list_of_cost]
    numbers = list_of_months
    """
    return render_template('index.html', all_period_outcome=all_period_outcome, all_period_income=all_period_income,
                           all_period_outcome_percent=all_period_outcome_percent,
                           all_period_income_percent=all_period_income_percent,
                           balance=balance, account_value=account_value, category_value=category_value)


@app.route("/<path>")
def other(path):
    return render_template(path)


if __name__ == "__main__":
    app.run(debug=True)
