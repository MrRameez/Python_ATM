import streamlit as st
import random

# -------------------------------
# Session State Initialization
# -------------------------------
if "all_accounts" not in st.session_state:
    st.session_state.all_accounts = []

# -------------------------------
# BankAccount Class (OOP)
# -------------------------------
class BankAccount:
    def __init__(self, name, initial_deposit):
        self.name = name
        self.balance = initial_deposit
        self.account_number = random.randint(1000, 9999)
        self.pin = random.randint(1000, 9999)

    # Deposit Method
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # Withdraw Method
    def withdraw(self, amount, pin):
        if pin != self.pin:
            return None, "Invalid PIN"
        if amount > self.balance:
            return None, "Insufficient Balance"
        self.balance -= amount
        return self.balance, None

    # Check Balance Method
    def check_balance(self, pin):
        if pin != self.pin:
            return None, "Invalid PIN"
        return self.balance, None

    # Transfer Method
    def transfer(self, amount, pin, beneficiary_account):
        if pin != self.pin:
            return None, "Invalid PIN"
        if amount > self.balance:
            return None, "Insufficient Balance"
        self.balance -= amount
        beneficiary_account.balance += amount
        return self.balance, None

# -------------------------------
# Backend Functions
# -------------------------------

def create_account(name, initial_deposit):
    acc = BankAccount(name, initial_deposit)
    st.session_state.all_accounts.append(acc)
    return acc

def find_account(account_number):
    for acc in st.session_state.all_accounts:
        if acc.account_number == account_number:
            return acc
    return None

def delete_account(account_number, pin):
    acc = find_account(account_number)
    if acc:
        if acc.pin != pin:
            return "Invalid PIN"
        st.session_state.all_accounts.remove(acc)
        return "Account Deleted Successfully"
    return "Account Not Found"

# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🏦 Simple Banking System (OOP)")
st.write("This is a beginner-friendly banking system using **Classes & Objects**")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Open Account", "Check Balance", "Deposit", "Withdraw", "Transfer", "Delete Account", "Show All Accounts"]
)

# -------------------------------
# Open Account
# -------------------------------
if menu == "Open Account":
    st.header("➕ Open a New Account")
    name = st.text_input("Enter Your Name")
    initial_deposit = st.number_input("Initial Deposit", min_value=0)
    if st.button("Create Account"):
        acc = create_account(name, initial_deposit)
        st.success("🎉 Account Created Successfully")
        st.write(f"**Account Number:** `{acc.account_number}`")
        st.write(f"**PIN:** `{acc.pin}` (Save this safely!)")

# -------------------------------
# Check Balance
# -------------------------------
elif menu == "Check Balance":
    st.header("💰 Check Balance")
    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    if st.button("Show Balance"):
        acc = find_account(acc_no)
        if acc:
            bal, err = acc.check_balance(pin)
            if err:
                st.error(err)
            else:
                st.success(f"Current Balance: Rs {bal}")
        else:
            st.error("Account Not Found")

# -------------------------------
# Deposit
# -------------------------------
elif menu == "Deposit":
    st.header("📥 Deposit Amount")
    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)
    if st.button("Deposit"):
        acc = find_account(acc_no)
        if acc:
            bal = acc.deposit(amt)
            st.success(f"Amount Deposited! New Balance: Rs {bal}")
        else:
            st.error("Account Not Found")

# -------------------------------
# Withdraw
# -------------------------------
elif menu == "Withdraw":
    st.header("📤 Withdraw Amount")
    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)
    if st.button("Withdraw"):
        acc = find_account(acc_no)
        if acc:
            bal, err = acc.withdraw(amt, pin)
            if err:
                st.error(err)
            else:
                st.success(f"Withdrawal Successful! New Balance: Rs {bal}")
        else:
            st.error("Account Not Found")

# -------------------------------
# Transfer
# -------------------------------
elif menu == "Transfer":
    st.header("💸 Transfer Amount")
    acc_no = st.number_input("Your Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("Your PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)
    ben_no = st.number_input("Beneficiary Account Number", min_value=1000, max_value=9999)
    if st.button("Transfer"):
        acc = find_account(acc_no)
        ben_acc = find_account(ben_no)
        if acc and ben_acc:
            bal, err = acc.transfer(amt, pin, ben_acc)
            if err:
                st.error(err)
            else:
                st.success(f"Transfer Successful! Remaining Balance: Rs {bal}")
        else:
            st.error("Account or Beneficiary Not Found")

# -------------------------------
# Delete Account
# -------------------------------
elif menu == "Delete Account":
    st.header("❌ Delete Account")
    acc_no = st.number_input("Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("PIN", min_value=1000, max_value=9999)
    if st.button("Delete Account"):
        msg = delete_account(acc_no, pin)
        if "Successfully" in msg:
            st.success(msg)
        else:
            st.error(msg)

# -------------------------------
# Show All Accounts (Debug)
# -------------------------------
elif menu == "Show All Accounts":
    st.header("📋 All Accounts (Debug View)")
    for acc in st.session_state.all_accounts:
        st.write(f"Name: {acc.name}, Acc No: {acc.account_number}, Balance: {acc.balance}, PIN: {acc.pin}")
