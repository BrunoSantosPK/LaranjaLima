import names
import numpy as np
import pandas as pd
from enum import Enum
from uuid import uuid4
from typing import List


class Compulsivity(Enum):
    BAIXISSIMA = 1
    BAIXA = 2
    ALTA = 3
    ALTISSIMA = 4


class Customer:

    def __init__(self, compulsivity: Compulsivity) -> None:
        self.__compulsivity = compulsivity
        self.__id = str(uuid4())

    def get_id(self) -> str:
        return self.__id
    
    def get_compulsivity(self) -> int:
        return self.__compulsivity.value


class Audience:

    def __init__(self, n_customers: int) -> None:
        self.__total_customers = n_customers
        self.__customers: List[Customer] = []

    def create(self) -> List[Customer]:
        possibilities = [Compulsivity.BAIXISSIMA, Compulsivity.BAIXA, Compulsivity.ALTA, Compulsivity.ALTISSIMA]
        _min = self.__total_customers // len(possibilities)
        available = [_min] * len(possibilities)

        while sum(available) < self.__total_customers:
            i = np.random.randint(0, len(possibilities))
            available[i] = available[i] + 1

        while len(self.__customers) < self.__total_customers:
            i = np.random.randint(0, len(possibilities))
            if available[i] > 0:
                self.__customers.append(Customer(possibilities[i]))
                available[i] = available[i] - 1
        
        return self.__customers
    
    def get_data(self) -> pd.DataFrame:
        data = []
        columns = ["Nome", "Identificador", "Nível de Compulsividade"]
        for customer in self.__customers:
            data.append([
                names.get_full_name(),
                customer.get_id(),
                customer.get_compulsivity()
            ])
        return pd.DataFrame(data, columns=columns)
