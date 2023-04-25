import numpy as np
import pandas as pd
from enum import Enum
from uuid import uuid4
from typing import List
from datetime import date
from ecommerce.customer import Audience


class Category(Enum):
    LIVRO = "Livros"
    GAME = "Games"
    INFORMATICA = "Informática"
    ELETRODOMESTICO = "Eletrodomésticos"
    MOVEL = "Móveis"


class Marketing:
    
    def __init__(self, lift=3) -> None:
        self.__sequence = [Category.LIVRO, Category.GAME, Category.INFORMATICA, Category.ELETRODOMESTICO, Category.MOVEL]
        self.__current = -1
        self.__lift = lift

    def get_category(self) -> Category:
        return self.__sequence[self.__current]

    def new_campaign(self) -> Category:
        while True:
            i = np.random.randint(0, len(self.__sequence))
            if i != self.__current:
                self.__current = i
                break
        return self.__sequence[i]
    
    def select_category(self) -> Category:
        possibilities: List[Category] = []
        for i in range(0, len(self.__sequence)):
            if i == self.__current:
                for j in range(0, self.__lift):
                    possibilities.append(self.__sequence[i])
            else:
                possibilities.append(self.__sequence[i])

        k = np.random.randint(0, len(possibilities))
        return possibilities[k]


class Product:

    def __init__(self, category: Category, name: str, price: float, pix: float) -> None:
        self.__category = category
        self.__name = name
        self.__price = price
        self.__pix = pix

    def get_category(self) -> str:
        return self.__category.value
    
    def get_name(self) -> str:
        return self.__name
    
    def get_price(self) -> str:
        return self.__price
    
    def get_pix_price(self) -> str:
        return self.__pix
    
    def get_price_off(self, off: float) -> float:
        if off >= 1 or off < 0:
            raise Exception("Desconto deve ser um valor entre 0 (inclusivo) e 1 (exclusivo).")    
        return self.__price * (1 - off)
    
    def get_pix_price_off(self, off: float) -> float:
        if off >= 1 or off < 0:
            raise Exception("Desconto deve ser um valor entre 0 (inclusivo) e 1 (exclusivo).")    
        return self.__pix * (1 - off)


class Products:

    def __init__(self) -> None:
        self.__products: List[Product] = []
        self.__hist = []
        self.__columns = ["Categoria", "Produto", "Preço Padrão (R$)", "Preço PIX (R$)"]
        self.__stock = [
            [Category.LIVRO, "Box Harry Potter 7 Livros - Capa Dura", 200, 178],
            [Category.LIVRO, "A Mandíbula de Caim", 36.99, 35],
            [Category.LIVRO, "Watchmen Edição Definitiva", 60, 55],
            [Category.LIVRO, "É Assim que Acaba", 37.99, 30.99],
            [Category.LIVRO, "Box Sombra e Ossos", 109.99, 99.99],
            [Category.LIVRO, "A Hipótese do Amor", 40.99, 35.99],

            [Category.GAME, "Console Playstation 5 Digital Edition", 3999.99, 3799.99],
            [Category.GAME, "Console Playstation 5", 4499.99, 4299.99],
            [Category.GAME, "Console Xbox Series S", 2249, 2199],
            [Category.GAME, "Console Playstation 4 + God of War Ragnarok", 2999.99, 2799.99],
            [Category.GAME, "Console Playstation 5 + God of War Ragnarok", 4799.99, 4399.99],

            [Category.INFORMATICA, "SSD 480GB", 189.99, 179.99],
            [Category.INFORMATICA, "Carregador iPhone", 64.90, 59.7],
            [Category.INFORMATICA, "HD Externo 1 TB", 299, 289],
            [Category.INFORMATICA, "Memória 8 GB", 120, 108],
            [Category.INFORMATICA, "Gabinete Gamer + Cooler", 297.79, 268.01],

            [Category.ELETRODOMESTICO, "Forno Micro-ondas 20 L", 567, 510.3],
            [Category.ELETRODOMESTICO, "Geladeira 260 L", 2398.11, 2206.26],
            [Category.ELETRODOMESTICO, "Lavadora de Roupas 8,5 kg", 1812.38, 1449.9],
            [Category.ELETRODOMESTICO, "Depurador de Ar 60 cm", 338.3, 299.99],
            [Category.ELETRODOMESTICO, "Fogão 5 Bocas", 1640.45, 1566.02],

            [Category.MOVEL, "Cadeira de Escritório", 229.9, 169],
            [Category.MOVEL, "Guarda Roupa 6 Portas", 674.32, 502.88],
            [Category.MOVEL, "Cadeira Gamer", 744.33, 669.89],
            [Category.MOVEL, "Estante de Aço 6 Prateleiras", 172.10, 156.45],
            [Category.MOVEL, "Cômoda 6 Gavetas", 575, 517.50]
        ]
        self.__generate()

    def get_data(self) -> pd.DataFrame:
        data = [[p.get_category(), p.get_name(), p.get_price(), p.get_pix_price()] for p in self.__products]
        return pd.DataFrame(data, columns=self.__columns)
    
    def get_products(self) -> List[Product]:
        return self.__products
    
    def get_purchases(self) -> pd.DataFrame:
        return pd.DataFrame(self.__hist)
    
    def sell(self, audience: Audience, campaign: Marketing, dt: date):
        # Seleciona um produto e verifica se ele faz parte da campanha de marketing
        product = self.select_product(campaign)
        in_campaign = True if product.get_category() == campaign.get_category().value else False

        # Atribui o aumento de probabilidade de compra de acordo com a campanha de marketing
        lift = 4 if in_campaign else 2
        customer = audience.select_customer(lift=lift)

        # Define método de compra e possível desconto
        pix_payment = True if np.random.random() < 0.5 else False
        off = self.__off(pix_payment, in_campaign)
        purchase_time = customer.get_time()
        price = product.get_pix_price_off(off) if pix_payment else product.get_price_off(off)

        # Registra os dados da venda
        self.__hist.append({
            "Data": dt,
            "Campanha em Curso": campaign.get_category().value,
            "Cliente": customer.get_id(),
            "Categoria": product.get_category(),
            "Produto": product.get_name(),
            "Compra no PIX": "Sim" if pix_payment else "Não",
            "Desconto Aplicado (%)": round(off * 100, 2),
            "Preço de Venda (R$)": round(price, 2),
            "Tempo de Finalização de compra (min)": round(purchase_time, 1)
        })

        return product, customer
    
    def select_product(self, campaign: Marketing) -> Product:
        category = campaign.select_category()
        possibilities: List[Product] = []

        for product in self.__products:
            if product.get_category() == category.value:
                possibilities.append(product)

        return possibilities[np.random.randint(0, len(possibilities))]

    def __generate(self) -> None:
        for category, name, price, pix in self.__stock:
            self.__products.append(Product(category, name, price, pix))

    def __off(self, pix: bool, mkt: bool) -> float:
        value = 0
        if pix and not mkt: value = 0.03 + 0.03 * np.random.random_sample()
        if pix and mkt: value = 0.08 + 0.04 * np.random.random_sample()
        if not pix and mkt: value = 0.03 + 0.04 * np.random.random_sample()
        if not pix and not mkt: value = 0 if np.random.random_sample() > 0.1 else 0.03
        return value
