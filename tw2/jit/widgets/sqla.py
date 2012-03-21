import tw2.core as twc
from tw2.core.resources import JSSymbol
from tw2.core.util import name2label

from tw2.jit.widgets.ajax import AjaxRadialGraph

# Used for doing ajax stuff
import tw2.jquery

import urllib
import sqlalchemy as sa
from hashlib import md5
from itertools import product
from BeautifulSoup import BeautifulSoup

SEP = '___'
ALPHA = 'ALPHA'

get_pkey = lambda ent : ent.__mapper__.primary_key[0].key

def _unicode(obj):
    result = ''.join(BeautifulSoup(unicode(obj)).findAll(text=True)).strip()
    return unicode(result)

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
    show_empty_relations = twc.Param("(bool) show empty relationships?",
                                     default=True)
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

        The `imply_relations` param overrides this!  The two params are not
        compatible.
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
             _unicode(getattr(self.rootObject, pkey))]) }

        super(SQLARadialGraph, self).prepare()

    # Override this from AjaxRadialGraph to get hot morphing!!!
    # This javascript stuff gets called after a json graph has been successfully
    # retrieved, but before it is handed to jit for rendering.  The code that
    # follows mangles IDs in the new tree so that thejit smoothly animates
    # (morphs) the old tree into the new (where it can).
    preprocessTree = JSSymbol(src="""
        (function(json) {
            var SEP = '%s';
            var ch = json.children;
            var getNode = function(nodeId) {
                for(var i=0; i < ch.length; i++) {
                    var new_ch_toks = ch[i].id.split(SEP).reverse();
                    var old_id_toks = nodeId.split(SEP).reverse();
                    var count = 0;
                    for (var j=0; j < new_ch_toks.length && j < old_id_toks.length; j++) {
                        if ( new_ch_toks[j] === old_id_toks[j] ) {
                            count++;
                        } else {
                            break;
                        }
                    }
                    if ( count >= 4 ) {
                        return ch[i]
                    }
                }
                return false;
            }
            json.id = $$jitwidget.root;
            var root = $$jitwidget.graph.getNode($$jitwidget.root);
            $jit.Graph.Util.eachAdjacency(root, function(elem) {
                var nodeTo = elem.nodeTo, jsonNode = getNode(nodeTo.id);
                if(jsonNode) jsonNode.id = nodeTo.id;
            });
        })""" % SEP)


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
        if 'key' not in req.params or not req.params['key']:
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
            s = s.replace(' ', '_').replace('#', '___')
            try:
                i, j = s.index('<'), s.rindex('>')+1
                if j < i:
                    return s
                hashed = md5(s[i:j]).hexdigest()
                return s[:i] + hashed + s[j:]
            except ValueError as e:
                pass
            return s

        def make_node_from_property(prefix, parent, key, value, depth):
            node_id = safe_id(SEP.join([prefix, key, _unicode(value or '')]))
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
                salt = SEP.join(prefix.split(SEP)[-2:] + [key])
                digest = md5(salt).hexdigest()
                node_id = SEP.join([prefix, key, digest])
                name = "%s (%i)" % (name2label(key), len(value))
                if depth < cls.depth:
                    if not cls._alphabetize(value):
                        children = [make_node_from_object(o, depth+1, node_id)
                                    for o in value]
                    else:
                        children = cls._do_alphabetize(value, depth+1, node_id)

                        for child, obj in product(children, value):
                            if not child['id'].endswith(_unicode(obj)[0].upper()):
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
                          _unicode(getattr(obj, get_pkey(type(obj))))]))
            prefix = node_id
            children = []
            data = getattr(obj, '__jit_data__', lambda : {})()
            cost = lambda k : data.get('traversal_costs', {}).get(k, 1)
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
                        if depth+cost(k) > cls.depth:
                            continue
                        if not cls.show_empty_relations and len(v) == 0:
                            continue
                        if not cls.imply_relations:
                            children.extend([
                                make_node_from_object(
                                    item, depth+cost(k),
                                    "%s%s%s%s%i" % (prefix, SEP, k, SEP, i))
                                for i, item in enumerate(v)
                            ])
                        else:
                            children.append(
                                make_node_from_property(
                                    prefix, obj, k, v, depth+cost(k))
                            )

                for k, v in props.iteritems():
                    if depth+cost(k) > cls.depth:
                        continue
                    children.append(
                        make_node_from_property(prefix, obj, k, v,
                                                depth+cost(k))
                    )

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
            salt = SEP.join([entity.__name__, key, relationship_node])
            digest = md5(salt).hexdigest()
            prefix = SEP.join([entity.__name__, key, relationship_node, digest])

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
                    # Here we throw away work that we've already done.  Sad.
                    original_relation['children'].remove(child)
                    break

            # Unfortunately, we have to 'do the same work twice' here
            # because at present I'm too lazy to do it correctly.  We're
            # going to make the same queries to expand children out a
            # second time.  Fortunately, sqlalchemy should make the
            # performance hit less noticable.
            #
            # Just to be clear, the call above to build
            # 'original_relation' makes the same queries we're about to
            # make here but with a 'depth' setting that doesn't make
            # sense since we reorganizing the tree here.  We just going
            # to make the same calls again on the children of the
            # 'faked' root node.
            #
            # In the future this can be optimized.
            for child in getattr(obj, relationship_node):
                if not _unicode(child)[0].upper().startswith(alphabetic_node):
                    continue

                json['children'].append(make_node_from_object(
                    child, prefix=prefix, depth=1))

            original_relation['children'].append(original_parent)
            json['children'].append(original_relation)
        elif relationship_node:
            json = make_node_from_property(
                SEP.join([entity.__name__, key]),
                obj, relationship_node, getattr(obj, relationship_node), 0)
            original_parent = make_node_from_object(
                obj, prefix=json['id'], depth=1)
            for child in original_parent['children']:
                if child['name'] == json['name']:
                    original_parent['children'].remove(child)
                    break
            json['children'].append(original_parent)
        else:
            json = make_node_from_object(obj)

        return json

