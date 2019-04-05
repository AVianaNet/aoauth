from views import render
from core.conf import *
from aioauth_client import (
    BitbucketClient,
    FacebookClient,
    GithubClient,
    GoogleClient,
    OAuth1Client,
    TwitterClient,
    YandexClient,
)
from aiohttp import web

clients = {
    'google': {
        'class': GoogleClient,
        'init': {
            'client_id': GOOGLE['client_id'],
            'client_secret': GOOGLE['client_secret'],
            'scope': GOOGLE['scope'],
        },
    },
    'facebook': {
        'class': FacebookClient,
        'init': {
            'client_id': FACEBOOK['client_id'],
            'client_secret': FACEBOOK['client_secret'],
            'scope': FACEBOOK['scope']
        },
    },
    'twitter': {
        'class': TwitterClient,
        'init': {
            'consumer_key': TWITTER['consumer_key'],
            'consumer_secret': TWITTER['consumer_secret'],
        },
    },
    'github': {
        'class': GithubClient,
        'init': {
            'client_id': GITHUB['client_id'],
            'client_secret': GITHUB['client_secret'],
        },
    },
    'bitbucket': {
        'class': BitbucketClient,
        'init': {
            'consumer_key': BITBUCKET['consumer_key'],
            'consumer_secret': BITBUCKET['consumer_secret'],
        },
    },
    'yandex': {
        'class': YandexClient,
        'init': {
            'client_id': YANDEX['client_id'],
            'client_secret': YANDEX['client_secret'],
        },
    },
}


async def oauth(request):

    try:
        provider = request.match_info.get('type')
        if provider not in clients:
            return await render.json({'error': 'Invalid oauth provider'}, 500)

        client_class = clients[provider]['class']
        params = clients[provider]['init']
        client = client_class(**params)
        client.params['oauth_callback' if issubclass(client_class, OAuth1Client) else 'redirect_uri'] = \
            'http://%s%s' % (request.host, request.path)

        if client.shared_key not in request.query:

            if isinstance(client, OAuth1Client):
                token, secret, _ = await client.get_request_token()

                request.app.secret = secret
                request.app.token = token

            return web.HTTPFound(client.get_authorize_url(access_type='offline'))

        if isinstance(client, OAuth1Client):
            client.oauth_token_secret = request.app.secret
            client.oauth_token = request.app.token

        _, meta = await client.get_access_token(request.query)
        user, info = await client.user_info()
        response = {'user': user, 'info': info}
        status = 200
    except Exception as e:
        print(e)
        response = {'error': e}
        status = 500

    return await render.json(response, status)
