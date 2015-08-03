from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('newgrid', '/')
    config.add_route('newgrid_json', 'newgrid.json')
    config.add_route('playgrid', '/')
    config.add_route('playgrid_json', 'playgrid.json')
    config.add_static_view(name='static', path='minesweeper:static')
    config.scan('.views')
    return config.make_wsgi_app()
