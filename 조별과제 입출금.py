def deposit(balance,money):
    print('�ܾ�{0}���̸� �Ա��Ͻ� �ݾ���{1}�� �Դϴ�.\
          ������ �� �ܾ���{2}�� �Դϴ�'\
          .format(balance,money,balance+money))
print(deposit(30000,20000))

def withdraw(balance,money):
    if balance<money:
        print('���̳� �ְ� ����� �ض� ����.')
    else :
        print('������ �ܾ���{0}�� �̸� ����Ͻ� �ݾ���{1}�� �Դϴ�.\
        ������ ���� �ܾ���{2}�� �Դϴ�.  '.format(balance,money,balance-money))
    
print(withdraw(200000,20000))

