#은행 시스템 기능부

#req! : pip install pickle
#       pip install pandas
#run with cmd!! 없으면 오류나요

import main as front
import pickle
import pandas as pd
import random

class TransactionLog:
    def __init__(self):
        try:
            with open('transaction_log.pkl', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['송금자', '수취인', '이체액'])
            self.save_data()

    def save_data(self):
        with open('transaction_log.pkl', 'wb') as f:
            pickle.dump(self.data, f)

    def log_transaction(self, sender, receiver, amount):
        new_row = {'송금자': sender, '수취인': receiver, '이체액': amount}
        self.data.loc[len(self.data)] = new_row
        self.save_data()

    def view_database(self):
        print(self.data)

class Bank:
    def __init__(self):
        self.transaction_log = TransactionLog()

        try:
            with open('db.pkl', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['이름', '계좌번호', '비밀번호', '잔고', '고객구분', '법인대표', '담당직원'])
            self.save_data()

    def save_data(self):
        with open('db.pkl', 'wb') as f:
            pickle.dump(self.data, f)

    def create_account(self, name, password, initial_balance, customer_type, name_ceo, name_charge):
        account_number = self.generate_account_number()
        account = self.data[(self.data['이름'] == name)]

        try:
            if account['이름'].iloc[0] == name:
                print("이미 개설된 고객입니다.")
                return None
        except:
            new_row = {'이름': name, '계좌번호': account_number, '비밀번호': password, '잔고': initial_balance, '고객구분': customer_type, '법인대표': name_ceo, '담당직원': name_charge}
            self.data.loc[len(self.data)] = new_row
            self.save_data()
            print(f"{name}님의 계좌가 생성되었습니다. 계좌번호는 {account_number} 입니다.")

    def find_account(self, name, password, name_ceo=None, name_charge=None):
        if name_ceo and name_charge:
            account = self.data[(self.data['이름'] == name) & (self.data['비밀번호'] == password) & (self.data['법인대표'] == name_ceo) & (self.data['담당직원'] == name_charge)]
        else:
            account = self.data[(self.data['이름'] == name) & (self.data['비밀번호'] == password)]
        
        if account.empty:
            return None
        return account

    def view_account(self, name, password, name_ceo=None, name_charge=None):
        account = self.find_account(name, password, name_ceo, name_charge)
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return
        balance = account['잔고'].iloc[0]
        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def deposit(self, name, password, amount, name_ceo=None, name_charge=None):
        account = self.find_account(name, password, name_ceo, name_charge)
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return
        self.data.loc[account.index, '잔고'] += amount
        self.save_data()
        print(f"{account['계좌번호'].iloc[0]} 계좌에 {int(amount)}원을 입금하였습니다.")

    def withdraw(self, name, password, amount, name_ceo=None, name_charge=None):
        account = self.find_account(name, password, name_ceo, name_charge)
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return
        if account['잔고'].iloc[0] < amount:
            print("잔액이 부족합니다.")
            return
        self.data.loc[account.index, '잔고'] -= amount
        self.save_data()
        print(f"{account['계좌번호'].iloc[0]} 계좌에서 {int(amount)}원을 출금하였습니다.")

    def transfer(self, name, password, destination_name, amount, name_ceo=None, name_charge=None):
        account = self.find_account(name, password, name_ceo, name_charge)
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return

        destination_account = self.data[self.data['이름'] == destination_name]
        if destination_account.empty:
            print("해당 수취인 계좌가 존재하지 않습니다.")
            return

        if account['잔고'].iloc[0] < amount + 1000:
            print("잔액이 부족합니다.")
            return

        print("*이체 수수료 1000원이 발생합니다. \n수수료는 계좌에서 자동 출금 됩니다.")
        self.data.loc[account.index, '잔고'] -= (amount + 1000)
        self.data.loc[destination_account.index, '잔고'] += amount
        self.save_data()
        print(f"{destination_account['계좌번호'].iloc[0]} ( {destination_name} 님 ) 계좌에 {int(amount)}원을 입금하였습니다.")
        balance = account['잔고'].iloc[0] - (amount + 1000)
        self.transaction_log.log_transaction(name, destination_name, amount)
        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def close_account(self, name, password, name_ceo=None, name_charge=None):
        account = self.find_account(name, password, name_ceo, name_charge)
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            return
        self.data = self.data[self.data['계좌번호'] != account['계좌번호'].iloc[0]]
        self.save_data()
        print(f"{account['계좌번호'].iloc[0]} 계좌가 해지되었습니다.")

    def generate_account_number(self):
        return '772-' + ''.join([str(random.randint(1000, 9999))]) + '-0114'

    def view_database(self):
        print(self.data)


#######################################################################################################

def login(optional):
    bank = Bank()
    trans = TransactionLog()

    if(optional == "개설"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        initial_balance = int(input("최초 입금 금액을 입력하세요: "))
        if initial_balance < 0:
            print("입력 오류")
            return
        
        if initial_balance < 10000:
            print("최초 입금 금액의 최소액은 1만원 입니다.")
            return
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '개인':
            isStudent = input("학생 고객에 해당하십니까? (Y/N): ")
            if isStudent == 'Y':
                print("환영합니다. 학생 고객 혜택으로 1만원이 지급 되었습니다.")
                initial_balance = initial_balance + 10000
                bank.create_account(name, password, initial_balance, customer_type, None, None)
            elif isStudent == 'N':
                bank.create_account(name, password, initial_balance, customer_type, None, None)
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            print("환영합니다. 법인 고객 혜택으로 십 만원이 지급 되었습니다.")
            initial_balance = initial_balance + 100000
            bank.create_account(name, password, initial_balance, customer_type, name_ceo, name_charge)

    elif(optional == "해지"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            bank.close_account(name, password, name_ceo, name_charge)
        else:
            bank.close_account(name, password)

    elif(optional == "입금"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("입금할 금액을 입력하세요: "))
        if amount < 0:
            print("입력 오류")
            return
        if amount % 10000:
            print("입금은 만원 단위로 가능합니다.")
            return
        
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            bank.deposit(name, password, amount, name_ceo, name_charge)
        else:
            bank.deposit(name, password, amount)

    elif(optional == "출금"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("출금할 금액을 입력하세요: "))
        if amount < 0:
            print("입력 오류")
            return
        if amount % 10000:
            print("출금은 만원 단위로 가능합니다.")
            return
        
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            bank.withdraw(name, password, amount, name_ceo, name_charge)
        else:
            bank.withdraw(name, password, amount)

    elif(optional == "이체"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("이체할 금액을 입력하세요: "))
        if amount < 0:
            print("입력 오류")
            return
        
        destination_name = input("이체하실 계좌의 고객 이름을 입력하세요: ")
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            bank.transfer(name, password, destination_name, amount, name_ceo, name_charge)
        else:
            bank.transfer(name, password, destination_name, amount)

    elif(optional == "잔액확인"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '법인':
            name_ceo = input("법인 대표의 이름을 입력하세요: ")
            name_charge = input("담당직원 이름을 입력하세요: ")
            bank.view_account(name, password, name_ceo, name_charge)
        else:
            bank.view_account(name, password)
    
    elif(optional == 't'):
        bank.view_database()
        trans.view_database()

if __name__ == "__main__":
    front.start()
