from ecommerce.site import Site
from ecommerce.customer import Audience
from ecommerce.products import Stock, Marketing


stock = Stock()
site = Site(stock)

mkt = Marketing()
mkt.new_campaign()

audience = Audience(100)
audience.create()

# Atenção, compradores pode ser uma lista vazia
compradores = site.select_customers(audience)
cart = site.make_cart(mkt, compradores[0])
print(cart.to_string())