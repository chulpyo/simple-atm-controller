# simple-atm-controller
Code for simple ATM

Python 3.8, vscode를 기반으로 코드를 작성하고 테스트하였음.  

## 구현 설명

- AtmController Class(atm_controller.py)
    - ATM을 제어하는 클래스
    - 생성자는 ATM과 연결된 Bank, CashBin, CardReader 객체를 받음
    - input_pin 메서드는 선택된 Card Number에 사용할 Pin 입력
    - authentication 메서드는 Bank 객체로부터 Card Number와 연결된 Pin이 유효한지 확인
    - select_account 메서드는 계좌를 입력받아 해당 계좌가 유효한지 확인
    - control_account 메서드는 control type을 입력받아 See Balance, Deposite, Withdraw 기능을 수행

- Bank Class(bank.py)
    - 가상의 은행 객체
    - 은행에 연결된 카드정보를 저장
    - add_account 메서드는 Card Number, Pin, Account, Balance를 입력받아 저장
        - 계좌 정보는 card_numbers dict 맴버에 저장
        - Card Number는 임의의 문자열
        - Pin은 임의의 숫자로 이루어진 문자열
        - Account는 임의의 문자열
        - Balance는 0 이상의 정수
        - Card Number, Pin, Account, Balance는 다음과 같은 형식으로 저장
        ``` python
        # Select Account 단계가 있으므로 하나의 카드에 여러개의 계좌가 연결될 수 있다고 가정
        # Card Number와 Account 제거 기능은 추가로 구현하지 않음
        self.card_numbers = {
            "Card Number":[
                "Pin",
                {
                    "Account1": balance1,
                    "Account2": balance2,
                    .....
                }
            ]
        }
        ```

    - check_pin 메서드는 AtmController 클래스의 check_pin메서드와 연관되어 Card Number와 Pin을 입력받아 해당 Pin이 유효한지 확인 후 연결된 계좌 정보 반환
    - control_balance는 Card Number, Account, Amount를 입력받아 해당 계좌의 잔고를 제어(+,-)
    - get_balance메서드는 Card Number - Account에 남아있는 잔고 출력


- CashBin Class(cash_bin.py)
    - 현금통에대한 클래스
    - get_balance 메서드는 현재 CashBin에 남아있는 현금이 얾마나 되는지 확인
    - deposit 메서드는 CashBin에 현금 저장
    - withdraw 메서드는 CashBin에서 현금 출금

- CardReader Class(card_reader.py)
    - 카드리더에 대한 클래스
    - get_card_number는 카드리더기에 삽입된 카드의 번호를 반환

## 실행 방법

``` bash
# 저장소 복사
git clone https://github.com/chulpyo/simple-atm-controller.git
cd simple-atm-controller

# 가상환경 생성
mkdir venv
cd venv
python -m venv atm_venv

# 가상환경 활성화
cd ..
.\venv\atm_venv\Scripts\activate

# 필요 패키지 설치
python -m pip install -r requirements.txt

# 테스트 실행
pytest
```
