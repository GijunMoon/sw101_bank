# sw101_bank
소프트웨어 기초 E조 은행 프로그램

## 코드 설명

### bank_back.py

- count_password [const]
전체 프로그램에서 사용자가 비밀번호를 틀린 횟수를 기록합니다.
사용자가 **“종료 후 재시작”** 혹은 **“비밀번호를 맞출 때”** 까지 유지됩니다.
- TransactionLog [class]
이체 기록을 남기는 class 입니다. 고객정보와 다른 DB 파일에 이체 기록을 저장하므로 다른 class로 만들었습니다.
    - __init__
    class가 호출되는 처음 시점에 작동합니다. open()을 통해 transaction_log.pkl 파일을 읽어들입니다. 만약 transaction_log.pkl가 없으면 생성합니다. 이때 '송금자', '수취인', '송금자 계좌번호', '수취인 계좌번호', '이체액’의 열을 새로 생성합니다.
    - save_data
    open()을 이용해 쓰기모드로 파일을 읽습니다. pickle.dump를 통해 덮어씁니다. (csv 읽기쓰기와 동일)
    - log_transaction
    딕셔너리 타입으로 새로운 열을 만들어 저장합니다.
    - view_database
    db 파일에 내용이 있다면 이체 기록을 출력합니다.
- Bank [class]
    - __init__
    class가 호출되는 처음 시점에 작동합니다. open()을 통해 db.pkl 파일을 읽어들입니다. 만약 db.pkl가 없으면 생성합니다. 이때 '이름', '계좌번호', '비밀번호', '잔고', '고객구분', '법인대표', '담당직원’의 열을 새로 생성합니다.
    - save_data
    open()을 이용해 쓰기모드로 파일을 읽습니다. pickle.dump를 통해 덮어씁니다. (csv 읽기쓰기와 동일)
    - create_account
    계좌 개설에 해당하는 함수입니다.
    generate_account_number()를 통해 랜덤한 계좌번호를 생성하, 이름이 중복되는지 체크합니다. 중복되는 경우 다시 메뉴로 돌려보내고, 중복되지 않는 경우 개설을 진행합니다.
    - find_account
    계좌 정보 확인에 해당하는 함수입니다.
    법인 고객과 개인 고객을 구분하여 찾습니다. (법인 고객은 법인대표 이름과 담당직원 이름까지 체크 해야하므로)
    계좌 정보가 있는 경우 account를 리턴하고, 없는 경우 None을 리턴합니다.
    None은 비어있음을 표현하는 값입니다.
    - view_account
    잔액 확인에 해당하는 함수 입니다.
    account 정보를 find_account()를 통해 전달받아 잔액을 출력합니다.
    - deposit
    입금에 해당하는 함수입니다.
    account 정보를 find_account()를 통해 전달받아 amount 만큼 잔액에 추가합니다.
    - withdraw
    출금에 해당하는 함수입니다.
    account 정보를 find_account()를 통해 전달받아 amount 만큼 잔액에서 마이너스 합니다.
    이때 잔액이 amount 보다 적으면 잔액이 부족하다고 출력하며 메뉴로 돌아갑니다.
    - transfer
    이체에 해당하는 함수입니다.
    계좌 번호가 전달되었다면 계좌번호로, 이름이 전달되었다면 이름으로 account를 찾습니다.
    잔액이 amount+1000(수수료) 보다 적은 경우 이체가 되지 않습니다.
    - close_account
    해지에 해당하는 함수입니다.
    계좌번호와 비밀번호를 받아 account를 받아오고 해당 account가 있는 행을 삭제합니다.
    - generate_account_number
    random 라이브러리를 이용하여 4자리수의 랜덤 수를 생성합니다. 
    772-0000-0114 형식의 계좌번호를 생성합니다.
    (why?: 772-~-0114는 경상국립대 전화번호 형식임)
    - view_database
    db 파일에 내용이 있다면 사용자 목록을 출력합니다. 
    이때 총 행의 수를 세어 고객의 수를 출력합니다.
    ’고객구분’ 열의 항목들을 value_counts()를 이용하여 자동으로 개인과 기업고객으로 구분하여 출력합니다.
    이때 한 쪽의 정보가 없으면 0명입니다로 출력합니다.
    은행의 총 잔고는 DB의 ’잔고’ 열의 전체 항목을 가져와 sum()으로 더하여 출력합니다.
- login [func]
로그인 함수입니다.
각 메뉴에 맞는 입력이 들어오면 이름, 비번 등등을 입력받아 class: bank를 호출하여 값을 넘겨줍니다.