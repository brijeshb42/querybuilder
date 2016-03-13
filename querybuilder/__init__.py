def get_normalized_func_name(func):
    func = func.upper()
    if func[-1] == '_':
        return func[:-1]
    return func


class _MetaField(type):

    """
    Maintain a single instance for same field name
    """

    instances = {}

    def __call__(cls, field_name):
        if field_name in _MetaField.instances:
            return _MetaField.instances[field_name]
        instance = type.__call__(cls, field_name)
        _MetaField.instances[field_name] = instance
        return instance


class Field(object):
    __metaclass__ = _MetaField
    _one_arg = ('eq', 'ne', 'gt', 'lt', 'ge', 'le')
    _two_arg = ('between',)
    _multi_arg = ('in_', 'contains_any', 'contains_all', 'contains')

    @staticmethod
    def __one_arg_func(method, field):
        def _func(*args):
            if len(args) != 1:
                raise ValueError(
                    '{} accepts only one argument.'.format(method))
            return '{}("{}", {})'.format(
                get_normalized_func_name(method),
                field, args[0])
        return _func

    @staticmethod
    def __two_arg_func(method, field):
        def _func(*args):
            if len(args) != 2:
                raise ValueError(
                    '{} accepts two arguments, {} given.'.format(
                        method, len(args)))
            return '{}("{}", {})'.format(
                get_normalized_func_name(method),
                field, ", ".join([str(arg) for arg in args]))
        return _func

    @staticmethod
    def __multi_arg_func(method, field):
        def _func(*args):
            if len(args) < 1:
                raise ValueError('No arguments given')
            return '{}("{}", {})'.format(
                get_normalized_func_name(method),
                field, ", ".join([str(arg) for arg in args]))
        return _func

    def __getattr__(self, attr):
        if attr in Field._one_arg:
            return Field.__one_arg_func(attr, self.field)
        elif attr in Field._two_arg:
            return Field.__two_arg_func(attr, self.field)
        elif attr in Field._multi_arg:
            return Field.__multi_arg_func(attr, self.field)
        else:
            raise AttributeError('{} not found'.format(attr))

    def __init__(self, field):
        self.field = field

    def __eq__(self, rhs):
        return self.eq(rhs)

    def __ne__(self, rhs):
        return self.ne(rhs)

    def __lt__(self, rhs):
        return self.lt(rhs)

    def __le__(self, rhs):
        return self.le(rhs)

    def __gt__(self, rhs):
        return self.gt(rhs)

    def __ge__(self, rhs):
        return self.ge(rhs)

    def __lshift__(self, rhs):
        return self.in_(*rhs)


def AND(*args):
    if len(args) < 1:
        raise ValueError('AND accepts more than Zero argumnets')
    return "AND({})".format(", ".join(args))


def OR(*args):
    if len(args) < 1:
        raise ValueError('AND accepts more than Zero argumnets')
    return "OR({})".format(", ".join(args))
