import re

from pyramid.view import view_config, view_defaults

from .security import TIKI_MANAGE


@view_config(
    name='tikibar',
    permission=TIKI_MANAGE,
    renderer='templates/tikibar.pt')
def tikibar(context, request):
    addables = [
        ct for ct in request.registry['tikibar']['content_types'].values()]
    widgets = [
        widget(context, request) for widget in
        request.registry['tikibar']['widgets'].values()]
    ct = request.tikibar_content_type
    return {
        'url': lambda p: request.static_url('tikibar:static/' + p),
        'widgets': widgets,
        'addables': addables,
    }


@view_defaults(
    name='tikibar-add-instance',
    permission=TIKI_MANAGE,
)
class AddInstanceViews(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

        ct_name = request.params['content_type']
        cts = request.registry['tikibar']['content_types']
        self.content_type = cts[ct_name]

    @view_config(request_method='GET', renderer='html')
    def get(self):
        return self.content_type['form'].add_form()

    @view_config(request_method='POST', renderer='json')
    def post(self):
        request = self.request
        ct = self.content_type
        factory = ct['factory']
        kw = dict(ct['form'].validate(request.POST))
        instance = factory(**kw)
        name = slug(instance.title)
        request.root[name] = instance
        return request.resource_url(instance)


@view_defaults(
    name='tikibar-edit',
    permission=TIKI_MANAGE,
)
class EditViews(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.content_type = request.tikibar_content_type

    @view_config(request_method='GET', renderer='html')
    def get(self):
        return self.content_type['form'].edit_form(self.context)

    @view_config(request_method='POST', renderer='json')
    def post(self):
        context = self.context
        request = self.request
        ct = self.content_type
        kw = dict(ct['form'].validate(request.POST))
        for name, value in kw.items():
            setattr(context, name, value)
        return request.resource_url(context)


def html_renderer_factory(info):
    def html_renderer(value, system):
        system['request'].response.content_type = 'text/html'
        return value
    return html_renderer


_nonwords = re.compile('[^\w]')


def slug(s):
    return '-'.join(map(str.lower, filter(None, _nonwords.split(s))))
