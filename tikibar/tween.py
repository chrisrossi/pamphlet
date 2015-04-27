from pyramid.renderers import render


def tikibar_tween_factory(handler, registry):
    def tikibar_tween(request):
        response = handler(request)
        show_tiki_bar = (
            response.status_int == 200 and
            response.content_type == 'text/html' and
            request.view_name != 'tikibar'
        )
        if show_tiki_bar:
            snippet = render('templates/inject.pt', {
                'tikibar_url': request.resource_url(
                    request.context, '@@tikibar')})
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
