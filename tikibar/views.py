from pyramid.view import view_config


@view_config(name='tikibar', renderer='templates/tikibar.pt')
def tikibar(context, request):
    addables = [
        ct for ct in request.registry['tikibar']['content_types'].values()
        if ct['add_view']]
    widgets = (
        widget(context, request) for widget in
        request.registry.get('tikibar_widgets', {}).values())
    return {
        'url': lambda p: request.static_url('tikibar:static/' + p),
        'widgets': widgets,
        'addables': addables,
    }
