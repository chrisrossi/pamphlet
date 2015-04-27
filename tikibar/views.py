from pyramid.view import view_config


@view_config(name='tikibar', renderer='templates/tikibar.pt')
def tikibar(context, request):
    widgets = (
        widget(context, request) for widget in
        request.registry.get('tikibar_widgets', {}).values())
    return {
        'url': lambda p: request.static_url('tikibar:static/' + p),
        'widgets': widgets,
    }
