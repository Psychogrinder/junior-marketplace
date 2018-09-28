import os
from datetime import datetime

from flask import render_template
import xml.etree.ElementTree as ET

from marketplace import app, SITE_DOMAIN, celery, FIND_IN_XML_PREFIX, DEFAULT_XML_NAMESPACE
from marketplace.api_folder.utils import product_utils


@celery.task()
def add_producer_to_global_sitemap(producer_id):
    if not os.path.isfile('sitemap.xml'):
        init_global_sitemap()
    path = 'sitemap.xml'
    producer_path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, False)
        tree.getroot().append(build_new_xml_elem('{}/{}'.format(SITE_DOMAIN, producer_path), cur_date, 'sitemap'))
        tree.write(path)


@celery.task()
def update_producer_info_in_global_sitemap(producer_id):
    path = 'sitemap.xml'
    producer_path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, False)
        update_xml_elem_date(tree.getroot(), '{}/{}'.format(SITE_DOMAIN, producer_path), cur_date)
        tree.write(path)


@celery.task()
def delete_producer_from_global_sitemap(producer_id):
    path = 'sitemap.xml'
    producer_path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, False)
        tree.getroot().remove(
            find_xml_elem_with_given_loc_value(tree.getroot(), '{}/{}'.format(SITE_DOMAIN, producer_path)))
        tree.write(path)


def init_global_sitemap():
    pages = []
    if os.path.isfile('static_sitemap.xml'):
        static_mod_data = get_modification_date('static_sitemap.xml')
        pages.append(['{}/static_sitemap.xml'.format(SITE_DOMAIN), static_mod_data])
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


@celery.task()
def add_new_product_to_sitemap(producer_id, product_id):
    path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, True)
        tree.getroot().append(build_new_xml_elem('{}/products/{}'.format(SITE_DOMAIN, product_id), cur_date, 'url'))
        tree.write(path)


@celery.task()
def delete_product_from_sitemap(producer_id, product_id):
    path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, True)
        tree.getroot().remove(
            find_xml_elem_with_given_loc_value(tree.getroot(), '{}/products/{}'.format(SITE_DOMAIN, product_id)))
        tree.write(path)


@celery.task()
def update_product_info_in_sitemap(producer_id, product_id):
    path = 'producer_sitemap{}.xml'.format(producer_id)
    if os.path.isfile(path):
        tree, cur_date = init_tree_and_update_date(path, True)
        update_xml_elem_date(tree.getroot(), '{}/products/{}'.format(SITE_DOMAIN, product_id), cur_date)
        tree.write(path)


def init_tree_and_update_date(path, need_update_date):
    ET.register_namespace('', DEFAULT_XML_NAMESPACE)
    tree = ET.parse(path)
    root = tree.getroot()
    cur_date = str(datetime.now())
    if need_update_date:
        update_sitemap_time(root, cur_date)
    return tree, cur_date


def update_xml_elem_date(root, loc, date):
    for elem in root:
        cur_loc = elem.find(
            '{}loc'.format(FIND_IN_XML_PREFIX)).text
        if cur_loc == loc:
            mod_date = elem.find('{}lastmod'.format(FIND_IN_XML_PREFIX))
            mod_date.text = date
            return


def update_sitemap_time(root, date):
    sitemap_agent = get_first_elem_lastmod_tag(root)
    sitemap_agent.text = date


def get_modification_date(path):
    tree = ET.parse(path)
    root = tree.getroot()
    mod_date = root.find('{}url'.format(FIND_IN_XML_PREFIX)).find(
        '{}lastmod'.format(FIND_IN_XML_PREFIX)).text
    return mod_date


def get_first_elem_lastmod_tag(root):
    return root.find('{}url'.format(FIND_IN_XML_PREFIX)).find(
        '{}lastmod'.format(FIND_IN_XML_PREFIX))


def build_new_xml_elem(tag_text, date, main_tag):
    url_elem = ET.Element(main_tag)
    loc = ET.SubElement(url_elem, 'loc')
    lastmod = ET.SubElement(url_elem, 'lastmod')
    loc.text = tag_text
    lastmod.text = date
    return url_elem


def find_xml_elem_with_given_loc_value(root, loc):
    for elem in root:
        cur_loc = elem.find(
            '{}loc'.format(FIND_IN_XML_PREFIX)).text
        if cur_loc == loc:
            return elem
