from __future__ import annotations

import random

from typing import List, Dict, Optional
from abc import ABCMeta, abstractmethod
from enum import Enum


class AbstractCardReader(metaclass=ABCMeta):
    def __init__(self, card_numbers) -> None:
        self.card_numbers = card_numbers

    @abstractmethod
    def get_card_number(self) -> str:
        pass


class CardReader(AbstractCardReader):
    def get_card_number(self) -> str:
        return random.sample(self.card_numbers, 1)[0]
