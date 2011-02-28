import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.ajax import AjaxRadialGraph

# Used for doing ajax stuff
import tw2.jquery

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
        elif req.params['key'].startswith(ATTR_STR):
            # TODO how to handle this?
            raise ValueError, "TDB -- How to handle this?"
        else:
            entkey, key = req.params['key'].split(SEP)

        key = int(key)

        get_pkey = lambda ent : ent.__mapper__.primary_key[0].key
        entity = filter(lambda x : x.__name__ == entkey, cls.entities)[0]
        pkey = get_pkey(entity)

        obj = entity.query.filter_by(**{pkey:key}).one()
        props = dict([(k, getattr(obj, k)) for k in obj.__mapper__.columns.keys()])

        # TBD -- is this necessary?
        del props[pkey]

        make_node_from_property = lambda key, value : {
            'id' : "%s%s%s%s" % (ATTR_STR, key, SEP, value),
            'name' : "%s:<br/>%s" % (key, value),
            'data' : {}, 'children' : []
        }

        make_node_from_object = lambda obj : {
            'id' : "%s%s%s" % (
                type(obj).__name__, SEP, getattr(obj, get_pkey(type(obj)))),
            'name' : "%s: %s" % (
                tw2.core.util.name2label(type(obj).__name__), unicode(obj)),
            'children' : [
                make_node_from_property(k, v) for k, v in props.iteritems()],
            'data' : {},
        }

        json = make_node_from_object(obj)

        import pprint
        pprint.pprint(json)
        return json

