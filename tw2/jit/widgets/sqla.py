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

    show_relations = twc.Param("(bool) show relationships?", default=True)
    show_attributes = twc.Param("(bool) show attributes?", default=True)

    depth = twc.Param("(int) number of levels of relations to show.", default=3)


    # TODO -- prefixes are all messed up and we are left with weird orphan node


    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        SEP = '___'
        get_pkey = lambda ent : ent.__mapper__.primary_key[0].key

        if 'key' not in req.params:
            entkey = cls.entities[0].__name__
            pkey = get_pkey(cls.entities[0])
            key = getattr(cls.entities[0].query.first(), pkey)
        else:
            toks = req.params['key'].split(SEP)
            entkey, key = toks[-2:]

        try:
            entity = filter(lambda x : x.__name__ == entkey, cls.entities)[0]
        except IndexError, e:
            raise ValueError, "No such sqla class '%s' in 'entities'." % entkey

        pkey = get_pkey(entity)

        obj = entity.query.filter_by(**{pkey:key}).one()

        def exclude_property(p):
            is_attribute = lambda x: type(x) is sqlalchemy.orm.properties.ColumnProperty
            is_relation = lambda x: type(x) is sqlalchemy.orm.properties.RelationshipProperty

            explicitly_excluded = p.key in cls.excluded_columns
            excluded_by_attribute = is_attribute(p) and not cls.show_attributes
            excluded_by_relation  = is_relation(p) and not cls.show_relations
            return explicitly_excluded or excluded_by_attribute or excluded_by_relation

        def safe_id(s):
            return s.replace(' ', '_').replace('#', '___')

        def make_node_from_property(prefix, parent, key, value, depth):
            node_id = safe_id(SEP.join([prefix, key, unicode(value)]))
            children = []
            if type(value) in cls.entities:
                result = make_node_from_object(value, depth, node_id)
                result['name'] = "%s:<br/>%s" % (key, result['name'])
                return result
            elif type(value) != sqlalchemy.orm.collections.InstrumentedList:
                name = "%s:<br/>%s" % (key, unicode(value)),
            else:
                node_id = SEP.join([prefix, key, unicode(uuid.uuid4())])
                name = "%s of %s (%i)" % (key, unicode(parent), len(value))
                if depth < cls.depth:
                    children = [make_node_from_object(o, depth+1, node_id) for o in value]

            node_id = safe_id(node_id)

            return {
                'id' : node_id, 'name' : name, 'children' : children, 'data' : {},
            }

        def make_node_from_object(obj, depth=0, prefix=''):
            node_id = safe_id(
                SEP.join([prefix, type(obj).__name__,
                          unicode(getattr(obj, get_pkey(type(obj))))]))
            prefix = node_id
            children = []
            if depth < cls.depth:
                props = dict([(p.key, getattr(obj, p.key))
                              for p in obj.__mapper__.iterate_properties
                              if not exclude_property(p) ])

                children = [make_node_from_property(prefix, obj, k, v, depth+1)
                            for k, v in props.iteritems()]

            data = getattr(obj, '__jit_data__', lambda : {})()

            return {
                'id' : node_id,
                'name' : "%s: %s" % (
                    tw2.core.util.name2label(type(obj).__name__), unicode(obj)),
                'children' : children,
                'data' : data,
            }

        json = make_node_from_object(obj)

        return json

