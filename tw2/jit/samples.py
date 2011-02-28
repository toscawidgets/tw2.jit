""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import AjaxRadialGraph
from tw2.jit.samples_data import RadialGraphJSONSampleData

import commands


def get_dependency_tree(package, n=1, prefix=''):
    make_node = lambda package, prefix : { 
        'id': prefix + "___" + package,
        'name': package,
        'children': [],
        'data': []
    }
    package = package.strip()
    print "Gathering dependencies of", package
    out = commands.getoutput(
        "yum deplist %s | grep dependency | awk ' { print $2 } '" % package)
    out = list(set([dep.split('(')[0] for dep in out.split('\n') if dep]))

    root = make_node(package, prefix)
    prefix = "%s_%s" % (prefix, package)

    if n > 0:
        [root['children'].append(
            get_dependency_tree(dep, n-1, prefix)) for dep in out]
    else:
        [root['children'].append(make_node(dep, prefix)) for dep in out]
    return root


class DemoAjaxRadialGraph(AjaxRadialGraph):
    from tw2.core.jsonify import jsonify
    @classmethod
    @jsonify
    def request(cls, req):
        if 'key' not in req.params:
            key = 'wine'
        else:
            key = req.params['key'].split('___')[-1]
        json = get_dependency_tree(key)
        return json

    url = '/db_radialgraph_demo/?key=wine'

    background = { 'CanvasStyles':{ 'strokeStyle' : '#555' } }
    
    backgroundcolor = '#0f0f0f'

    postInitJSCallback = JSSymbol(src="""
        (function (jitwidget) {
              jitwidget.compute();
              jitwidget.plot();
              $('#wine').click();
         })""")
    
    Node = {
        'color' : '#ddeeff',
    }
            
    Edge = {
        'color': '#C17878',
        'lineWidth':1.5,
    }

import tw2.core as twc
mw = twc.core.request_local()['middleware']
mw.controllers.register(DemoAjaxRadialGraph, 'db_radialgraph_demo')
