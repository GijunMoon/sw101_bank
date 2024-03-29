def deposit(balance,money):
    print('잔액{0}원이며 입금하신 금액은{1}원 입니다.\
          귀하의 총 잔액은{2}원 입니다'\
          .format(balance,money,balance+money))
print(deposit(30000,20000))

def withdraw(balance,money):
    if balance<money:
        print('돈이나 넣고 출금을 해라 ㅅㅂ.')
    else :
        print('귀하의 잔액은{0}원 이며 출금하신 금액은{1}원 입니다.\
        귀하의 남은 잔액은{2}원 입니다.  '.format(balance,money,balance-money))
    
print(withdraw(200000,20000))

