from flask import session
from flask_restful import Resource, Api, reqparse
from marketplace.app.marketplace import Product
from marketplace.app.marketplace import Producer

api = Api(app)


class ProductRest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id')
    parser.add_argument('image_link')
    parser.add_argument('name')
    parser.add_argument('price')
    parser.add_argument('image')
    parser.add_argument('quantity')
    parser.add_argument('measurement_unit')
    parser.add_argument('description')

    def get(self, id):
        """
        :return: карточка товара
        """
        # вернуть карточку товара  по id
        product = Product.query.filter_by(id=id).first()
        if product:
            producer = Producer.query(id=product.producer_id).first()
            producer_name = producer.name
            result = product.to_json()
            result['producer'] = producer_name
            return result
        else:
            return {'error': 'No product with such id'}, 404

    def post(self):
        """
        Добавить продукт в каталог.

        Чтобы не загружать изображение раньше времени (вдргу ошибка), фронт присылает одно
        из значений image: либо 0, либо 1. Если значение 0, значит фото не было добавлено.
        Если 1 значит было. После того, как добавли товар в БД, отправляем ответ, в котором
        указываем значение image 1. Фронт это видит и загружает изображение на сервер, а сюда
        посылает ссылку на него. Всё это в теории.
        """
        args = self.parser.parse_args()

        producer = session['name']
        if product_name in producer.products:
            return {'error': f'Producer {producer} already has product with name {product_name}'}, 400
        new_product = Product(name=args['name'],
                              producer=args['producer'],
                              price=args['price'],
                              quantity=args['quantity'],
                              measurement_unit=args['measurement_unit'],
                              description=args['description'])

        session.add(new_product)
        session.commit()

        if image == 0:
            return {'message': 'New product has been added', 'image': 0}
        else:
            return {'message': 'New product has been added', 'image': 1, 'product_id': new_product.id}

    def delete(self, id):
        """
        Удалить продукт из БД
        """
        product = Product.query.filter_by(id=id).first()
        if product:
            session.delete(product)
            session.commit()
            return {'message': 'The product has been deleted'}
        else:
            return {'message': 'No product with such id'}

    def put(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            args = self.parser.parse_args()
            for k, v in args:
                if v is not None:
                    product.k = v
            return {'message': 'The product information has been updated'}
        else:
            return {'message': 'No product with such id'}


class ImageUpload(Resource):
    def post(self):
        args = self.parser.parse_args()
        product = Product.query.filter_by(id=args['id']).first()
        product.image = args['image_link']
        session.commit()


api.add_resource(ProductRest, '/product')
api.add_resource(ProductRest, '/product/<int:num>')
api.add_resource(ImageUpload, '/product/image')
