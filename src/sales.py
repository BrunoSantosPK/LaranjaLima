import os
import numpy as np
import pandas as pd
from datetime import date, timedelta
from ecommerce.customer import Audience
from ecommerce.products import Stock, Marketing
from ecommerce.site import Site


if __name__ == "__main__":
    # Definição de parâmetros para gestão de arquivos
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # Cria o conjunto de clientes e produtos para realização de transações
    stock = Stock()
    site = Site(stock)
    audience = Audience(100)
    audience.create()

    # Define intervalo de tempo e parâmetros de controle
    start_date = date(2022, 1, 1)
    end_date = date(2023, 4, 30)
    current_date = start_date

    # Define sistema de campanhas de marketing
    interval = 15
    campaign = Marketing()
    last_campaign = start_date - timedelta(days=interval)

    purchases = []
    while current_date <= end_date:
        # Log de acompanhamento
        p = round((current_date - start_date).days * 100 / (end_date - start_date).days, 2)
        print(f"Simulação em {p}%", end="\r")

        # Caso o intervalo entre campanhas de marketing seja atingido, cria uma nova
        if (current_date - last_campaign).days >= 15:
            current_campaign = campaign.new_campaign()
            last_campaign = current_date

        # De uma sequência de visitas, encontra quantos clientes realizaram compra,
        # seguindo com o fluxo de venda e obtenção de dados da nota
        customers = site.select_customers(audience)
        for customer in customers:
            cart = site.make_cart(campaign, customer)
            nf = site.execute_purchase(cart, campaign, current_date)
            purchases.extend(nf.to_json())

        # Avança no tempo
        current_date = current_date + timedelta(days=1)

    # Salva os dados das vendas
    with pd.ExcelWriter(f"{base_path}/data/ecommerce.xlsx", mode="a", if_sheet_exists="replace") as file:
        pd.DataFrame(purchases).to_excel(file, sheet_name="Vendas", index=False)

    '''
    Base 1: é preciso ter uma lista de 100 clientes com o total gasto, número de compras,
    tempo desde a última compra e gasto setorizado por grande categoria de produto.

    Base 2: os dados necessários são perfil do cliente, método de pagamento, tempo de decisão
    desde o início da compra, gasto total na compra, gasto setorizado na compra.

    Base 3: os dados necessários são perfil de consumidor, preço do produto, categoria do produto,
    valor de desconto, vendas no último mês do produto, tempo desde a última promoção/campanha de
    marketing para o produto e a quantidade vendida.

    Base 4: os dados necessários são produto foco da campanha de marketing, gasto com publicidade,
    público alvo (perfil de consumidor), vendas concluídas no último mês e valor total vendido na
    campanha de marketing.

    Base 5: os dados necessários são identificador da campanha de marketing, aderência de um cliente
    na campanha, perfil do cliente, total gasto pelo cliente historicamente na categoria da campanha,
    total gasto pelo cliente no último mês na categoria da campanha, ticket médio dos produtos na
    campanha e ticket médio gasto pelo cliente.
    '''

    '''
    Estratégia:
    - exite o total de 5 categorias de produtos: livros, games, informática, eletrodomésticos e móveis
    - os produtos disponíveis em cada categoria são:
    - ...
    - serão simuladas vendas diárias, que variam entre 10 e 25
    - o período de tempo analisado será de 01/01/2022 e 30/04/2023
    - cada cliente tem a mesma probabilidade de comprar qualquer item, com a possibilidade de alteração por
    meio da compulsividade própria (1 a 4), onde 4 dobra a chance de compra
    - a cada 15 dias uma campanha de marketing é feita em um determinado tipo de produto
    - durante uma campanha de marketing, as probabilidades de venda de produtos da categoria são maiores
    - durante uma campanha de marketing, cliente com compulsividade 3 e 4 dobram novamente as chances de compra
    - para cada compra, um tempo de finalização da compra deve ser atribuídos, variando em sigmoide desde 5 minutos até 60 minutos
    - existe uma probabilidade baixa do cliente levar dois produtos, menor de levar três e quase inexistente de levar até 5 produtos
    - o preço base do produto varia de acordo com o IPCA do mês para a categoria
    - existe uma pequena probabilidade de um produto estar com desconto de 10% a vista e 5% a prazo
    - durante uma campanha de marketing, todos os produtos da categoria estão com desconto entre 10% e 12% a vista e 5% a 7% a prazo
    - cada campanha de marketing tem um custo entre R$ 20.000 e R$ 30.000, podendo ser ajustado durante a simulação
    - quanto maior o gasto de marketing, maios o aumento da probabilidade de venda
    '''
