import pandas as pd


class Products:
    
    def get(self) -> pd.DataFrame:
        return pd.DataFrame([
            {"Categoria": "Livros", "Produto": "Box Harry Potter 7 Livros - Capa Dura", "Preço Padrão": 200, "Preço PIX": 178},
            {"Categoria": "Livros", "Produto": "A Mandíbula de Caim", "Preço Padrão": 36.99, "Preço PIX": 35},
            {"Categoria": "Livros", "Produto": "Watchmen Edição Definitiva", "Preço Padrão": 60, "Preço PIX": 55},
            {"Categoria": "Livros", "Produto": "É Assim que Acaba", "Preço Padrão": 37.99, "Preço PIX": 30.99},
            {"Categoria": "Livros", "Produto": "Box Sombra e Ossos", "Preço Padrão": 109.99, "Preço PIX": 99.99},
            {"Categoria": "Livros", "Produto": "A Hipótese do Amor", "Preço Padrão": 40.99, "Preço PIX": 35.99},

            {"Categoria": "Games", "Produto": "Console Playstation 5 Digital Edition", "Preço Padrão": 3999.99, "Preço PIX": 3799.99},
            {"Categoria": "Games", "Produto": "Console Playstation 5", "Preço Padrão": 4499.99, "Preço PIX": 4299.99},
            {"Categoria": "Games", "Produto": "Console Xbox Series S", "Preço Padrão": 2249, "Preço PIX": 2199},
            {"Categoria": "Games", "Produto": "Console Playstation 4 + God of War Ragnarok", "Preço Padrão": 2999.99, "Preço PIX": 2799.99},
            {"Categoria": "Games", "Produto": "Console Playstation 5 + God of War Ragnarok", "Preço Padrão": 4799.99, "Preço PIX": 4399.99},

            {"Categoria": "Informática", "Produto": "SSD 480GB", "Preço Padrão": 189.99, "Preço PIX": 179.99},
            {"Categoria": "Informática", "Produto": "Carregador iPhone", "Preço Padrão": 64.90, "Preço PIX": 59.7},
            {"Categoria": "Informática", "Produto": "HD Externo 1 TB", "Preço Padrão": 299, "Preço PIX": 289},
            {"Categoria": "Informática", "Produto": "Memória 8 GB", "Preço Padrão": 120, "Preço PIX": 108},
            {"Categoria": "Informática", "Produto": "Gabinete Gamer + Cooler", "Preço Padrão": 297.79, "Preço PIX": 268.01},

            {"Categoria": "Eletrodomésticos", "Produto": "Forno Micro-ondas 20 L", "Preço Padrão": 567, "Preço PIX": 510.3},
            {"Categoria": "Eletrodomésticos", "Produto": "Geladeira 260 L", "Preço Padrão": 2398.11, "Preço PIX": 2206.26},
            {"Categoria": "Eletrodomésticos", "Produto": "Lavadora de Roupas 8,5 kg", "Preço Padrão": 1812.38, "Preço PIX": 1449.9},
            {"Categoria": "Eletrodomésticos", "Produto": "Depurador de Ar 60 cm", "Preço Padrão": 338.3, "Preço PIX": 299.99},
            {"Categoria": "Eletrodomésticos", "Produto": "Fogão 5 Bocas", "Preço Padrão": 1640.45, "Preço PIX": 1566.02},

            {"Categoria": "Móveis", "Produto": "Cadeira de Escritório", "Preço Padrão": 229.9, "Preço PIX": 169},
            {"Categoria": "Móveis", "Produto": "Guarda Roupa 6 Portas", "Preço Padrão": 674.32, "Preço PIX": 502.88},
            {"Categoria": "Móveis", "Produto": "Cadeira Gamer", "Preço Padrão": 744.33, "Preço PIX": 669.89},
            {"Categoria": "Móveis", "Produto": "Estante de Aço 6 Prateleiras", "Preço Padrão": 172.10, "Preço PIX": 156.45},
            {"Categoria": "Móveis", "Produto": "Cômoda 6 Gavetas", "Preço Padrão": 575, "Preço PIX": 517.50}
        ])
