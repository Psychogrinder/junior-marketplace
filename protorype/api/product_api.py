from flask import session
from flask_restful import Resource, Api
from marketplace.app.marketplace import Product as dbProduct
from marketplace.app.marketplace import Producer as dbProducer

api = Api(app)


# но зачем?
class CatalogProduct(Resource):
    def get(self, num):
        # вернуть карточку товара  по id
        product = dbProduct.query.filter_by(id == id).first()
        if product:
            producer = dbProducer.query(id=product.producer_id).first()
            producer_name = producer.name
            return {'description': 'product data',
                    'data': {'id': num, 'name': product.name, 'producer': producer_name, "price": product.price,
                             "image": product.image}}
        else:
            return {'error': 'No product with such id'}, 404


class Product(Resource):
    def get(self, product_id):
        """
        :return: карточка товара
        """
        # вернуть карточку товара  по id
        product = dbProduct.query.filter_by(id=product_id).first()
        if product:
            producer = dbProducer.query(id=product.producer_id).first()
            producer_name = producer.name
            return {'description': 'product data',
                    'data': {'id': product_id, 'name': product.name, 'producer': producer_name, "price": product.price,
                             "image": product.image}}
        else:
            return {'error': 'No product with such id'}, 404

    def post(self, product_name, producer, price, image=0):
        """
        Добавить продукт в каталог.

        Чтобы не загружать изображение раньше времени (вдргу ошибка), фронт присылает одно
        из значений image: либо 0, либо 1. Если значение 0, значит фото не было добавлено.
        Если 1 значит было. После того, как добавли товар в БД, отправляем ответ, в котором
        указываем значение image 1. Фронт это видит и загружает изображение на сервер, а сюда
        посылает ссылку на него. Всё это в теории.
        """
        producer = session['name']
        if product_name in producer.products:
            return {'error': f'Producer {producer} already has product with name {product_name}'}, 400
        new_product = dbProduct(name=product_name, producer=producer, price=price)
        db.session.add(new_product)
        db.session.commit()

        if image == 0:
            return {'message': 'New product has been added', 'image': 0}
        else:
            return {'message': 'New product has been added', 'image': 1, 'product_id': new_product.id}


class ImageUpload(Resource):
    def post(self, id, image_link):
        product = dbProduct.query.filter_by(id=id).first()
        product.image = image_link
        db.session.commit()


api.add_resource(CatalogProduct, '/product/catalog/<int:product_id>')
api.add_resource(Product, '/product/<int:num>')
api.add_resource(Product, '/product')
api.add_resource(ImageUpload, '/product/image')
