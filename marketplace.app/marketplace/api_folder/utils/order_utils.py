from marketplace import db, ORDERS_PER_PAGE
from marketplace.api_folder.schemas import order_schema_list
from marketplace.api_folder.utils import product_utils
from marketplace.api_folder.utils.abortions import abort_if_producer_doesnt_exist_or_get, \
    abort_if_consumer_doesnt_exist_or_get, abort_if_order_doesnt_exist_or_get
from marketplace.models import Order, Product, Producer


def get_orders_by_producer_id(producer_id: int) -> list:
    """Returns list of orders connected with given producer"""
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Order.query.filter_by(producer_id=producer_id).all()


def get_orders_by_consumer_id(consumer_id: int) -> list:
    """Returns list of orders connected with given consumer"""
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    return Order.query.filter_by(consumer_id=consumer_id).all()


def get_order_by_id(order_id: int) -> Order:
    """Returns order with given id"""
    return abort_if_order_doesnt_exist_or_get(order_id)


def get_products_by_order_id(order_id: int) -> list:
    """Returns products from given order"""
    order_items = Order.query.filter_by(id=order_id).first().order_items_json
    products = []
    for item in order_items:
        products.append(product_utils.get_product_by_id(product_id=int(item)))
    return products


def get_all_orders() -> list:
    """Returns all orders"""
    return Order.query.all()


def put_order(args: dict, order_id: int) -> Order:
    """Changes given order"""
    order = get_order_by_id(order_id)
    if args['status'] is not None:
        order.change_status(args['status'])
    db.session.commit()
    return order


def delete_order_by_id(order_id: int) -> dict:
    """Delete order with given id"""
    order = get_order_by_id(int(order_id))
    db.session.delete(order)
    db.session.commit()
    return {"message": "Order with id {} has been deleted successfully".format(order_id)}


def get_number_of_unprocessed_orders_by_producer_id(producer_id: int) -> int:
    return len(Order.query.filter_by(producer_id=producer_id).filter_by(status='Необработан').all())


def get_filtered_orders(args: dict):
    """
    Функция для отображения заказов на странице истории заказов производителя.
    """
    order_status = args['order_status']
    page = int(args['page'])
    if order_status == 'Все':
        orders = Order.query.filter_by(producer_id=int(args['producer_id'])).order_by(
            Order.has_unread_consumer_messages.desc()).paginate(page, ORDERS_PER_PAGE)
        next_page = orders.next_num
        orders = order_schema_list.dump(orders.items).data
    else:
        orders = Order.query.filter_by(producer_id=int(args['producer_id'])).filter_by(status=order_status).order_by(
            Order.has_unread_consumer_messages.desc()).paginate(page, ORDERS_PER_PAGE)
        next_page = orders.next_num
        orders = order_schema_list.dump(orders.items).data
    for order in orders:
        order['items'] = []
        order['order_timestamp'] = order['order_timestamp'].split('T')[0]
        for product_id, quantity in order['order_items_json'].items():
            product_data = db.session.query(Product.id, Product.name, Product.price, Product.weight,
                                            Product.photo_url, Product.measurement_unit).filter_by(
                id=int(product_id)).first()
            order_product_schema = ("id", "name", "price", "weight", "photo_url", "measurement_unit")
            product = dict(zip(order_product_schema, product_data))
            product['quantity'] = quantity
            if product['weight'].is_integer():
                product['weight'] = int(product['weight'])
            order['items'].append(product)
        del order['order_items_json']

    return {'orders': orders,
            'page': next_page}


def get_formatted_orders_by_consumer_id(consumer_id: int, page: int) -> dict:
    """
    Функция для отображения заказов на странице истории заказов потребителя.
    """
    query = db.session.query(Order.id, Order.status, Order.delivery_method, Order.order_timestamp, Order.total_cost,
                             Order.order_items_json, Order.reviewed, Order.producer_id,
                             Order.has_unread_producer_messages,
                             Producer.name.label('producer_name')).filter(
        Order.producer_id == Producer.id).filter_by(consumer_id=consumer_id).order_by(
        Order.has_unread_producer_messages.desc()).paginate(page, ORDERS_PER_PAGE)
    next_num = query.next_num
    order_schema = ("id", "status", "delivery_method", "placement_date", "cost", "items", "reviewed", "producer_id",
                    "has_unread_messages", "producer_name")
    item_schema = ('name', 'price', 'id', 'weight', 'measurement_unit', 'photo_url')
    orders = []
    for order in query.items:
        order = dict(zip(order_schema, order))
        order['placement_date'] = order['placement_date'].strftime("%d.%m.%Y")
        new_items = []
        for product_id, quantity in order['items'].items():
            query = db.session.query(Product.name, Product.price, Product.id, Product.weight, Product.measurement_unit,
                                     Product.photo_url).filter_by(
                id=int(product_id)).first()
            item = dict(zip(item_schema, query))
            item['quantity'] = quantity
            if int(item['weight']) == item['weight']:
                item['weight'] = int(item['weight'])
            new_items.append(item)
        order['items'] = new_items
        orders.append(order)

    return {'orders': orders,
            'page': next_num}
