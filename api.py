import monobank
from datetime import datetime, date, timezone
import time

token = 'token'
mono = monobank.Client(token)

def get_cards():
    try:
        user_info = mono.get_client_info()
        card_ids = [] 
        if user_info:
            for user in user_info['accounts']:
                originBalance = user['balance'] // 100
                temp = user['maskedPan'][0]
                if temp[0] == '4':
                    print('VISA ''Назва карти ', user['type'], 'Номер карти ', user['maskedPan'], 'Баланс по карті', originBalance)
                elif temp[0] == '5':
                    print('Master ''Назва карти ', user['type'], 'Номер карти ', user['maskedPan'], 'Баланс по карті', originBalance)
                
                card_ids.append(user['id']) 
        return card_ids
    except Exception as e:
        print("Помилка у функції get_cards:", e)
        return []

def get_pay(ttt):
    originAmounts = [] 
    try:
        for tt in ttt: 
            client = mono.get_statements(tt, date(2024, 2, 23), date(2024, 2, 23))
            for payment in client:
                timeOrigin = datetime.fromtimestamp(payment['time'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                print('Час', timeOrigin)
                originAmount = payment['amount'] // 100
                print('Сума', originAmount)
                originAmounts.append(originAmount) 
                currency = ''
                if payment['currencyCode'] == 980:
                    currency = 'UAH'
                print('Категорія', payment['description'])
                print('Валюта', currency)
                print('--------------------------------------')
                print( payment['description'], currency, originAmount, timeOrigin) 
    except Exception as e:
        print("Помилка у функції get_pay:", e)
    return originAmounts 

#def get_only_category(user_ids)

def get_category_earn_cost(originAmounts):
    try:
        for originAmount in originAmounts:
            if str(originAmount).startswith('-'):
                print("Витрата")
            else:
                print("Поповнення")
    except Exception as e:
        print("Помилка у функції get_category_earn_cost:", e)

try:
    card_ids = get_cards()
    if card_ids:
        time.sleep(61)
        originAmounts = get_pay(card_ids) 
        time.sleep(100)
        #get_category_earn_cost(originAmounts)  
except Exception as e:
    print("Помилка у головній програмі:", e)
