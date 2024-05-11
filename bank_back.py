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

    def view_database(self):#DB관리 func
        print(self.data)

class Bank:
    def __init__(self): #DB 초기화  
        self.transaction_log = TransactionLog()

        try:
            with open('db.pkl', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['이름', '계좌번호', '비밀번호', '잔고', '고객구분'])
            self.save_data()

    def save_data(self): #DB 저장 
        with open('db.pkl', 'wb') as f:
            pickle.dump(self.data, f)

    def create_account(self, name, password, initial_balance, customer_type): #이름 / 비번 / 계좌번호(auto created) / 고객구분
        account_number = self.generate_account_number()
        new_row = {'이름': name, '계좌번호': account_number, '비밀번호': password, '잔고': initial_balance, '고객구분': customer_type}
        self.data.loc[len(self.data)] = new_row #Value Error 방지 (행 개수 맞지 않는 버그)
        self.save_data()
        print(f"{name}님의 계좌가 생성되었습니다. 계좌번호는 {account_number} 입니다.")

    def view_account(self, account_number, password):
        count_password = 0
        account = self.data[self.data['계좌번호'] == account_number] #계좌번호 조회
        if count_password >= 5:
            print("비밀번호 5회 오류 입니다. 5분 후 다시 시도하세요.")
            return
        
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            count_password += 1
            return
        
        balance = account['잔고'].iloc[0]

        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def deposit(self, account_number, password, amount): #계좌번호 / 비번 / 출금금액
        account = self.data[self.data['계좌번호'] == account_number] #계좌번호 조회
        count_password = 0
        if count_password >= 5:
            print("비밀번호 5회 오류 입니다. 5분 후 다시 시도하세요.")
            return
        
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            count_password += 1
            return
        self.data.loc[self.data['계좌번호'] == account_number, '잔고'] += amount
        self.save_data()
        print(f"{account_number} 계좌에 {int(amount)}원을 입금하였습니다.")

    def withdraw(self, account_number, password, amount):
        account = self.data[self.data['계좌번호'] == account_number]
        count_password = 0
        if count_password >= 5:
            print("비밀번호 5회 오류 입니다. 5분 후 다시 시도하세요.")
            return
        
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            count_password += 1
            return
        if account['잔고'].iloc[0] < amount:
            print("잔액이 부족합니다.")
            return
        self.data.loc[self.data['계좌번호'] == account_number, '잔고'] -= amount
        self.save_data()
        print(f"{account_number} 계좌에서 {int(amount)}원을 출금하였습니다.")


    def transfer(self, account_number, password, destination_account_number, amount):

        account = self.data[self.data['계좌번호'] == account_number] #계좌번호 조회
        des_account = self.data[self.data['계좌번호'] == destination_account_number]
        count_password = 0
        
        if count_password >= 5:
            print("비밀번호 5회 오류 입니다. 5분 후 다시 시도하세요.")
            return
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            count_password += 1
            return
        if des_account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        
        if account['잔고'].iloc[0] < amount+1000:
            print("잔액이 부족합니다.")
            return
        
        print("*이체 수수료 1000원이 발생합니다. \n수수료는 계좌에서 자동 출금 됩니다.")
        self.data.loc[self.data['계좌번호'] == account_number, '잔고'] -= (amount+1000) #출금
        self.data.loc[self.data['계좌번호'] == destination_account_number, '잔고'] += (amount) #입금
        self.save_data()
        print(f"{destination_account_number} ( {des_account['이름'].iloc[0]} 님 )계좌에 {int(amount)}원을 입금하였습니다.")

        balance = account['잔고'].iloc[0] - (amount+1000)

        self.transaction_log.log_transaction(account_number, destination_account_number, amount)

        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def close_account(self, account_number, password):
        account = self.data[self.data['계좌번호'] == account_number]
        count_password = 0
        if count_password >= 5:
            print("비밀번호 5회 오류 입니다. 5분 후 다시 시도하세요.")
            return
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            count_password += 1
            return
        self.data = self.data[self.data['계좌번호'] != account_number]
        self.save_data()
        print(f"{account_number} 계좌가 해지되었습니다.")

    def generate_account_number(self):#랜덤 계좌번호 생성기
        return '772-' + ''.join([str(random.randint(1000, 9999))]) + '-0114' #772-nnnn-0114 형식
    
    def view_database(self):#DB관리 func
        print(self.data)





######################################################




def login(optional):
    bank = Bank()
    trans = TransactionLog()

    if(optional == "개설"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        initial_balance = int(input("최초 입금 금액을 입력하세요: "))
        customer_type = input("고객 구분을 입력하세요 (0 또는 1): ") #0: 법인고객 #1:개인고객
        bank.create_account(name, password, initial_balance, customer_type)

    elif(optional == "해지"):
        account_number = input("계좌번호를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        bank.close_account(account_number, password)

    elif(optional == "입금"):
        account_number = input("계좌번호를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("입금할 금액을 입력하세요: "))
        bank.deposit(account_number, password, amount)

    elif(optional == "출금"):
        account_number = input("계좌번호를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("출금할 금액을 입력하세요: "))
        bank.withdraw(account_number, password, amount)

    elif(optional == "이체"):
        account_number = input("계좌번호를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("이체할 금액을 입력하세요: "))

        destination_account_number = input("이체하실 계좌의 계좌번호를 입력하세요: ")
        bank.transfer(account_number, password, destination_account_number, amount)

    elif(optional == "잔액확인"):
        account_number = input("계좌번호를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        bank.view_account(account_number, password)
    
    elif(optional == 't'): #오후 6시 이후
        bank.view_database()
        trans.view_database()

if __name__ == "__main__":
    front.start()
