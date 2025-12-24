import streamlit as st
import random



# Backend logic

all_account = []

def open_account(cnic,account_title, initial_deposite):
    account = {
        'cnic': cnic,
        'title': account_title,
        'balance': initial_deposite,
        'pin': random.randint(1000,9999),
        'account_number':random.randint(1000,9999)
    }
    all_account.append(account)
    return account

def show_balance(account_number,pin):
    for acc in all_account:
        if acc['account_number'] == account_number:
            if acc['pin'] == pin:
                return acc['balance'], None
            else:
                return None, "Invalid Pin"
    return None,"Account Not found"

def deposit_amount(account_number, amount):
    for acc in all_account:
        if acc['account_number'] == account_number:
             acc['balance'] += amount
             return acc['balance'],None
    return None,"Account Not found"

def withdraw_amt(account_number,pin,amount):
    for acc in all_account:
        if acc['account_number'] == account_number:
            
            if acc['pin'] != pin:
                return None, 'Invalid pin'
            if amount > acc['balance']:
                return None, "Insufficient Balance"
            
            acc['balance'] -= amount
            return acc['balance'],None
        
    return None, 'Account Not found'


def transfer_amt(account_number,pin, amount, beneficiary_acc):
    for acc in all_account:
        if acc['account_number'] == account_number:
            if acc['pin'] != pin:
                return None, 'Invalid Pin'
            if acc['balance'] < amount:
                return None, 'Insufficiant Balance'
            
            for bacc in all_account:
                if bacc['account_number'] == beneficiary_acc:
                    acc['balance']-= amount
                    bacc['balance']+= amount
                    return bacc['balance'],None
            return None,"beneficiary_account is not found"
    return None,'Account Not found '               
                    