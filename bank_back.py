#은행 시스템 기능부

import main as front
import pickle
import pandas as pd
import random

class Bank:
    def __init__(self): #DB 초기화
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

    def deposit(self, account_number, password, amount): #계좌번호 / 비번 / 출금금액
        account = self.data[self.data['계좌번호'] == account_number] #계좌번호 조회
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            return
        self.data.loc[self.data['계좌번호'] == account_number, '잔고'] += amount
        self.save_data()
        print(f"{account_number} 계좌에 {amount}원을 입금하였습니다.")

    def withdraw(self, account_number, password, amount):
        account = self.data[self.data['계좌번호'] == account_number]
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
            return
        if account['잔고'].iloc[0] < amount:
            print("잔액이 부족합니다.")
            return
        self.data.loc[self.data['계좌번호'] == account_number, '잔고'] -= amount
        self.save_data()
        print(f"{account_number} 계좌에서 {amount}원을 출금하였습니다.")

    def close_account(self, account_number, password):
        account = self.data[self.data['계좌번호'] == account_number]
        if account.empty:
            print("해당 계좌번호가 존재하지 않습니다.")
            return
        if account['비밀번호'].iloc[0] != password:
            print("비밀번호가 일치하지 않습니다.")
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
    
    elif(optional == 't'):
        bank.view_database()

if __name__ == "__main__":
<<<<<<< HEAD
    front.start()
=======
    front.start()
>>>>>>> dc26438d2113d9e60dd5dcf53377b14d3ec0a383
