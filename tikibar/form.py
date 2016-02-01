from kemmering import (
    bind,
    defer,
    in_context,
    format_context,
    html,
    tag,
    text)

_nodefault = object()


class form(tag):
    fields = ()

    def __init__(self, name, title, action=None, method='POST'):
        super(form, self).__init__(
            'form',
            role='form',
            action=action,
            method=method)
        self.name = name
        self.title = title

    def __call__(self, *children):
        super(form, self).__call__(
            html.h1()(self.title),
            *children
        )
        self.fields = tuple(
            x for x in depth_first(self)
            if isinstance(x, field))
        return self

    def validate(self, params):
        return tuple(
            (field.name, params[field.name])
            for field in self.fields)

    def _copy(self, attrs, children):
        obj = super(form, self)._copy(attrs, children)
        obj.name = self.name
        obj.title = self.title
        obj.fields = self.fields
        return obj


class field(tag):

    def __init__(self, name, widget, required=False, validator=None,
                 title=None, description=''):
        if not title:
            title = name.title()
        self.name = name
        self.widget = widget
        self.required = required
        self.validator = validator
        self.title = title
        self.description = description

        self.id = id = 'input-' + name

        super(field, self).__init__('div', class_='form-group')
        self(
            html.label(for_=id)(title),
            widget(self),
        )
        if description:
            self(html.p(class_='help-block')(description),)

    def _copy(self, attrs, children):
        obj = super(field, self)._copy(attrs, children)
        obj.name = self.name
        obj.widget = self.widget
        obj.required = self.required
        obj.validator = self.validator
        obj.title = self.title
        obj.description = self.description
        obj.id = self.id
        return obj


def text_widget(field):
    return html.input(
        type_='text',
        class_='form-control',
        name=field.name,
        id=field.id,
        value=in_context(['data', field.name], None),
    )


def textarea_widget(field, rows=5):
    return html.textarea(
        class_='form-control',
        name_=field.name,
        id=field.id,
        rows=rows,
    )(in_context(['data', field.name], ''))


class content_form(object):

    def __init__(self, content_type, *fields):
        self.content_type = content_type
        self.fields = fields

        form_fields = fields + (
            html.button(
                type_='submit',
                class_='btn btn-default')('Save'),
        )

        @defer
        def title(context):
            return text('%s %s' % (
                context['action'].title(),
                context['content_type']['name']))

        self.form = form(format_context('{action}-page'), title)(*form_fields)

    def edit_form(self, instance):
        data = {
            field.name: getattr(instance, field.name, '')
            for field in self.fields
        }
        return HTML(bind(self.form, {
            'action': 'edit',
            'content_type': self.content_type,
            'data': data,
        }))

    def add_form(self):
        return HTML(bind(self.form, {
            'action': 'add',
            'content_type': self.content_type,
            'data': {}
        }))

    def validate(self, params):
        return self.form.validate(params)


def depth_first(tree):
    for x in getattr(tree, 'children', ()):
        for y in depth_first(x):
            yield y
    yield tree


def root(x):
    while x.parent:
        x = x.parent
    return x


def interleave(*seqs):
    iters = [iter(seq) for seq in seqs]
    while iters:
        i = iters.pop(0)
        try:
            yield next(i)
            iters.append(i)
        except StopIteration:
            pass


class HTML(str):

    def __html__(self):
        return self
