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