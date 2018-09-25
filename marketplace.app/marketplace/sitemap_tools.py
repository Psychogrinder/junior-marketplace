from datetime import datetime, timedelta

from flask import render_template

from marketplace import app, SITE_DOMAIN, celery
from marketplace.api_folder.utils import product_utils, producer_utils


@celery.task
def generate_sitemap():
    print('Start async sitemap ge')
    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            if not str(rule).startswith('/api/v1/'):
                if len(rule.arguments) == 0:
                    pages.append(
                        ['{}{}'.format(SITE_DOMAIN, rule), ten_days_ago]
                    )
                if str(rule) == '/producer/<int:producer_id>':
                    producers = producer_utils.get_all_producers()
                    for producer in producers:
                        pages.append(['{}/producer/{}'.format(SITE_DOMAIN, producer.id), ten_days_ago])
                if str(rule) == '/products/<int:product_id>':
                    products = product_utils.get_all_products()
                    for product in products:
                        pages.append(['{}/products/{}'.format(SITE_DOMAIN, product.id), ten_days_ago])
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    with open('sitemap.xml', 'w+') as sitemap:
        sitemap.write(sitemap_xml)
