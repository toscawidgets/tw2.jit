import tw2.core as twc
from tw2.core.resources import JSSymbol

from tw2.jit.widgets.ajax import AjaxRadialGraph

# Used for doing ajax stuff
import tw2.jquery

class SQLARadialGraph(AjaxRadialGraph):
    """ A radial graph built automatically from sqlalchemy objects """

    entity = twc.Param("sqlalchemy class to which this graph is mapped",
                      request_local=False)

    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        print "HALLO"

        import pprint
        pprint.pprint(req.params)
        print "-"*40
        if 'key' not in req.params:
            key = u'1'
        else:
            key = req.params['key'].split('___')[-1]
    
        key = int(key)

        get_pkey = lambda ent : ent.__mapper__.primary_key[0].key
        pkey = get_pkey(cls.entity)

        obj = cls.entity.query.filter_by(**{pkey:key}).one()
        props = dict([(k, getattr(obj, k)) for k in obj.__mapper__.columns.keys()])

        make_node_from_property = lambda key, value : {
            'id' : "%s___%s" % (key, value),
            'name' : "%s -> %s" % (key, value),
            'data' : {}, 'children' : []
        }

        make_node_from_object = lambda obj : {
            'id' : "%s___%s" % (
                type(obj).__name__, get_pkey(type(obj))),
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

