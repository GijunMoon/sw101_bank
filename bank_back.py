<<<<<<< HEAD
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
    front.start()
=======
## 은행 시스템 기능 구현

import main as front #front-end import
import pickle #변수 로컬 저장용

values = 0

def login(optional):
    #일단은 하드코딩.. case문으로 바꾸고 싶어요

    if(optional == "개설"):
        #print("1")
        name, pw = map(str, input("고객님의 이름과 계좌 비밀번호를 입력해주세요. \n>>").split())
        v = int(input("최초 입금액을 입력해주세요."))
        create_account(name, pw, v)

    elif(optional == "해지"):
        #print("2")
        name, pw = map(str, input("고객님의 이름과 계좌 비밀번호를 입력해주세요. \n>>").split())
        delete_account(name, pw)

    elif(optional == "입금"):
        #print("3")
        name, pw = map(str, input("고객님의 이름과 계좌 비밀번호를 입력해주세요. \n>>").split())
        global values 
        values = int(input("입금하실 금액을 입력해주세요.")) #숫자 아닌거 입력했을 때 오류 처리 : try-catch문
        deposit_account(name, pw, values)

    elif(optional == "출금"):
        name, pw = map(str, input("고객님의 이름과 계좌 비밀번호를 입력해주세요. \n>>").split())
        v = int(input("출금하실 금액을 입력해주세요."))
        withdraw_account(name, pw, v)

#def check_account():
    #ac = input("고객님의 이름과 계좌 비밀번호를 입력해주세요. \n>>")
    ## if(ac) 기존에 개설되어있는 계좌가 있는지 판단할 필요가 있을까??
    # 로컬 저장 기능이 있으므로 불러와서 비교는 가능.

def create_account(name, pw, v):
    deposit_account(name, pw, v)
    print(f'{name} 님의 명의로 계좌가 개설되었습니다.')

def delete_account(name, pw):
    print(f'{name} 님의 계좌가 해지되었습니다.')

def deposit_account(name, pw, v):
    with open("v.pickle","wb") as f:
            pickle.dump(v, f) #저장
    print(f'{name} 님의 계좌에 금 {v} 원이 입금 처리 되었습니다.')

def withdraw_account(name, pw, v):
    global values
    with open("v.pickle","rb") as f:
            values = pickle.load(f) #불러오기
    
    if(v > values):
        print("계좌에 잔액이 부족합니다.")
    else:
        with open("v.pickle","wb") as f:
            pickle.dump(values-v, f) #저장
        print(v, "원 만큼 출금이 완료되었습니다.", "잔액은", values-v, "원 입니다.")


if __name__ == "__main__":
    front.start()
>>>>>>> 5d2790b72abfc05831993b6a650494a093557895
