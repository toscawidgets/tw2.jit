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

    # TBD -- show_relations?
    # TBD -- show_attributes?

    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        ATTR_STR = "__attr__"
        SEP = '___'

        import pprint
        print "HALLO"
        pprint.pprint(req.params)
        print "-"*40

        if 'key' not in req.params:
            entkey, key = 'Person', 1
        else:
            toks = req.params['key'].split(SEP)
            entkey, key = toks[-2:]

        key = int(key)

        get_pkey = lambda ent : ent.__mapper__.primary_key[0].key
        entity = filter(lambda x : x.__name__ == entkey, cls.entities)[0]
        pkey = get_pkey(entity)

        obj = entity.query.filter_by(**{pkey:key}).one()
        props = dict([(p.key, getattr(obj, p.key)) for p in obj.__mapper__.iterate_properties])

        # TBD -- is this necessary?
        del props[pkey]

        def safe_id(s):
            return s.replace(' ', '_').replace('#', '___')

        def make_node_from_property(prefix, key, value, depth):

            if type(value) != sqlalchemy.orm.collections.InstrumentedList:
                node_id = SEP.join([prefix, key, value])
                name = "%s:<br/>%s" % (key, value),
                children = []
            else:
                node_id = SEP.join([prefix, key, str(uuid.uuid4())])
                name = key
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
                children = [make_node_from_property(prefix, k, v, depth+1) for k, v in props.iteritems()]
            return {
                'id' : node_id,
                'name' : "%s: %s" % (
                    tw2.core.util.name2label(type(obj).__name__), unicode(obj)),
                'children' : children,
                'data' : {},
            }

        json = make_node_from_object(obj, 0)

        import pprint
        pprint.pprint(json)
        return json

