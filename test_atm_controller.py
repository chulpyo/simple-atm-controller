import pytest

from bank import Bank
from atm_controller import AtmController, ControlType
from cash_bin import CashBin
from card_reader import CardReader


@pytest.fixture(scope="module")
def cards():
    """ 카드 데이터 fixture 생성 """

    # 쉽게 알아보기 위하여 card number와 account를 문자열로 처리
    card_list = {
        "card1": [
            "1234",
            {
                "account1-card1": 100000,
                "account2-card1": 100000,
            },
        ],
        "card2": [
            "4321",
            {
                "account1-card2": 100000,
            },
        ],
        "card3": [
            "1515",
            {
                "account1-card3": 100000,
            },
        ],
    }

    return card_list


@pytest.fixture(scope="module")
def one_bank(cards):
    """ 은행 fixture 생성 """
    bank1 = Bank("은행1")

    for k, v in cards.items():
        for account, balance in v[1].items():
            bank1.add_account(k, v[0], account, balance)

    return bank1


@pytest.fixture(scope="module")
def one_cash_bin():
    """ 현금통 fixture 생성 """
    cash = CashBin(1000000)
    return cash


@pytest.fixture(scope="module")
def one_card_reader(cards):
    """ 카드리더 fixture 생성 """
    # 임의로 하나의 카드만 선택
    card = CardReader([list(cards.keys())[1]])
    return card


@pytest.fixture(scope="module")
def atm(one_bank, one_cash_bin, one_card_reader):
    """ atm contoller fixture 생성 """
    controller = AtmController(one_bank, one_cash_bin, one_card_reader)
    return controller


def test_test():
    """ 테스트 동작 확인 """
    assert True


# class 생성 테스트
def test_init_bank(one_bank):
    """ virtual bank 객체 생성 확인 """

    card_list = ["card1", "card2", "card3"]

    for card in card_list:
        if card not in one_bank.card_numbers:
            assert False

    assert one_bank is not None


def test_init_cash_bin(one_cash_bin):
    """ 현금통 생성 확인 """
    assert one_cash_bin is not None


def test_init_card_reader(one_card_reader):
    """ 카드리더 생성 확인 """
    assert one_card_reader is not None


def test_init_atmcontroller(atm):
    """ atm contoller 객체 생성 확인 """
    assert atm is not None


# bank test
def test_bank_add_account(one_bank):
    """ 계좌 생성 가능 여부 확인 """
    one_bank.add_account("card3", "1515", "account2-card3", 1)
    assert one_bank.get_balance("card3", "account2-card3") == 1


def test_bank_duplicate_account(one_bank):
    """ 계좌 중복 예외 발생 확인 """
    assert one_bank.add_account("card1", "1234", "account1-card1", 1) == False


def test_bank_pin_error(one_bank):
    """ pin error 확인 """
    assert one_bank.add_account("card1", "4321", "account3-card1", 1) == False


def test_bank_control_balance_withdraw(one_bank):
    """ 계좌 잔고 조정 확인 withdraw """
    assert one_bank.control_balance("card1", "account2-card1", -100000) == 0


def test_bank_control_balance_deposit(one_bank):
    """ 계좌 잔고 조정 확인 deposit """
    assert one_bank.control_balance("card1", "account2-card1", 100000) == 100000


def test_bank_get_balance_withdraw(one_bank):
    """ 계좌 잔고 확인 """
    assert one_bank.get_balance("card1", "account2-card1") == 100000


# cash bin 테스트
def test_cash_bin_get_balance(one_cash_bin):
    """ 현금통 잔고 확인 """
    assert one_cash_bin.get_balance() == 1000000


def test_cash_bin_deposit(one_cash_bin):
    """ 현금통 입금 확인 """
    assert one_cash_bin.deposit(1) == 1000001


def test_cash_bin_withdraw(one_cash_bin):
    """ 현금통 출금 확인 """
    assert one_cash_bin.withdraw(1) == 1000000


# card reader 테스트
def test_card_reader_get_card_number(cards, one_card_reader):
    """ 카드리더 카드 번호 선택 확인 """
    assert one_card_reader.get_card_number() in cards


# atm controller 테스트
def test_atm_input_pin(atm):
    """ pin 입력 """
    atm.input_pin("1234")

    assert atm.pin == "1234"


def test_atm_authentication_fail(atm):
    """ 잘못된 핀 입력 테스트 """
    assert not atm.authentication()[0]


def test_atm_authentication_success(atm):
    """ 유효한 핀 입력 테스트 """
    atm.input_pin("4321")
    assert atm.authentication()[0]


def test_atm_select_account_fail(atm):
    """ 유효하지 않은 계좌 선택 """

    # fixture에서 card2가 선택되어 있음
    assert not atm.select_account("account10-card2")[0]


def test_atm_select_account_success(atm):
    """ 유효한 계좌 선택 """

    # 이전 테스트에서 유효하지 않은 계좌 선택으로 상태 초기화
    atm.input_pin("4321")
    atm.authentication()
    assert atm.select_account("account1-card2")[0]


def test_atm_control_account_balance(atm):
    """ 계좌 잔고 출력 """

    atm.input_pin("4321")
    atm.authentication()
    atm.select_account("account1-card2")
    rst = atm.control_account(ControlType.SeeBalance)
    assert rst[0] and rst[2] == 100000


def test_atm_control_account_deposit(atm):
    """ 계좌 입금 """

    atm.input_pin("4321")
    atm.authentication()
    atm.select_account("account1-card2")
    rst = atm.control_account(ControlType.Deposit, 1)
    assert rst[0] and rst[2] == 100001


def test_atm_control_account_withdraw_fail(atm):
    """ 계좌 출금 실패 """

    atm.input_pin("4321")
    atm.authentication()
    atm.select_account("account1-card2")
    rst = atm.control_account(ControlType.Withdraw, 100002)
    assert not rst[0] and rst[1] == "계좌에 잔고가 부족합니다."


def test_atm_control_account_withdraw_success(atm):
    """ 계좌 출금 성공 """

    atm.input_pin("4321")
    atm.authentication()
    atm.select_account("account1-card2")
    rst = atm.control_account(ControlType.Withdraw, 100001)
    assert rst[0] and rst[1] == "성공" and rst[2] == 0
