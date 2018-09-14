from urllib.error import HTTPError
from marketplace.models import Category, User, Product, Producer
from urllib.request import Request, urlopen
import requests, json

def parseViews(file='../views.py'):

    routes = {'auth': [],
              'not_auth': ['/category/<category_name>',
                           '/products/<product_id>',
                           '/producer/<producer_id>'
                           ],
              }

    with open(file) as f:
        for s in f:
            """ parsing classes of routes (keys) and routes:
                                seek first, last symbols in strings"""

            if '@app.route' in s:
                start, end = s.find('/'), s.rfind('\'')
                route = s[start:end]

                if route not in (routes['not_auth']):
                    if ('<' or '>' or 'products') not in route:
                        routes['not_auth'].append(route)
                    else:
                        routes['auth'].append(route)
    return routes


def parseRoutes(file='../api_routes.py'):
    routes = {'Orders': [],
              'Cart': [],
              'Authorization': [],
              'Upload': [],
              'Category': [],
              'Producers': [],
              'Consumers': [],
              'Products': [],
              'Password': [],
    }

    with open(file) as f:
        for s in f:

            if '#' in s:
                string = ''
                for char in s:
                    if char.isalpha():
                        string += char
                route_category = string

            if 'api.add_resource' in s:
                start, end = s.find('/'), s.rfind('\'')
                route = s[start:end]
                for key in routes:
                    if route_category == key:
                        routes[key].append(route)

    return routes

def getCategorySlugs(parent_id=0):
    category_slugs = []

    if parent_id == 0:
        categories = Category.query.filter_by(parent_id=0)
    else:
        categories = Category.query.all()

    for category in categories:
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

    if '<' and '>' in url:
        first_symbol, last_symblol = url.find('<'), url.rfind('>')

        if 'producer_id' in url:
            return url.replace(url[first_symbol:last_symblol + 1], str(user_id))

        elif 'user_id' in url:
            return url.replace(url[first_symbol:last_symblol + 1], str(user_id))


def getProductIds():
    product_ids = []
    for product_id in Product.query.all():
        product_ids.append(product_id.id)

    return product_ids


def replaceProductId(url, product_id):
    if 'product_id' in url:
        url = url.replace('<int:product_id>', str(product_id))
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


def getResponse(login_url, email, password):
    payload = {
        'email': email,
        'password': password
    }
    return requests.Session().post(login_url, data=payload, allow_redirects=False)


def getCookiesFromResponse(response):
    return response.cookies.get_dict()


def getUserIdFromResponse(response):
    return json.loads(response.content)['id']


def is_price_sorted(list, price_sort):
    if price_sort == 'up':
        return all(a <= b for a, b in zip(list, list[1:]))
    elif price_sort == 'down':
        return all(a >= b for a, b in zip(list, list[1:]))


def check_price(sorted, args_price):
    price_in_slug = []

    for product in sorted['products']:
        if ' ₽' in product['price']:
            price = product['price'][:-2]
        else:
            price = product['price']
        price_in_slug.append(float(price))

    if price_in_slug:
        return is_price_sorted(price_in_slug, args_price)
    else:
        return True
