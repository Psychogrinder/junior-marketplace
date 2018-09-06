import string

from sqlalchemy import desc, func, exc
from sqlalchemy_searchable import inspect_search_vectors

from marketplace import db, app
from marketplace.api_folder.schemas import product_schema
from marketplace.api_folder.utils.abortions import abort_if_product_doesnt_exist_or_get, \
    abort_if_producer_doesnt_exist_or_get, abort_if_category_doesnt_exist_or_get
from marketplace.api_folder.utils.category_utils import get_category_by_id, get_subcategories_by_category_id, \
    check_producer_categories, delete_categories_if_it_was_the_last_product
from marketplace.api_folder.utils.order_utils import get_order_by_id
from marketplace.api_folder.utils.producer_utils import get_producer_by_id
from marketplace.api_folder.utils.uploaders import upload_image
from marketplace.models import Product, Producer, Category


def get_product_by_id(product_id):
    return abort_if_product_doesnt_exist_or_get(product_id)


def get_products_by_category_id(category_id):
    category = get_category_by_id(category_id)
    if category.parent_id != 0:
        return category.get_products()
    else:
        subcategories = get_subcategories_by_category_id(category_id)
        divided_products = [subcategory.get_products() for subcategory in subcategories]
        return [product for subcategory in divided_products for product in subcategory]


def get_products_by_producer_id(producer_id):
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Product.query.filter_by(producer_id=producer_id).all()


def get_all_products_from_a_list_of_categories(categories):
    all_products = []
    for category in categories:
        all_products += category.get_products()
    return all_products


def get_products_from_a_parent_category(parent_category_id):
    subcategories = get_subcategories_by_category_id(parent_category_id)
    return get_all_products_from_a_list_of_categories(subcategories)


def get_sorted_and_filtered_products(args):
    query = db.session.query(Product.id, Product.name, Product.price, Product.photo_url,
                             Producer.name.label('producer_name')).filter(
        Product.producer_id == Producer.id)

    if args['popularity']:
        if args['popularity'] == 'down':
            query = query.order_by(Product.times_ordered.desc())

    if args['producer_name']:
        query = query.filter(Producer.name == args['producer_name'])

    if args['in_stock'] == 1:
        query = query.filter(Product.quantity > 0)

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

    product_schema = ("id", "name", "price", "photo_url", "producer_name")
    products_data = query.all()
    products = []
    for product_data in products_data:
        products.append(dict(zip(product_schema, product_data)))
    return products


def get_popular_products():
    return Product.query.order_by(Product.times_ordered.desc()).limit(12).all()


def get_popular_products_by_category_id(category_id, direction):
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


def get_products_by_category_id_sorted_by_price(category_id, direction):
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


def get_all_products_from_order(order_id):
    order_items = get_order_by_id(order_id).order_items_json
    products = []
    for item in order_items:
        products.append(Product.query.filter_by(id=int(item)).first())
    return products


def get_all_products():
    return Product.query.all()


def producer_has_product_with_such_name(args):
    if Product.query.filter_by(producer_id=args['producer_id']).filter_by(name=args['name']).first():
        return True


def search_products_by_param(search_query):
    vector = inspect_search_vectors(Product)[0]
    try:
        result = db.session.query(Product).filter(
            Product.search_vector.match(search_query)
        ).order_by(desc(func.ts_rank_cd(vector, func.tsq_parse(search_query)))).all()
    except exc.ProgrammingError:
        return None
    return result


def post_product(args):
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
    return new_product


def put_product(args, product_id):
    product = get_product_by_id(product_id)

    if args['category_id']:
        args['category_id'] = Category.query.filter_by(slug=args['category_id']).first().id
        check_producer_categories(args['category_id'], product)
    args['id'] = None
    args['producer_id'] = None
    for k, v in args.items():
        if v:
            setattr(product, k, v)
    db.session.commit()
    return product


def delete_product_by_id(product_id):
    product = get_product_by_id(product_id)
    delete_categories_if_it_was_the_last_product(product)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product with id {} has been deleted successfully".format(product_id)}


def upload_product_image(product_id, files):
    product = get_product_by_id(product_id)
    producer_id = product.producer_id
    image_size = app.config['USER_IMAGE_PRODUCTS_SIZE']
    return upload_image(product, files, producer_id, image_size, product_id=product_id)
