from marketplace import api
from marketplace.api_folder.cart_api import GlobalCart, NumberOfProductsInCart
from marketplace.api_folder.category_api import BaseCategories, Subcategories, SubcategoriesBySlug, \
    PopularProductsByCategory, ProductsByCategory, ParentCategoryBySubcategoryId, CategoryRest, \
    SubcategoryNamesByProducerName, SubcategoryNamesByParentSlugAndProducerName
from marketplace.api_folder.consumer_api import GlobalConsumers, ConsumerRest, ConsumerOrders, UploadImageConsumer
from marketplace.api_folder.login_api import Login
from marketplace.api_folder.logout_api import Logout
from marketplace.api_folder.order_api import GlobalOrders, Orders
from marketplace.api_folder.producer_api import ProductsByProducer, GlobalProducers, ProducerRest, ProducerOrders, \
    UploadImageProducer, ProducerNamesByCategoryName
from marketplace.api_folder.product_api import GlobalProducts, ProductRest, UploadImageProduct, ProductsInCart, \
    ProductsByPrice, PopularProducts, ProductsSortedAndFiltered

# TODO CHECK

api.add_resource(GlobalOrders, '/orders')
api.add_resource(Orders, '/orders/<int:order_id>')
api.add_resource(ConsumerOrders, '/consumers/<int:consumer_id>/orders')
api.add_resource(ProducerOrders, '/producers/<int:producer_id>/orders')
api.add_resource(GlobalCart, '/consumers/<int:consumer_id>/cart')
api.add_resource(NumberOfProductsInCart, '/consumers/<int:consumer_id>/cart/quantity')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UploadImageConsumer, '/consumers/<int:consumer_id>/upload')
api.add_resource(UploadImageProducer, '/producers/<int:producer_id>/upload')
api.add_resource(UploadImageProduct, '/products/<int:product_id>/upload')
api.add_resource(CategoryRest, '/categories/<string:slug>')
api.add_resource(ProductsInCart, '/products/<int:consumer_id>/cart')
api.add_resource(SubcategoryNamesByProducerName, '/categories/producer/<string:producer_name>')
api.add_resource(SubcategoryNamesByParentSlugAndProducerName,
                 '/categories/<string:parent_category_slug>/producer/<string:producer_name>')
api.add_resource(ProducerNamesByCategoryName, '/producers/<string:category_name>')
# checked
api.add_resource(BaseCategories, '/categories/base')
api.add_resource(Subcategories, '/categories/<int:category_id>/subcategories/')
api.add_resource(ParentCategoryBySubcategoryId, '/categories/<int:category_id>/parent')
api.add_resource(SubcategoriesBySlug, '/categories/slug/<string:category_slug>/subcategories/')
api.add_resource(GlobalProducts, '/products')
api.add_resource(ProductRest, '/products/<int:product_id>')
api.add_resource(ProductsByCategory, '/categories/<int:category_id>')
api.add_resource(PopularProductsByCategory, '/categories/<int:category_id>/popularity/<string:direction>')
api.add_resource(ProductsByPrice, '/categories/<int:category_id>/price/<string:direction>')
api.add_resource(ProductsByProducer, '/producers/<int:producer_id>/products')
api.add_resource(GlobalConsumers, '/consumers')
api.add_resource(ConsumerRest, '/consumers/<int:consumer_id>')
api.add_resource(GlobalProducers, '/producers')
api.add_resource(ProducerRest, '/producers/<int:producer_id>')
api.add_resource(PopularProducts, '/products/popular')
api.add_resource(ProductsSortedAndFiltered, '/products/filter')
