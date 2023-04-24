import pandas as pd
from enum import Enum
from uuid import uuid4
from typing import List


class Category(Enum):
    LIVRO = "Livros"
    GAME = "Games"
    INFORMATICA = "Informática"
    ELETRODOMESTICO = "Eletrodomésticos"
    MOVEL = "Móveis"


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

    def __generate(self) -> None:
        for category, name, price, pix in self.__stock:
            self.__products.append(Product(category, name, price, pix))
