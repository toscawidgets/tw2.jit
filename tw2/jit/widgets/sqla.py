import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.ajax import AjaxRadialGraph

# Used for doing ajax stuff
import tw2.jquery

import sqlalchemy
import uuid

class SQLARadialGraph(AjaxRadialGraph):
    """ A radial graph built automatically from sqlalchemy objects """

    entities = twc.Param(
        "sqlalchemy classes to which this graph is mapped",
        request_local=False)

    excluded_columns = twc.Param(
        "list of names of columns to be excluded from the visualization",
        default=[])

    # TBD -- show_relations?
    # TBD -- show_attributes?
    # TBD -- specified depth

    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        SEP = '___'

        if 'key' not in req.params:
            entkey, key = 'Person', 1
        else:
            toks = req.params['key'].split(SEP)
            entkey, key = toks[-2:]

        try:
            entity = filter(lambda x : x.__name__ == entkey, cls.entities)[0]
        except IndexError, e:
            raise ValueError, "No such sqla class '%s' in 'entities'." % entkey

        get_pkey = lambda ent : ent.__mapper__.primary_key[0].key
        pkey = get_pkey(entity)

        obj = entity.query.filter_by(**{pkey:key}).one()

        def safe_id(s):
            return s.replace(' ', '_').replace('#', '___')

        def make_node_from_property(prefix, parent, key, value, depth):
            if type(value) in cls.entities:
                result = make_node_from_object(value, depth, prefix)
                result['name'] = "%s:<br/>%s" % (key, result['name'])
                return result
            elif type(value) != sqlalchemy.orm.collections.InstrumentedList:
                node_id = SEP.join([prefix, key, unicode(value)])
                name = "%s:<br/>%s" % (key, unicode(value)),
                children = []
            else:
                node_id = SEP.join([prefix, key])
                name = "%s of %s (%i)" % (key, unicode(parent), len(value))
                children = [make_node_from_object(o, depth+1, node_id) for o in value]

            node_id = safe_id(node_id)

            return {
                'id' : node_id, 'name' : name, 'children' : children, 'data' : {},
            }

        def make_node_from_object(obj, depth, prefix=''):
            node_id = SEP.join([prefix, type(obj).__name__,
                                str(getattr(obj, get_pkey(type(obj))))])
            prefix = node_id
            children = []
            if depth < 2:
                props = dict([(p.key, getattr(obj, p.key))
                              for p in obj.__mapper__.iterate_properties
                              if not p.key in cls.excluded_columns
                             ])
                children = [make_node_from_property(prefix, obj, k, v, depth+1)
                            for k, v in props.iteritems()]

            data = getattr(obj, '__data__', lambda : {})()

            return {
                'id' : node_id,
                'name' : "%s: %s" % (
                    tw2.core.util.name2label(type(obj).__name__), unicode(obj)),
                'children' : children,
                'data' : data,
            }

        json = make_node_from_object(obj, 0)

        return json

