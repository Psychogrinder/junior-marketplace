from marketplace import api
from marketplace.api_folder.cart_api import GlobalCart
from marketplace.api_folder.category_api import BaseCategories, Subcategories, SubcategoriesBySlug, \
    PopularProductsByCategory, ProductsByCategory
from marketplace.api_folder.consumer_api import GlobalConsumers, ConsumerRest, ConsumerOrders
from marketplace.api_folder.login_api import Login
from marketplace.api_folder.logout_api import Logout
from marketplace.api_folder.order_api import GlobalOrders, Orders
from marketplace.api_folder.producer_api import ProductsByProducer, GlobalProducers, ProducerRest, ProducerOrders
from marketplace.api_folder.product_api import GlobalProducts, ProductRest

# TODO CHECK
api.add_resource(GlobalOrders, '/orders')
api.add_resource(Orders, '/orders/<int:order_id>')
api.add_resource(ConsumerOrders, '/consumers/<int:consumer_id>/orders')
api.add_resource(ProducerOrders, '/producers/<int:producer_id>/orders')
api.add_resource(GlobalCart, '/consumers/<int:consumer_id>/cart')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

# checked
api.add_resource(BaseCategories, '/categories/base')
api.add_resource(Subcategories, '/categories/<int:category_id>/subcategories/')
api.add_resource(SubcategoriesBySlug, '/categories/slug/<string:category_slug>/subcategories/')
api.add_resource(GlobalProducts, '/products')
api.add_resource(ProductRest, '/products/<int:product_id>')
api.add_resource(ProductsByCategory, '/categories/<int:category_id>')
api.add_resource(PopularProductsByCategory, '/categories/<int:category_id>/popularity')
api.add_resource(ProductsByProducer, '/producers/<int:producer_id>/products')
api.add_resource(GlobalConsumers, '/consumers')
api.add_resource(ConsumerRest, '/consumers/<int:consumer_id>')
api.add_resource(GlobalProducers, '/producers')
api.add_resource(ProducerRest, '/producers/<int:producer_id>')