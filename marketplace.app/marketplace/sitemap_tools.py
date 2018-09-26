from datetime import datetime

from flask import render_template

from marketplace import app, SITE_DOMAIN, celery
from marketplace.api_folder.utils import product_utils, producer_utils


@celery.task(name='sitemap_tools.update_global_sitemap')
def update_global_sitemap():
    pages = []
    cur_date = datetime.now()
    producers = producer_utils.get_all_producers()
    pages.append(['{}/static_sitemap.xml'.format(SITE_DOMAIN), cur_date])
    for producer in producers:
        pages.append(['{}/producer_sitemap{}.xml'.format(SITE_DOMAIN, producer.id), cur_date])
    sitemap_xml = render_template('global_sitemap.xml', pages=pages)
    with open('sitemap.xml', 'w+') as sitemap:
        sitemap.write(sitemap_xml)


@celery.task(name='sitemap_tools.update_static_sitemap')
def update_static_sitemap():
    pages = []
    cur_date = datetime.now()
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and not str(rule).startswith('/api/v1/') and len(rule.arguments) == 0:
            pages.append(['{}{}'.format(SITE_DOMAIN, rule), cur_date])
    static_sitemap = render_template('sitemap.xml', pages=pages)
    with open('static_sitemap.xml', 'w+') as sitemap:
        sitemap.write(static_sitemap)


@celery.task()
def create_producer_sitemap(producer_id):
    pages = []
    cur_date = datetime.now()
    pages.append(['{}/producer/{}'.format(SITE_DOMAIN, producer_id), cur_date])
    producer_sitemap = render_template('sitemap.xml', pages=pages)
    with open('producer_sitemap{}.xml'.format(producer_id), 'w+') as sitemap:
        sitemap.write(producer_sitemap)


@celery.task()
def update_producer_sitemap(producer_id):
    pages = []
    cur_date = datetime.now()
    pages.append(['{}/producer/{}'.format(SITE_DOMAIN, producer_id), cur_date])
    producer_products = product_utils.get_products_by_producer_id(producer_id)
    for product in producer_products:
        pages.append(['{}/products/{}'.format(SITE_DOMAIN, product.id), cur_date])
    producer_sitemap = render_template('sitemap.xml', pages=pages)
    with open('producer_sitemap{}.xml'.format(producer_id), 'w+') as sitemap:
        sitemap.write(producer_sitemap)
