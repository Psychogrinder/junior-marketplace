from marketplace.api_folder.utils.abortions import abort_if_category_doesnt_exist_or_get, \
    abort_if_category_doesnt_exist_slug_or_get
from marketplace.api_folder.utils.producer_utils import get_producer_by_id
from marketplace.models import Category, Producer, Product


def get_category_by_id(category_id):
    return abort_if_category_doesnt_exist_or_get(category_id)


def get_subcategories_by_category_id(category_id):
    abort_if_category_doesnt_exist_or_get(category_id)
    return Category.query.filter_by(parent_id=category_id).all()


def get_subcategories_by_category_slug(category_slug):
    abort_if_category_doesnt_exist_slug_or_get(category_slug)
    category_id = Category.query.filter_by(slug=category_slug).first().id
    return Category.query.filter_by(parent_id=category_id).all()


def get_parent_category_by_category_id(category_id):
    parent_category_id = Category.query.filter_by(id=category_id).first().parent_id
    return get_category_by_id(parent_category_id)


def get_category_by_name(slug):
    return Category.query.filter_by(slug=slug).first()


def get_category_names_by_producer_name(producer_name):
    return [category.name for category in Producer.query.filter_by(name=producer_name).first().categories]


def get_subcategory_names_by_parent_category_slug_and_producer_name(parent_category_slug, producer_name):
    subcategories = get_subcategories_by_category_id(Category.query.filter_by(slug=parent_category_slug).first().id)
    all_producer_category_names = [category.name for category in
                                   Producer.query.filter_by(name=producer_name).first().categories]
    return [category.name for category in subcategories if category.name in all_producer_category_names]


def get_all_base_categories():
    return Category.query.filter_by(parent_id=0).all()


def delete_categories_if_it_was_the_last_product(product):
    quantity_of_products_with_this_category = len(Product.query.filter_by(producer_id=product.producer_id).filter_by(
        category_id=product.category_id).all())
    if quantity_of_products_with_this_category == 1:
        category = get_category_by_id(product.category_id)
        producer = get_producer_by_id(product.producer_id)
        producer.categories.remove(category)
        subcategories = get_subcategories_by_category_id(category.parent_id)
        has_such_categories = False
        for cat in subcategories:
            if cat in producer.categories:
                has_such_categories = True
                break
        if not has_such_categories:
            parent_category = get_category_by_id(category.parent_id)
            producer.categories.remove(parent_category)


def add_product_categories_if_producer_doesnt_have_them(product, new_category_id):
    producer = get_producer_by_id(product.producer_id)
    category = get_category_by_id(new_category_id)
    parent_category = get_category_by_id(category.parent_id)
    for category in (category, parent_category):
        if category not in producer.categories:
            producer.categories.append(category)


def check_producer_categories(new_category_id, product):
    if product.category_id != int(new_category_id):
        delete_categories_if_it_was_the_last_product(product)
        add_product_categories_if_producer_doesnt_have_them(product, new_category_id)
