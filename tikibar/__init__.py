from pyramid.renderers import render
from pyramid.view import view_config


def tikibar_tween_factory(handler, registry):
    def tikibar_tween(request):
        response = handler(request)
        conditions = (
            response.status_int == 200,
            response.content_type == 'text/html',
            request.view_name != 'contentbar',
        )
        if all(conditions):
            snippet = render('templates/inject.pt', {
                'contentbar_url': request.resource_url(
                    request.context, '@@contentbar')})
            response.text = ireplace(
                response.text, '</body>', snippet + '</body>')
        return response
    return tikibar_tween


def ireplace(s, x, y):
    """
    Case insensitively replace `x` with `y` in string `s`.
    """
    l = s.lower().find(x.lower())
    if l == -1:
        return s
    return s[:l] + y + s[l + len(x):]


@view_config(name='contentbar', renderer='templates/contentbar.pt')
def contentbar(context, request):
    return {
        'url': lambda p: request.static_url('tikibar:static/' + p),
    }


def includeme(config):
    config.add_tween('tikibar.tikibar_tween_factory')
    config.add_static_view('tikibar-static', 'tikibar:static')
    config.scan()
