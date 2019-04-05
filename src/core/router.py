from controllers import auth
import aiohttp_cors


def routes(app):
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_methods=("*"),
            allow_credentials=True,
            expose_headers=("*",),
            allow_headers=("*"),
            max_age=3600,
        )
    })

    cors.add(app.router.add_get('/oauth/{type}', auth.oauth))
