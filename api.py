import monobank
from datetime import datetime, date, timezone
import time

token = 'uhcETfSFbEeE7qpGAfEJNLsYv6xTlK61nnlP8IHyIIrk'
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

def get_pay(user_ids):
    try:
        for user_id in user_ids: 
            client = mono.get_statements(user_id, date(2024, 2, 23), date(2024, 2, 23))
            for payment in client:
                timeOrigin = datetime.fromtimestamp(payment['time'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                print('Час', timeOrigin)
                originAmount = payment['amount'] // 100
                print('Сума', originAmount)
                originAmounts.append(client['originAmount']) 
                print('Категорія', payment['description'])
                print('Валюта', payment['currencyCode'])
                print('--------------------------------------')
        return originAmounts
    except Exception as e:
        print("Помилка у функції get_pay:", e)

def get_category_earn_cost(originAmounts):
    try:
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
        get_pay(card_ids)
        time.sleep(100)
        get_category_earn_cost(originAmounts)
except Exception as e:
    print("Помилка у головній програмі:", e)