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
        self.__name = names.get_full_name()

    def get_id(self) -> str:
        return self.__id
    
    def get_compulsivity(self) -> int:
        return self.__compulsivity.value
    
    def get_name(self) -> str:
        return self.__name
    
    def get_time(self) -> float:
        limits = [(10, 60), (10, 30), (5, 30), (5, 20)]
        vmin, vmax = limits[self.get_compulsivity() - 1]
        return vmin + (vmax - vmin) * np.random.random_sample()


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
    
    def select_customer(self, lift=2):
        possibilities: List[Customer] = []
        for customer in self.__customers:
            if customer.get_compulsivity() in [1, 2]:
                possibilities.append(customer)
            elif customer.get_compulsivity() == 3:
                for i in range(0, lift * 2):
                    possibilities.append(customer)
            elif customer.get_compulsivity() == 4:
                for i in range(0, lift * 3):
                    possibilities.append(customer)
        
        return possibilities[np.random.randint(0, len(possibilities))]
    
    def get_data(self) -> pd.DataFrame:
        data = []
        columns = ["Nome", "Identificador", "Nível de Compulsividade"]
        for customer in self.__customers:
            data.append([
                customer.get_name(),
                customer.get_id(),
                customer.get_compulsivity()
            ])
        return pd.DataFrame(data, columns=columns)
