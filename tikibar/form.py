import re


_nodefault = object()


class tag(object):
    self_closing = False

    def __init__(self, tag, **attrs):
        if tag.endswith('/'):
            self.self_closing = True
            tag = tag[:-1]
        self.tag = tag
        self.attrs = {k: substitution(v) for k, v in attrs.items()}
        self.children = ()

    def __call__(self, *children):
        def mkchild(x):
            if isinstance(x, str):
                x = text_substitution(x)
            x.parent = self
            return x
        self.children = tuple(mkchild(x) for x in children)
        return self

    def __iter__(self):
        return iter(self.children)

    def render(self, context):
        return HTML(self.__str__(context))

    def __str__(self, context=None):
        return ''.join(self._stream(context))

    __html__ = __str__  # chameleon

    def __repr__(self):
        if self.self_closing and not self.children:
            return 'tag(%s)' % repr(self.tag + '/')

        if self.attrs:
            attrs = ', ' + ', '.join(
                ('%s=%s' % (k, repr(v)) for k, v in self.attrs.items())
            )
        else:
            attrs = ''

        children = ('(%s)' % ', '.join(map(repr, self.children))
                    if self.children else '')
        return 'tag(%s%s)%s' % (repr(self.tag), attrs, children)

    def _stream(self, context):
        attrs = {k: _maybe_call(v, context) for k, v in self.attrs.items()}
        if attrs:
            attrs = ' ' + ' '.join(
                ('%s="%s"' % (k.lstrip('_'), v) for k, v in attrs.items())
            )
        else:
            attrs = ''

        if self.self_closing and not self.children:
            yield '<%s%s/>' % (self.tag, attrs)
            return

        yield '<%s%s>' % (self.tag, attrs)
        for child in self.children:
            for x in _maybe_call(child, context)._stream(context):
                yield x
        yield '</%s>' % self.tag


def _maybe_call(f, context):
    if callable(f) and not isinstance(f, tag):
        return f(context)
    return f


class text(str):

    def _stream(self, context):
        yield self


def text_substitution(s):
    x = substitution(s)
    if callable(x):
        def callx(context):
            s = x(context)
            return text(s) if s is not None else None
        return callx
    return text(s)


_subpat = re.compile(r'\${([^}]+)}')


def substitution(s):
    if not isinstance(s, str):
        return s

    toks = _subpat.split(s)
    if len(toks) == 1:
        return s

    def mksub(name):
        pipe = name.rfind('|')
        if pipe == -1:
            name, default = name, _nodefault
        else:
            name, default = name[:pipe], name[pipe + 1:]
        path = name.split()

        def sub(context):
            value = context
            for name in path:
                try:
                    value = value[name]
                except KeyError:
                    value = default
                    break
            if value is _nodefault:
                raise KeyError(name, value)
            return value

        return sub

    if len(toks) == 3 and not (toks[0] or toks[2]):
        return mksub(toks[1])

    literals = toks[::2]
    subs = [mksub(tok) for tok in toks[1::2]]

    def sub(context):
        return ''.join(
            interleave(literals, (f(context) for f in subs))
        )

    return sub


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
            tag('h1')(self.title),
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

        super(field, self).__init__('div', _class='form-group')
        html = (
            tag('label', _for=id)(title),
            widget(self),
        )
        if description:
            html += (tag('p', _class='help-block')(description),)
        self(*html)


def text_widget(field):
    return tag(
        'input/',
        _type='text',
        _class='form-control',
        _name=field.name,
        id=field.id,
        value='${context %s|}' % field.name,
    )


def textarea_widget(field, rows=5):
    return tag(
        'textarea',
        _class='form-control',
        _name=field.name,
        id=field.id,
        rows=rows,
    )('${context %s|}' % field.name)


class content_form(object):

    def __init__(self, content_type, *fields):
        self.content_type = content_type
        self.fields = fields

        form_fields = fields + (
            tag('button',
                _type='submit',
                _class='btn btn-default')('Save'),
        )

        def title(context):
            return text('%s %s' % (
                context['action'].title(),
                context['content_type']['name']))

        self.form = form('${action}-page', title)(*form_fields)

    def edit_form(self, instance):
        context = {
            field.name: getattr(instance, field.name, '')
            for field in self.fields
        }
        return self.form.render({
            'action': 'edit',
            'content_type': self.content_type,
            'context': context,
        })

    def add_form(self):
        return self.form.render({
            'action': 'add',
            'content_type': self.content_type,
            'context': {}
        })

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

