import string

from sqlalchemy import desc, func, exc
from sqlalchemy_searchable import inspect_search_vectors
from flask import url_for
from marketplace import db, app, PRODUCTS_PER_PAGE, sitemap_tools
from marketplace.api_folder.schemas import product_schema, product_schema_list
from marketplace.api_folder.utils.abortions import abort_if_product_doesnt_exist_or_get, \
    abort_if_producer_doesnt_exist_or_get, abort_if_category_doesnt_exist_or_get, abort_if_invalid_rating_value
from marketplace.api_folder.utils.category_utils import get_category_by_id, get_subcategories_by_category_id, \
    check_producer_categories, delete_categories_if_it_was_the_last_product
from marketplace.api_folder.utils.order_utils import get_order_by_id
from marketplace.api_folder.utils.producer_utils import get_producer_by_id
from marketplace.api_folder.utils.uploaders import upload_image
from marketplace.models import Product, Producer, Category
from marketplace.email_tools import send_notify_about_products_supply


def get_product_by_id(product_id: int) -> Product:
    """Returns product"""
    return abort_if_product_doesnt_exist_or_get(product_id)


def get_products_by_category_id(category_id: int) -> list:
    """Returns list of products by category"""
    category = get_category_by_id(category_id)
    if category.parent_id != 0:
        return category.get_products()
    else:
        subcategories = get_subcategories_by_category_id(category_id)
        divided_products = [subcategory.get_products() for subcategory in subcategories]
        return [product for subcategory in divided_products for product in subcategory]


def get_products_by_producer_id(producer_id: int) -> list:
    """Returns products of given producer"""
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Product.query.filter_by(producer_id=producer_id).all()


def get_product_rating_by_id(product_id: int) -> float:
    """Returns product rating"""
    return round(get_product_by_id(product_id).rating, 2)


def producer_has_products(producer_id: int) -> bool:
    abort_if_producer_doesnt_exist_or_get(producer_id)
    if Product.query.filter_by(producer_id=producer_id).first():
        return True
    return False


def get_all_products_from_a_list_of_categories(categories: list) -> list:
    """Returns products by given categories"""
    all_products = []
    for category in categories:
        all_products += category.get_products()
    return all_products


def get_products_from_a_parent_category(parent_category_id: int) -> list:
    """Returns products by parent category"""
    subcategories = get_subcategories_by_category_id(parent_category_id)
    return get_all_products_from_a_list_of_categories(subcategories)


def get_sorted_and_filtered_products(args: dict) -> dict:
    products = []
    args['page'] = int(args['page'])
    query = db.session.query(Product.id, Product.name, Product.price, Product.photo_url, Product.rating, Product.votes,
                             Producer.name.label('producer_name')).filter(
        Product.producer_id == Producer.id)

    if args['popularity']:
        if args['popularity'] == 'down':
            query = query.order_by(Product.times_ordered.desc())

    if args['rating']:
        query = query.order_by(Product.rating.desc(), Product.votes.desc())

    if args['producer_name']:
        query = query.filter(Producer.name == args['producer_name'])

    if args['in_stock'] == 'true':
        query = query.filter(Product.quantity > 0)

    if not args['in_stock'] == 'false':
        query = query.filter(Product.quantity >= 0)

    if args['search']:
        query = query.filter(Product.name.ilike('%' + args['search'] + '%'))

    if args['category_name']:
        # check if the category_name is in English. Then it means it's a parent category
        if args['category_name'][0] in string.ascii_lowercase:
            parent_category_id = db.session.query(Category.id).filter(Category.slug == args['category_name']).first()
            subcategory_ids = [el[0] for el in
                               db.session.query(Category.id).filter(Category.parent_id == parent_category_id).all()]
            query = query.filter(Product.category_id.in_(subcategory_ids))
        # else it's a subcategory and the name is in Russian
        else:
            category_id = db.session.query(Category.id).filter(Category.name == args['category_name']).first()
            query = query.filter(Product.category_id == category_id)

    if args['price']:
        if args['price'] == 'down':
            query = query.order_by(Product.price.desc())
        elif args['price'] == 'up':
            query = query.order_by(Product.price.asc())

    product_schema = ("id", "name", "price", "photo_url", "rating", "votes", "producer_name")
    page_products = query.paginate(args['page'], PRODUCTS_PER_PAGE)
    for product in page_products.items:
        products.append(dict(zip(product_schema, product)))
    for product in products:
        product['stars'] = get_formatted_rating(product['rating'])
    return {"products": products,
            "next_page": page_products.next_num}


def get_popular_products() -> list:
    """Returns 12 most popular products"""
    return Product.query.order_by(Product.times_ordered.desc()).limit(12).all()


def get_popular_products_by_category_id(category_id: int, direction: str) -> list:
    """
    Если direction == up, то товары возврщаются от наименее популярных до самых популярных. Если down, то наоборот.
    """
    if direction == 'up':
        reverse = False
    elif direction == 'down':
        reverse = True

    if get_category_by_id(category_id).parent_id != 0:
        category = get_category_by_id(category_id)
        return sorted(category.get_products(), key=lambda product: int(product.times_ordered), reverse=reverse)
    else:
        all_products = get_products_from_a_parent_category(category_id)
        return sorted(all_products, key=lambda product: int(product.times_ordered), reverse=reverse)


def get_products_by_category_id_sorted_by_price(category_id: int, direction: str) -> list:
    """
    Если direction == up, то товары возврщаются от самых дешёвых до самых дорогих. Если down, то наоборот.
    """
    if direction == 'up':
        reverse = False
    elif direction == 'down':
        reverse = True

    if get_category_by_id(category_id).parent_id != 0:
        category = get_category_by_id(category_id)
        return sorted(category.get_products(), key=lambda product: float(product.price.strip('₽').strip(' ')),
                      reverse=reverse)
    else:
        all_products = get_products_from_a_parent_category(category_id)
        return sorted(all_products, key=lambda product: float(product.price.strip('₽').strip(' ')), reverse=reverse)


def get_products_by_order_id(order_id: int) -> list:
    """Returns products from order"""
    order_items = get_order_by_id(order_id).order_items_json
    products = []
    for item in order_items:
        products.append(Product.query.filter_by(id=int(item)).first())
    return products


def get_all_products() -> list:
    """Returns all products"""
    return Product.query.all()


def producer_has_product_with_such_name(args: dict) -> bool:
    """Returns if producer provides product with given id"""
    if Product.query.filter_by(producer_id=args['producer_id']).filter_by(name=args['name']).first():
        return True


def search_products_by_param(search_query: str, product_id: int = None, category_id: int = None) -> list or None:
    vector = inspect_search_vectors(Product)[0]
    try:
        result = db.session.query(Product).filter(
            Product.search_vector.match(search_query)
        )
    except exc.ProgrammingError:
        return None
    if product_id:
        result = result.filter_by(producer_id=product_id)
    if category_id:
        result = result.filter_by(category_id=category_id)
    return result.order_by(desc(func.ts_rank_cd(vector, func.tsq_parse(search_query))))


def search_by_keyword(search_key_word: str) -> list:
    """Returns all products mathced with key word"""
    search_query = '&'.join(search_key_word.split(' '))
    result = search_products_by_param(search_query)
    return product_schema_list.dump(result).data


def get_products_for_global_search(search_key_word: str) -> list:
    products = search_by_keyword(search_key_word)
    producers = Producer.query.all()
    # формат: {1: Совхоз А, 2: Совхоз Б}
    producer_id_name_mapping = {}
    for producer in producers:
        producer_id_name_mapping[producer.id] = producer.name
    # в продуктах добавляем producer_name
    for product in products:
        product['producer_name'] = producer_id_name_mapping[product['producer_id']]
    return products


def post_product(args: dict) -> Product:
    """Post product by given args"""
    abort_if_producer_doesnt_exist_or_get(args['producer_id'])
    abort_if_category_doesnt_exist_or_get(args['category_id'])
    new_product = product_schema.load(args).data
    db.session.add(new_product)
    producer = get_producer_by_id(args['producer_id'])
    category = get_category_by_id(args['category_id'])
    parent_category = get_category_by_id(category.parent_id)
    for category in (category, parent_category):
        if category not in producer.categories:
            producer.categories.append(category)
    db.session.commit()
    sitemap_tools.add_new_product_to_sitemap.apply_async((new_product.producer_id, new_product.id),
                                                         link=sitemap_tools.update_producer_info_in_global_sitemap.s())
    return new_product


def put_product(args: dict, product_id: int) -> Product:
    """Change product"""
    product = get_product_by_id(product_id)
    product_quantity_before = product.quantity
    if args['category_id']:
        args['category_id'] = Category.query.filter_by(slug=args['category_id']).first().id
        check_producer_categories(args['category_id'], product)
    args['id'] = None
    args['producer_id'] = None
    args['price'] = float("".join(args['price'].split()))
    for k, v in args.items():
        if v:
            setattr(product, k, v)
    db.session.commit()
    if 0 == product_quantity_before < product.quantity:
        notify_subscribers_about_products_supply(product)
    sitemap_tools.update_product_info_in_sitemap.apply_async((product.producer_id, product_id),
                                                             link=sitemap_tools.update_producer_info_in_global_sitemap.s())
    return product


def delete_product_by_id(product_id: int) -> dict:
    """Delete product"""
    product = get_product_by_id(product_id)
    delete_categories_if_it_was_the_last_product(product)
    db.session.delete(product)
    db.session.commit()
    sitemap_tools.delete_product_from_sitemap.apply_async((product.producer_id, product_id),
                                                          link=sitemap_tools.update_producer_info_in_global_sitemap.s())
    return {"message": "Product with id {} has been deleted successfully".format(product_id)}


def upload_product_image(product_id: int, image_data) -> bool:
    """Upload image for product"""
    product = get_product_by_id(product_id)
    producer_id = product.producer_id
    image_size = app.config['USER_IMAGE_PRODUCTS_SIZE']
    return upload_image(product, image_data, producer_id, image_size, product_id=product_id)


def get_formatted_rating(rating_value):
    stars = {'empty': 'img/star_empty.png',
             'half': 'img/star_half.png',
             'full': 'img/star.png'}
    rating = []
    rating_integer = int(rating_value)
    rating_fraction = rating_value % 1
    for i in range(rating_integer):
        rating.append(stars['full'])
    if 0.25 <= rating_fraction < 0.85:
        rating.append(stars['half'])
    for i in range(5 - len(rating)):
        rating.append(stars['empty'])
    return rating


def subscribe_consumer(product, consumer):
    product.subscribers.append(consumer)
    db.session.commit()


def notify_subscribers_about_products_supply(product):
    while any(product.subscribers):
        subscriber = product.subscribers.pop()
        product_url = url_for('product_card', product_id=product.id, _external=True)
        send_notify_about_products_supply(
            subscriber.email,
            subscriber.first_name,
            product_url,
            product.name
        )
    db.session.commit()
