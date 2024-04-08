import monobank
from datetime import datetime, date, timezone
import time
import iso18245
import pandas as pd

token = 'token'
mono = monobank.Client(token)

def get_mcc_description(mcc):
    try:
        merchant_category = iso18245.get_mcc(mcc).usda_description
    except:
        merchant_category = None
    return merchant_category

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except Exception as e:
        print("Помилка у функції read_csv:", e)
        return None


def get_cards():
    try:
        user_info = mono.get_client_info()
        card_ids = [] 
        if user_info:
            for user in user_info['accounts']:
                originBalance = user['balance'] // 100
                temp = user['maskedPan'][0]
                if temp[0] == '4':
                    print('VISA ''Назва карти ', user['type'], 'Номер карти ', user['maskedPan'], 'Баланс по карті', originBalance, 'id', user['id'])
                elif temp[0] == '5':
                    print('Master ''Назва карти ', user['type'], 'Номер карти ', user['maskedPan'], 'Баланс по карті', originBalance,'id', user['id'])
                
                card_ids.append(user['id']) 
        return card_ids
    except Exception as e:
        print("Помилка у функції get_cards:", e)
        return []

def get_pay(user_ids, df):
    originAmounts = [] 
    try:
        for user_id in user_ids: 
            client = mono.get_statements(user_id, date(2024, 2, 1), date(2024, 3, 1))
            for payment in client:
                timeOrigin = datetime.fromtimestamp(payment['time'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                print('Час', timeOrigin)
                originAmount = payment['amount'] // 100
                print('Сума', originAmount)
                originAmounts.append(originAmount) 
                currency = ''
                if payment['currencyCode'] == 980:
                    currency = 'UAH'
                mcc_description = get_mcc_description(str(payment.get('mcc', '')))
                category = find_category(df, mcc_description)
                print('Категорія', category)
                print('Валюта', currency)
                print('--------------------------------------')
    except Exception as e:
        print("Помилка у функції get_pay:", e)
    return originAmounts 

def find_category(df, mcc_description):
    if df is not None:
        mask = df['Description'] == mcc_description
        if mask.any():
            return df[mask]['Category'].values[0]
    return mcc_description



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
    file_path = 'category.csv'  # Шлях до файлу CSV
    df = read_csv(file_path)
    if df is not None:
        card_ids = get_cards()
        if card_ids:
            time.sleep(61)
            pp = ''
            originAmounts = get_pay(pp, df) 
            time.sleep(100)
            #get_category_earn_cost(originAmounts)  
except Exception as e:
    print("Помилка у головній програмі:", e)
