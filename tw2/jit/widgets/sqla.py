import tw2.core as twc
from tw2.core.resources import JSSymbol
from tw2.core.util import name2label

from tw2.jit.widgets.ajax import AjaxRadialGraph

# Used for doing ajax stuff
import tw2.jquery

import sqlalchemy as sa
import uuid
from itertools import product

SEP = '___'
ALPHA = 'ALPHA'
get_pkey = lambda ent : ent.__mapper__.primary_key[0].key

class SQLARadialGraph(AjaxRadialGraph):
    """ A radial graph built automatically from sqlalchemy objects """

    rootObject = twc.Param(
        "sqlalchemy mapped object to focus on when the graph first loads")

    entities = twc.Param(
        "sqlalchemy classes to which this graph is mapped",
        request_local=False)

    excluded_columns = twc.Param(
        "list of names of columns to be excluded from the visualization",
        default=[])

    show_relations = twc.Param("(bool) show relationships?", default=True)
    show_attributes = twc.Param("(bool) show attributes?", default=True)

    imply_relations = twc.Param("(bool) show implied relationship nodes?",
                                default=True)

    auto_labels = twc.Param("(bool) Auto add relationship metadata to labels",
                            default=True)

    alphabetize_relations = twc.Param(
        """(str or int) Sub-package relationship items alphabetically.

        If the value is a `str`, it must be either 'always', or 'never'.

        If the value is an `int`, it is taken as a threshold where if and
        only if the number of items in the relation is greater than the
        threshold value will the relations then be branched out in
        alphabetically organized sub trees.

        The `imply_relations` param does not override this.  If you truely want
        no implicit nodes shown, then both must be set to False/'never'.
        """, default=26)

    alphabetize_minimal = twc.Param(
        """(bool) Trim away alphabetic entries that have no children.

        True or False.

        Make the tree easier to see.  Only useful in conjunction with
        `alphabetize_relations`.
        """, default=False)

    depth = twc.Param("(int) number of levels of relations to show.", default=3)

    def prepare(self):
        if type(self.rootObject) not in self.entities:
            raise ValueError, "Type of rootObject must be in entities"

        pkey = get_pkey(type(self.rootObject))
        self.url_kw = { 'key' : SEP.join(
            [type(self.rootObject).__name__,
             unicode(getattr(self.rootObject, pkey))]) }

        super(SQLARadialGraph, self).prepare()


    @classmethod
    def _alphabetize(cls, lst):
        """ True if, as configured, this widget should alphabetize this list.
        """
        return (
            cls.alphabetize_relations == 'always' or
            cls.alphabetize_relations < len(lst)
        )

    @classmethod
    def _do_alphabetize(cls, lst, depth, node_id):
        """ Produce the list of children of an alphabetized relation. """
        # TODO -- internationalization?
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        letter_nodes = [{
            'id' : "%s%s%s%s%s" % (node_id, SEP, ALPHA, SEP, ch),
            'name' : ch,
            'children' : [],
            'data' : {},
        } for ch in characters]

        return letter_nodes

    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        relationship_node, alphabetic_node = None, None
        if 'key' not in req.params:
            entkey = cls.entities[0].__name__
            pkey = get_pkey(cls.entities[0])
            key = getattr(cls.entities[0].query.first(), pkey)
        else:
            toks = req.params['key'].split(SEP)
            entkey, key = toks[-2:]
            if entkey not in [x.__name__ for x in cls.entities]:
                if entkey == ALPHA:
                    # Then this must be an 'alphabetic' node
                    if not len(toks) >= 6:
                        raise ValueError, "Invalid id len with %s." % ALPHA
                    entkey, key = toks[-6:-4]
                    relationship_node = toks[-4]
                    alphabetic_node = toks[-1]
                elif len(toks) >= 4:
                    # Then this might be a 'relationship' node
                    entkey, key = toks[-4:-2]
                    relationship_node = toks[-2]

        try:
            entity = filter(lambda x : x.__name__ == entkey, cls.entities)[0]
        except IndexError, e:
            raise ValueError, "No such sqla class '%s' in 'entities'." % entkey

        pkey = get_pkey(entity)

        obj = entity.query.filter_by(**{pkey:key}).one()

        def exclude_property(p):
            is_attribute = lambda x: type(x) is sa.orm.properties.ColumnProperty
            is_relation = lambda x: type(x) is sa.orm.properties.RelationshipProperty

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
                if cls.auto_labels:
                    result['name'] = "%s:<br/>%s" % (
                        name2label(key), result['name'])
                return result
            elif type(value) != sa.orm.collections.InstrumentedList:
                name = "%s:<br/>%s" % (name2label(key), unicode(value))
            else:
                node_id = SEP.join([prefix, key, unicode(uuid.uuid4())])
                name = "%s (%i)" % (name2label(key), len(value))
                if depth < cls.depth:
                    if not cls._alphabetize(value):
                        children = [make_node_from_object(o, depth+1, node_id)
                                    for o in value]
                    else:
                        children = cls._do_alphabetize(value, depth+1, node_id)

                        for child, obj in product(children, value):
                            if not child['id'].endswith(unicode(obj)[0].upper()):
                                continue
                            # This would mess with all the depth checking if it
                            # weren't for the removal code three blocks below.
                            n = make_node_from_object(obj,depth+2,child['id'])
                            child['children'].append(n)

                        for child in children:
                            child['name'] += " (%i)" % len(child['children'])

                        if cls.alphabetize_minimal:
                            children = [c for c in children
                                        if len(c['children']) > 0]

                        if not depth + 1 < cls.depth:
                            # Just delete 'em'!  We had to query them anyways
                            # to get the length counts for each alphabet letter,
                            # but if we keep them, we disobey the cls.depth
                            # parameter!  Oh wellz.
                            for child in children:
                                child['children'] = []


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

                # If 'imply_relations' is set to False
                # Wipe out each relation in the dict of props and replace it
                # with the actual objects from the relation.
                children = []
                for k, v in list(props.iteritems()):
                    if isinstance(v, sa.orm.collections.InstrumentedList):
                        del props[k]
                        if not cls.imply_relations:
                            children.extend([
                                make_node_from_object(
                                    item, depth+1,
                                    "%s%s%s%s%i" % (prefix, SEP, k, SEP, i))
                                for i, item in enumerate(v)
                            ])
                        else:
                            children.append(
                                make_node_from_property(
                                    prefix, obj, k, v, depth+1)
                            )

                children += [make_node_from_property(prefix, obj, k, v, depth+1)
                            for k, v in props.iteritems()]

            data = getattr(obj, '__jit_data__', lambda : {})()

            name = unicode(obj)
            if cls.auto_labels:
                name = "%s:  %s" % (name2label(type(obj).__name__), name)
            return {
                'id' : node_id,
                'name' : name,
                'children' : children,
                'data' : data,
            }

        if alphabetic_node:
            prefix = SEP.join([
                entity.__name__, key, relationship_node, str(uuid.uuid4())])

            json = {
                'id' : prefix,
                'name' : alphabetic_node,
                'children' : [],
                'data' : {}
            }

            original_relation = make_node_from_property(
                SEP.join([entity.__name__, key]),
                obj, relationship_node,
                getattr(obj, relationship_node), depth=1)

            original_parent = make_node_from_object(
                obj, prefix=json['id'], depth=2)

            for child in original_relation['children']:
                if child['name'].startswith('%s (' % alphabetic_node):
                    # TODO -- this isn't quite right and doesn't obey the depth
                    # rules correctly.
                    json['children'] = child['children']
                    original_relation['children'].remove(child)

            original_relation['children'].append(original_parent)
            json['children'].append(original_relation)
        elif relationship_node:
            json = make_node_from_property(
                SEP.join([entity.__name__, key]),
                obj, relationship_node, getattr(obj, relationship_node), 0)
            original_parent = make_node_from_object(
                obj, prefix=json['id'], depth=1)
            json['children'].append(original_parent)
        else:
            json = make_node_from_object(obj)

        return json

