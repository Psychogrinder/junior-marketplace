from marketplace import api
from marketplace.api.category_api import BaseCategories, Subcategories, PopularProductsByCategory, ProductsByCategory
from marketplace.api.consumer_api import GlobalConsumers, ConsumerRest, ConsumerOrders
from marketplace.api.order_api import GlobalOrders, Orders
from marketplace.api.producer_api import ProductsByProducer, GlobalProducers, ProducerRest, ProducerOrders
from marketplace.api.product_api import GlobalProducts, ProductRest

api.add_resource(GlobalOrders, '/api/orders')
api.add_resource(Orders, '/api/orders/<int:order_id>')
api.add_resource(BaseCategories, '/api/categories/base')
api.add_resource(Subcategories, '/api/categories/<int:category_id>/subcategories/')
api.add_resource(ProductsByCategory, '/api/categories/<int:category_id>')
api.add_resource(PopularProductsByCategory, '/api/category/<int:category_id>/popularity')
api.add_resource(ProductsByProducer, '/api/producers/<int:produce_id>/products')
api.add_resource(GlobalProducts, '/api/products')
api.add_resource(ProductRest, '/api/products/<int:product_id>')
api.add_resource(GlobalConsumers, '/api/consumers')
api.add_resource(ConsumerRest, '/api/consumers/<int:consumer_id>')
api.add_resource(ConsumerOrders, '/api/consumers/<int:consumer_id>/orders')
api.add_resource(GlobalProducers, '/api/producers')
api.add_resource(ProducerRest, '/api/producers/<int:consumer_id>')
api.add_resource(ProducerOrders, '/api/producers/<int:consumer_id>/orders')

