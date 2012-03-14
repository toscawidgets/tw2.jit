from webob import Request
from webob.multidict import NestedMultiDict
from tw2.core.testbase import assert_in_xml, assert_eq_xml, WidgetTest
from nose.tools import raises
from cStringIO import StringIO
from tw2.core import EmptyField, IntValidator, ValidationError
from cgi import FieldStorage
import formencode

import webob
if hasattr(webob, 'NestedMultiDict'):
    from webob import NestedMultiDict
else:
    from webob.multidict import NestedMultiDict

import tw2.jit.widgets as w

## TODO - this is a super-weak test.  so much more is done after the fact to
##  create the javascript calls.
class TestAreaChartWidget(WidgetTest):
    widget = w.AreaChart
    attrs = {'id' : 'foo'}
    params = {
        'data' : [
            { 'label': 'date A','values': [20, 40, 15, 5] },
            { 'label': 'date B', 'values': [30, 10, 45, 10] }
        ]
    }
    expected = """<div style="text-align:center; overflow:hidden; background-color:#3a3a3a; width: 500; height: 500;" id="foo"></div>"""
