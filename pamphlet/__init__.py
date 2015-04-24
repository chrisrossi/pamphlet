import acidfs
import dumpling

from pyramid.view import view_config


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


def includeme(config):
    config.set_root_factory(root_finder())
    config.scan('.')
