from marketplace import api
from marketplace.category_api import BaseCategories, Subcategories, PopularProductsByCategory, ProductsByCategory
from marketplace.consumer_api import GlobalConsumers, ConsumerRest, ConsumerOrders
from marketplace.order_api import GlobalOrders, Orders
from marketplace.producer_api import ProductsByProducer, GlobalProducers, ProducerRest, ProducerOrders
from marketplace.product_api import GlobalProducts, ProductRest

api.add_resource(GlobalOrders, '/orders')
api.add_resource(Orders, '/orders/<int:order_id>')
api.add_resource(BaseCategories, '/categories/base')
api.add_resource(Subcategories, '/categories/<int:category_id>/subcategories/')
api.add_resource(ProductsByCategory, '/categories/<int:category_id>')
api.add_resource(PopularProductsByCategory, '/category/<int:category_id>/popularity')
api.add_resource(ProductsByProducer, '/producers/<int:produce_id>/products')
api.add_resource(GlobalProducts, '/products')
api.add_resource(ProductRest, '/products/<int:product_id>')
api.add_resource(GlobalConsumers, '/consumers')
api.add_resource(ConsumerRest, '/consumers/<int:consumer_id>')
api.add_resource(ConsumerOrders, '/consumer/<int:consumer_id>/orders')
api.add_resource(GlobalProducers, '/producers')
api.add_resource(ProducerRest, '/producers/<int:consumer_id>')
api.add_resource(ProducerOrders, '/producers/<int:consumer_id>/orders')

