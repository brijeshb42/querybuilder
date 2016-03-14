import operator


def in_(lhs, rhs):
    return lhs << (rhs)


def between_(lhs, rhs):
    start = rhs[0]
    end = rhs[1]
    return lhs.between(start, end)


def contains_(lhs, rhs):
    return lhs.contains(rhs)


def contains_any_(lhs, rhs):
    return lhs.contains_any(rhs)


def contains_all_(lhs, rhs):
    return lhs.contains_all(rhs)


def startswith_(lhs, rhs):
    return lhs.startswith(rhs)


OPERATORS = {
    'EQ': operator.eq,
    'NE': operator.ne,
    'GT': operator.gt,
    'GE': operator.ge,
    'LT': operator.lt,
    'LE': operator.le,
    'CONTAINS': contains_,
    'CONTAINS_ANY': contains_any_,
    'CONTAINS_ALL': contains_all_,
    'STARTSWITH': startswith_,
    'IN': in_,
    'BETWEEN': between_
}

MULTI_VALUE = ('IN', 'BETWEEN', 'CONTAINS_ANY', 'CONTAINS_ALL')

GROUP = {
    'AND': operator.and_,
    'OR': operator.or_
}


def travel_node(query, Model, operators):
    for key in query:
        if key in GROUP:
            exp = []
            for arg in query[key]:
                exp.append(travel_node(arg, Model, operators))
            return reduce(GROUP[key], exp)
        elif key in operators:
            op = operators[key]
            for key1, val in query[key].iteritems():
                field = Model._meta.fields[key1]
                value = val
                break
            return op(field, value)


def get_expression_for(Model, query, operators=None):
    if operators:
        OPERATORS.update(operators)
    return travel_node(query, Model, OPERATORS)
