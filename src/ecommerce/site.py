import numpy as np
from uuid import uuid4
from typing import List
from ecommerce.products import Stock, Marketing, Product
from ecommerce.customer import Audience, Customer
from ecommerce.dto.nf import NF


class Cart:
    def __init__(self) -> None:
        self.__products: List[Product] = []

    def add(self, product: Product) -> None:
        self.__products.append(product)

    def total(self) -> float:
        value = 0
        for product in self.__products:
            value = value + product.get_price()
        return value
    
    def to_string(self):
        name = ""
        for product in self.__products:
            name = name + product.get_name() + f" R$ {product.get_price()} \n"
        return name


class Site:
    def __init__(self, stock: Stock) -> None:
        self.__stock = stock

    
    def select_customers(self, audience: Audience) -> List[Customer]:
        '''
        Recebe um público disponível e a partir dele seleciona clientes que serão
        direcionados para o fluxo de compra. O nível de compulsividade do cliente
        aumenta as chances dele entrar no fluxo de compra.
        '''
        result: List[Customer] = []
        quantity = np.random.randint(0, 20)
        for i in range(0, quantity):
            result.append(audience.select_customer(lift=3))
        return result

    def make_cart(self, marketing: Marketing, customer: Customer) -> Cart:
        '''
        Um cliente selecionado para entrar no fluxo de compra começa a montar os
        itens que levará. A probabilidade de comprar mais itens cai de acordo com
        o valor acumulado da compra até o momento. Produtos mais baratos possuem
        maior probabilidade de serem comprados. A campanha de marketing altera os
        produtos que estão mais disponíveis para a compra, ou seja, aumenta a sua
        probabilidade de compra por meio de mais exposição.
        '''

        cart = Cart()
        more = True

        category = marketing.get_category()
        portfolio = self.__stock.portfolio(category, lift=4)

        while more:
            i = np.random.randint(0, len(portfolio))
            cart.add(portfolio[i])

            partial = cart.total()
            prob_next = 1 - (1 / (1 + np.exp(-partial / 2000)))

            if np.random.random_sample() > prob_next:
                more = False

        return cart

    def execute_purchase(self, cart: Cart) -> NF:
        '''
        Dado um carrinho montado, define o método de pagamento (PIX ou não) e para
        cada produto verifica a disponibilidade de desconto (por produto).
        '''
        pix_payment = True if np.random.random_sample() < 0.5 else False
        off = 0 + 0.03 * np.random.random_sample()
        if pix_payment: off = 0.05 + 0.05 * np.random.random_sample()

        pass


if __name__ == "__main__":
    site = Site()
    site.visits()
    print(site)