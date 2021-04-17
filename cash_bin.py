from __future__ import annotations
from typing import List, Dict, Optional
from abc import ABCMeta, abstractmethod
from enum import Enum


class AbstractCashBin(metaclass=ABCMeta):
    def __init__(self, balance: int) -> None:
        self.balance = balance

    @abstractmethod
    def get_balance(self) -> int:
        pass

    @abstractmethod
    def deposit(self, amount: int) -> int:
        pass

    @abstractmethod
    def withdraw(self, amount: int) -> int:
        pass


class CashBin(AbstractCashBin):
    def get_balance(self) -> int:
        return self.balance

    def deposit(self, amount: int) -> int:
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int) -> int:
        self.balance -= amount
        return self.balance
