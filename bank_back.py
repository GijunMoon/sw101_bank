#은행 시스템 기능부

#req! : pip install pickle
#       pip install pandas
#run with cmd!! 없으면 오류나요

import main as front #메뉴 화면
import pickle        #DB 저장 lib
import pandas as pd  #DataFrame lib
import random        #계좌 번호 생성용 (random lib)

count_password = 0 #비밀번호 오류 횟수 체크용 global 변수

class TransactionLog: #class: 이체 기록 남기기
    def __init__(self): #__init__는 class 초기 실행시 작동합니다.
        try:
            with open('transaction_log.pkl', 'rb') as f: #읽기모드
                self.data = pickle.load(f)
        except FileNotFoundError: #db없는 경우 db생성
            self.data = pd.DataFrame(columns=['송금자', '수취인', '송금자 계좌번호', '수취인 계좌번호', '이체액'])
            self.save_data()

    def save_data(self): #db 저장 기능
        with open('transaction_log.pkl', 'wb') as f: #쓰기모드
            pickle.dump(self.data, f)

    def log_transaction(self, sender, receiver, sender_num, receiver_num, amount):#class 참조, 송금자, 수취인, 송금자 계좌번호, 수취인 계좌번호, 이체액
        new_row = {'송금자': sender, '수취인': receiver, '송금자 계좌번호': sender_num, '수취인 계좌번호': receiver_num, '이체액': amount}
        self.data.loc[len(self.data)] = new_row #데이터에 맞는 열 생성
        self.save_data()

    def view_database(self): #db 확인 : TODO - 은행 계좌를 가진 전체 고객 수, 개인고객 수, 법인고객 수, 당일의 은행 전체 잔액(잔고), 전체 입출금 내역이 담긴 보고서를 볼 수 있는 서비스를 제공
        print("========             지 누 은 행 이 체 정 보 조 회              ========\n")
        try:
            if self.data.empty: #DB는 있으나 텅 빈 경우
                print("저장된 정보가 없습니다.")
            else:
                print(self.data)
        except: #혹시나 DB 자체가 없는 경우 (__init__에서 검출하고 있으나 더블 체크)
            print("저장된 DB가 없습니다.")
            return
        print("\n======================================================================")

class Bank: #은행 기능 class
    def __init__(self):
        self.transaction_log = TransactionLog() #이체 기록 참조

        try:
            with open('db.pkl', 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError: #DB 파일 자체가 없는 경우
            self.data = pd.DataFrame(columns=['이름', '계좌번호', '비밀번호', '잔고', '고객구분', '법인대표', '담당직원'])
            self.save_data()

    def save_data(self):
        with open('db.pkl', 'wb') as f:
            pickle.dump(self.data, f)

    def create_account(self, name, password, initial_balance, customer_type, name_ceo, name_charge): #계좌 개설
        account_number = self.generate_account_number() #계좌 번호 생성
        #### 동일 이름을 가진 계좌 정보가 있는지 확인 ####
        account = self.data[(self.data['이름'] == name)] 

        try: #.iloc => 데이터값이 없을 경우 오류 출력. <= try-except 문으로 예외처리하여 해결
            if account['이름'].iloc[0] == name:
                print("이미 개설된 고객입니다.")
                return None
        ###############################################
        except:
            new_row = {'이름': name, '계좌번호': account_number, '비밀번호': password, '잔고': initial_balance, '고객구분': customer_type, '법인대표': name_ceo, '담당직원': name_charge}
            self.data.loc[len(self.data)] = new_row #가장 아랫줄에 추가
            self.save_data()
            print(f"{name}님의 계좌가 생성되었습니다. 계좌번호는 {account_number} 입니다.")
        ###############################################

    def find_account(self, name, password, name_ceo=None, name_charge=None, account_number=None): #계좌 조회
        if name_ceo and name_charge: #법인 고객인 경우
            account = self.data[(self.data['이름'] == name) & (self.data['비밀번호'] == password) & (self.data['법인대표'] == name_ceo) & (self.data['담당직원'] == name_charge)]
        else: #법인 고객이 아닌 경우
            account = self.data[(self.data['이름'] == name) & (self.data['비밀번호'] == password)]
        
        if account.empty: #정보가 없는 경우
            return None
        return account

    def view_account(self, name, password, name_ceo=None, name_charge=None): #잔액 확인
        account = self.find_account(name, password, name_ceo, name_charge)
        global count_password #최상단에 정의한 count_password 변수를 이 함수 내부에서도 공유
        if count_password >= 5:
            print("입력 5회 오류 입니다. 5분 후 다시 시도하세요.")
            count_password = 0
            return
        if account is None: 
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            count_password = count_password + 1
            return
        balance = account['잔고'].iloc[0] #잔고가 None인 케이스 존재하지 않으므로 예외처리 사용하지 않음
        count_password = 0
        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def deposit(self, name, password, amount, name_ceo=None, name_charge=None): #입금
        account = self.find_account(name, password, name_ceo, name_charge) #계좌 정보 조회
        global count_password
        if count_password >= 5:
            print("입력 5회 오류 입니다. 5분 후 다시 시도하세요.")
            count_password = 0
            return
        if account is None: 
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            count_password = count_password + 1
            return
        self.data.loc[account.index, '잔고'] += amount
        self.save_data()
        count_password = 0
        print(f"{account['계좌번호'].iloc[0]} 계좌에 {int(amount)}원을 입금하였습니다.")

    def withdraw(self, name, password, amount, name_ceo=None, name_charge=None): #출금
        account = self.find_account(name, password, name_ceo, name_charge)
        global count_password
        if count_password >= 5:
            print("입력 5회 오류 입니다. 5분 후 다시 시도하세요.")
            count_password = 0
            return
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            count_password = count_password + 1
            return
        if account['잔고'].iloc[0] < amount: #출금하고자 하는 금액보다 잔액이 적은 경우
            print("잔액이 부족합니다.")
            count_password = 0
            return
        self.data.loc[account.index, '잔고'] -= amount
        self.save_data()
        count_password = 0
        print(f"{account['계좌번호'].iloc[0]} 계좌에서 {int(amount)}원을 출금하였습니다.")

    def transfer(self, name, password, destination_name, amount, name_ceo=None, name_charge=None, account_number=None): #이체
        account = self.find_account(name, password, name_ceo, name_charge, account_number)
        global count_password
        if count_password >= 5:
            print("입력 5회 오류 입니다. 5분 후 다시 시도하세요.")
            count_password = 0
            return
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            count_password = count_password + 1
            return
        
        if account_number: #계좌로 찾기와 이름으로 찾기 모드
            destination_account = self.data[self.data['계좌번호'] == account_number]
        else:
            destination_account = self.data[self.data['이름'] == destination_name]
        if destination_account.empty:
            print("해당 수취인 계좌가 존재하지 않습니다.")
            count_password = 0
            return

        if account['잔고'].iloc[0] < amount + 1000: #이체액 + 수수료보다 잔액이 없는 경우
            print("잔액이 부족합니다.")
            count_password = 0
            return

        print("*이체 수수료 1000원이 발생합니다. \n수수료는 계좌에서 자동 출금 됩니다.")
        count_password = 0
        self.data.loc[account.index, '잔고'] -= (amount + 1000) #수수료와 이체액을 합한 만큼 본인 계좌에서 감산
        self.data.loc[destination_account.index, '잔고'] += amount
        self.save_data()
        fin_sender_number = account['계좌번호'].iloc[0]
        fin_destination_name = destination_account['이름'].iloc[0]
        fin_destination_number = destination_account['계좌번호'].iloc[0]

        print(f"{destination_account['계좌번호'].iloc[0]} ( {fin_destination_name} 님 ) 계좌에 {int(amount)}원을 입금하였습니다.")
        balance = account['잔고'].iloc[0] - (amount + 1000)
        self.transaction_log.log_transaction(name, fin_destination_name, fin_sender_number, fin_destination_number, amount)
        print(f"고객님의 계좌 잔액은 {balance}원 입니다.")

    def close_account(self, name, password, name_ceo=None, name_charge=None): #해지
        account = self.find_account(name, password, name_ceo, name_charge)
        global count_password
        if count_password >= 5:
            print("입력 5회 오류 입니다. 5분 후 다시 시도하세요.")
            count_password = 0
            return
        if account is None:
            print("해당 조건에 맞는 계좌가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
            count_password = count_password + 1
            return
        self.data = self.data[self.data['계좌번호'] != account['계좌번호'].iloc[0]] #행 제거 (NaN)
        self.save_data()
        count_password = 0
        print(f"{account['계좌번호'].iloc[0]} 계좌가 해지되었습니다.")

    def generate_account_number(self): #랜덤 계좌번호 생성기
        return '772-' + ''.join([str(random.randint(1000, 9999))]) + '-0114' 

    def view_database(self):
        print("========             지 누 은 행 관 리 자 시 스 템              ========\n")
        try:
            print("GNU 은행의 총 고객 수는 " + str(self.data.shape[0]) + " 명 입니다.")
            a = self.data['고객구분'].value_counts()[0:len(self.data['고객구분'].value_counts())]
            try:
                individual = a.iloc[0]
                print(f"GNU 은행의 총 개인고객 수는 {individual} 명 입니다.")
            except:
                print("GNU 은행의 총 개인고객 수는 0 명 입니다.")

            try:
                legal = a.iloc[1]
                print(f"GNU 은행의 총 법인고객 수는 {legal} 명 입니다.")
            except:
                print("GNU 은행의 총 법인고객 수는 0 명 입니다.")
            
            asset = sum(self.data['잔고'].iloc[0:len(self.data['잔고'])]) #복사
            print(f"GNU 은행의 전체 잔고는 {asset} 원 입니다.\n")
        except:
            print("저장된 DB가 없습니다.")


#######################################################################################################

def login(optional):
    bank = Bank()
    trans = TransactionLog()

    if(optional == "개설"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        try:
            initial_balance = int(input("최초 입금 금액을 입력하세요: "))
            if initial_balance < 0:
                print("입력 오류")
                return
        except ValueError:
            print("입력 오류. (정수값을 입력하세요.)")
            return
        
        if initial_balance < 10000:
            print("최초 입금 금액의 최소액은 1만원 입니다.")
            return
        customer_type = input("고객 구분을 입력하세요 (개인 또는 법인): ")
        if customer_type == '개인':
            isStudent = input("학생 / 직장인 / 사업가 중 어느 유형에 해당하십니까? (택 1): ")
            if isStudent == '학생':
                print("환영합니다. 학생 고객 혜택으로 1만원이 지급 되었습니다.")
                initial_balance = initial_balance + 10000
                bank.create_account(name, password, initial_balance, customer_type, None, None)
            elif isStudent == '직장인' or isStudent == '사업가':
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

        try:
            if amount < 0:
                print("입력 오류")
                return
            if amount % 10000:
                print("입금은 만원 단위로 가능합니다.")
                return
            bank.deposit(name, password, amount)
        except ValueError:
            print("입력 오류. (정수값을 입력하세요.)")
            return

    elif(optional == "출금"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")

        try:
            amount = int(input("출금할 금액을 입력하세요: "))
            if amount < 0:
                print("입력 오류")
                return
            if amount % 10000:
                print("출금은 만원 단위로 가능합니다.")
                return
        except ValueError:
            print("입력 오류. (정수값을 입력하세요.)")
            return
        
        bank.withdraw(name, password, amount)

    elif(optional == "이체"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        amount = int(input("이체할 금액을 입력하세요: "))
        try:
            amount = int(input("출금할 금액을 입력하세요: "))
            if amount < 0:
                print("입력 오류")
                return
        except ValueError:
            print("입력 오류. (정수값을 입력하세요.)")
            return
        
        destination_name = input("이체하실 계좌의 계좌 번호 혹은 고객 이름을 입력하세요: ")
        if destination_name[0] == '7': #계좌번호 형식이 772 - xxxx - 0114이므로 앞자리 7인지 검출.
            bank.transfer(name, password, None, amount, None, None, destination_name)
        else:
            bank.transfer(name, password, destination_name, amount, None, None, None)

    elif(optional == "잔액확인"):
        name = input("이름을 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        bank.view_account(name, password, None, None)
    
    elif(optional == '관리자'): #오후 6시
        print("오후 6시 이후 관리자 전용 시스템입니다.\n")
        bank.view_database()
        trans.view_database()

if __name__ == "__main__":
    front.start()
