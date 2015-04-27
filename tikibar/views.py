from pyramid.view import view_config


@view_config(name='tikibar', renderer='templates/tikibar.pt')
def tikibar(context, request):
    return {
        'url': lambda p: request.static_url('tikibar:static/' + p),
    }
