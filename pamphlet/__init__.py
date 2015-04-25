import acidfs
import base64
import dumpling
import re

from pyramid.renderers import render_to_response


@dumpling.folder
class Page(object):
    title = dumpling.Field()
    body = dumpling.Field()


@dumpling.folder
class HomePage(Page):
    pass


def root_finder(root_folder_factory=HomePage):
    def factory(request):
        settings = request.registry.settings
        fs = acidfs.AcidFS(settings['pamphlet.repo'])
        return dumpling.Store(fs, root_folder_factory).root()
    return factory


BODY = re.compile('<body([^>]*)>')

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
            return render_to_response(
                'templates/contentbar.pt',
                {'contentsrc': 'data:text/html;charset=utf8;base64,' +
                               str(base64.b64encode(text), 'utf8')},
                request=request,
                response=response)
        return response
    return pamphlet_tween


def includeme(config):
    config.set_root_factory(root_finder())
    config.add_tween('pamphlet.pamphlet_tween_factory')
    config.scan('.')
