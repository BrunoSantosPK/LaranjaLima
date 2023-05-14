from uuid import uuid4
from datetime import date
from typing import List
from ecommerce.products import Product
from ecommerce.customer import Customer


class InfoNF:
    def __init__(self, product: Product, off: float, time: float, quantity: int) -> None:
        self.product: Product = product
        self.quantity: float = quantity
        self.time: float = time
        self.off: float = off


class NF:
    def __init__(self, dt: date, mkt_category: str, pix: bool, customer: Customer) -> None:
        self.__date = dt
        self.__pix_payment = pix
        self.__customer = customer
        self.__mkt_category = mkt_category
        self.__id = str(uuid4())
        self.__data: List[InfoNF] = []

    def add(self, info: InfoNF) -> None:
        self.__data.append(info)

    def to_json(self) -> List[dict]:
        data = []
        for info in self.__data:
            price = info.product.get_pix_price_off(info.off) if self.__pix_payment else info.product.get_price_off(info.off)
            data.append({
                "Data": self.__date,
                "Nota": self.__id,
                "Campanha em Curso": self.__mkt_category,
                "Cliente": self.__customer.get_id(),
                "Categoria": info.product.get_category(),
                "Produto": info.product.get_name(),
                "Quantidade": info.quantity,
                "Compra no PIX": "Sim" if self.__pix_payment else "Não",
                "Desconto Aplicado (%)": round(info.off * 100, 2),
                "Preço de Venda (R$)": round(price, 2),
                "Tempo de Finalização de compra (min)": round(info.time, 1)
        })
        return data
