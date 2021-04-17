from __future__ import annotations
from typing import List, Dict, Optional
from abc import ABCMeta, abstractmethod


class AbstractBank(metaclass=ABCMeta):
    def __init__(self, name: str) -> None:
        self.name = name
        self.card_numbers = dict()

    @abstractmethod
    def add_account(
        self, card_number: str, pin: str, account: str, balance: int
    ) -> bool:
        pass

    @abstractmethod
    def check_pin(self, card_number: str, pin: str) -> Optional[Dict[str, int]]:
        pass

    @abstractmethod
    def control_balance(self, card_number: str, account: str, delta: int) -> int:
        pass

    @abstractmethod
    def get_balance(self, card_number: str, account: str) -> int:
        pass


class Bank(AbstractBank):
    def add_account(self, card_number: str, pin: str, account: str, balance: int) -> bool:
        if card_number in self.card_numbers:
            if self.card_numbers[card_number][0] != pin:
                return False

            if account not in self.card_numbers[card_number][1]:
                self.card_numbers[card_number][1][account] = balance
            else:
                return False
        else:
            self.card_numbers[card_number] = [pin, {account: balance}]
        return True

    def check_pin(self, card_number: str, pin: str) -> Optional[Dict[str, int]]:
        if card_number in self.card_numbers:
            if self.card_numbers[card_number][0] != pin:
                return None
            else:
                return self.card_numbers[card_number][1].keys()
        else:
            return None

    def control_balance(self, card_number: str, account: str, delta: int) -> int:
        if card_number in self.card_numbers:
            if account in self.card_numbers[card_number][1]:
                if self.card_numbers[card_number][1][account] + delta >= 0:
                    self.card_numbers[card_number][1][account] += delta
                    return self.card_numbers[card_number][1][account]
                else:
                    return -1
            else:
                return -1
        else:
            return -1

    def get_balance(self, card_number: str, account: str) -> Optional[int]:
        if card_number in self.card_numbers:
            if account in self.card_numbers[card_number][1]:
                return self.card_numbers[card_number][1][account]
            else:
                return -1
        else:
            return -1
