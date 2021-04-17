from __future__ import annotations
from typing import List, Dict, Tuple, Optional
from abc import ABCMeta, abstractmethod
from enum import Enum

from bank import Bank
from cash_bin import CashBin
from card_reader import CardReader


class ControlType(Enum):
    SeeBalance = (0, "잔고 출력")
    Deposit = (1, "입금")
    Withdraw = (2, "출금")

    def __init__(self, code: int, desc: str) -> None:
        self.code = code
        self.desc = desc


class AbstractAtmController(metaclass=ABCMeta):
    def __init__(self, bank: Bank, cash_bin: CashBin, card_reader: CardReader) -> None:
        self.bank = bank
        self.cash_bin = cash_bin
        self.card_reader = card_reader
        self.accounts = None
        self.pin = None
        self.card_number = None
        self.account = None

    @abstractmethod
    def input_pin(self, pin: str) -> None:
        pass

    @abstractmethod
    def authentication(self, card_number: str, pin: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def select_account(self, account: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def control_account(
        self, control: ControlType, delta: int = 0
    ) -> Tuple[bool, str, int]:
        pass

    def finish(self) -> None:
        self.accounts = None
        self.pin = None
        self.card_number = None
        self.account = None


class AtmController(AbstractAtmController):
    def input_pin(self, pin: str) -> None:
        self.pin = pin

    def authentication(self) -> Tuple[bool, str]:
        self.card_number = self.card_reader.get_card_number()
        self.accounts = self.bank.check_pin(self.card_number, self.pin)
        if self.accounts is None:
            self.finish()
            return (False, "인증 실패.")
        else:
            return (True, "성공")

    def select_account(self, account: str) -> Tuple[bool, str]:
        if account in self.accounts:
            self.account = account
            return (True, "성공")
        else:
            self.finish()
            return (False, "존재하지 않는 계좌 입니다.")

    def control_account(
        self, control: ControlType, delta: int = 0
    ) -> Tuple[bool, str, int]:

        # 중복된 예외처리 존재, 개선 필요
        # 카드 번호, 계좌가 없을시 atmcontroller의 control_account와 bank의 control_balnce에서 동시에 채크함
        if self.card_number is None or self.account is None:
            self.finish()
            return (False, "카드번호 혹은 계좌가 존재하지 않습니다.", -1)

        if control == ControlType.SeeBalance:
            result = (True, "성공", self.bank.get_balance(self.card_number, self.account))

        elif control == ControlType.Deposit or control == ControlType.Withdraw:
            # delta 는 양의 정수만 입력된다고 가정
            if control == ControlType.Withdraw:
                delta = delta * -1

                if self.cash_bin.get_balance() + delta < 0:
                    self.finish()
                    return (False, "현금통에 현금이 부족합니다.", -1)

                if self.bank.get_balance(self.card_number, self.account) + delta < 0:
                    self.finish()
                    return (False, "계좌에 잔고가 부족합니다.", -1)

            balance = self.bank.control_balance(self.card_number, self.account, delta)

            if balance < 0:
                result = (False, "실패(예외처리용)", balance)
            else:
                result = (True, "성공", balance)

        else:
            result = (False, "잘못된 제어구문입니다.", -1)

        self.finish()
        return result
