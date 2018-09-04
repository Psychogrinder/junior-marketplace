from urllib.error import HTTPError
from marketplace.models import Category, User, Product, Producer
from urllib.request import Request, urlopen
import requests, json

def parseApiRoutes():
    file = '../views.py'
    routes = {'auth': [],
              'not_auth': ['/category/<category_name>',
                           '/products/<product_id>',
                           '/producer/<producer_id>'
                           ]
              }

    with open(file) as f:
        for s in f:
            """ parsing classes of routes (keys) and routes:
                                seek first, last symbols in strings"""
            if '@app.route' in s:
                first_symbol, last_symblol = s.find('/'), s.rfind('\'')
                route = s[first_symbol:last_symblol]

                if route not in (routes['not_auth'] and routes['not_auth']):
                    if ('<' or '>' or 'products') not in route:
                        routes['not_auth'].append(route)
                    else:
                        routes['auth'].append(route)
    return routes


def getCategorySlugs():
    category_slugs = []
    for category in Category.query.all():
        category_slugs.append(category.slug)

    return category_slugs


def replaceCategoryName(url, category_slug):
    if '<category_name>' in url:
        return url.replace('<category_name>', category_slug)


def getUserIds():
    user_ids = {'producer_ids': [], 'user_ids': [], 'count': 0}

    for user in User.query.all():
        if user.entity == 'producer':
            user_ids['producer_ids'].append(user.id)
        else:
            user_ids['user_ids'].append(user.id)
        user_ids['count'] += 1

    return user_ids #return dict with user ids


def replaceUserId(url, user_id):
    if '<producer_id>' in url:
        return url.replace('<producer_id>', str(user_id))
    elif '<user_id>' in url:
        return url.replace('<user_id>', str(user_id))


def getProductIds():
    product_ids = []
    for product_id in Product.query.all():
        product_ids.append(product_id.id)

    return product_ids


def replaceProductId(url, product_id):
    if '<product_id>' in url:
        return url.replace('<product_id>', str(product_id))
    else:
        return url

def getResponseCode(url):
    request = Request(url=url)
    try:
        response = urlopen(request).getcode()
    except HTTPError:
        response = None

    return response


def getCookie(login_url, email, password):
    payload = {
        'email': email,
        'password': password
    }
    s = requests.Session()
    response = s.post(login_url, data=payload, allow_redirects=False)

    return response.cookies.get_dict(), response


def getUserIdAndEntity(response):
    user = json.loads(response.content)
    return user['id'], user['entity']