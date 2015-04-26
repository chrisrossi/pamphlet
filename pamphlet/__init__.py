import base64
import re

from pyramid.renderers import render_to_response


BODY = re.compile('<body([^>]*)>')
TITLE = re.compile('<title>(.*)</title>', flags=re.I)


def pamphlet_tween_factory(handler, registry):
    def pamphlet_tween(request):
        response = handler(request)
        if response.status_int == 200 and response.content_type == 'text/html':
            onload = (' onload="parent.postMessage('
                      'document.body.scrollHeight, \'%s\');"' %
                      request.url)
            text = BODY.sub(
                lambda m: '<body%s%s>'% (m.groups()[0], onload),
                response.text).encode('utf8')
            title = TITLE.search(response.text)
            title = title.groups()[0] if title else ''
            def url(path):
                return request.static_url('pamphlet:static/' + path)
            return render_to_response(
                'templates/contentbar.pt',
                {'contentsrc': 'data:text/html;charset=utf8;base64,' +
                               str(base64.b64encode(text), 'utf8'),
                 'title': title,
                 'url': url},
                request=request,
                response=response)
        return response
    return pamphlet_tween


def includeme(config):
    config.add_tween('pamphlet.pamphlet_tween_factory')
    config.add_static_view('pamphlet-static', 'pamphlet:static')
