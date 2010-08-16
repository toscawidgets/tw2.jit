
from tw2.core.widgets import WidgetMeta
from tw2.core.resources import JSSource
import tw2.core.params
import re
from simplejson import JSONEncoder
from simplejson.encoder import (
    encode_basestring_ascii, encode_basestring,
    FLOAT_REPR, PosInf,
    _make_iterencode, c_make_encoder)

class special(str):
    pass

class NotQuiteJSONEncoder(JSONEncoder):
    def default(self, obj):
        print "Verifying obj:", type(obj)
        if isinstance(obj, WidgetMeta):
            print "Got in"
            obj = obj.req()
        print " Verifying source:", type(obj)
        if 'JSSource_s' == obj.__class__.__name__:
            return special(re.sub("\s+", " ", obj.src))
        return super(NotQuiteJSONEncoder, self).default(obj)

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring
        if self.encoding != 'utf-8':
            def _encoder(o, _orig_encoder=_encoder, _encoding=self.encoding):
                if isinstance(o, str):
                    o = o.decode(_encoding)
                return _orig_encoder(o)

        # These three lines are all i wanted to add
        def _encoder(obj, _orig_encoder=_encoder):
            if isinstance(obj, special):
                return _orig_encoder(obj)[1:-1]
            return _orig_encoder(obj)
        # End lines I wanted to add.
        
        def floatstr(o, allow_nan=self.allow_nan,
                _repr=FLOAT_REPR, _inf=PosInf, _neginf=-PosInf):
            # Check for specials. Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on
            # the internals.

            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text


        key_memo = {}
        if (_one_shot and c_make_encoder is not None
                and not self.indent and not self.sort_keys):
            _iterencode = c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan, key_memo, self.use_decimal)
        else:
            _iterencode = _make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot, self.use_decimal)
        try:
            return _iterencode(o, 0)
        finally:
            key_memo.clear()


