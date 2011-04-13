""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import AjaxRadialGraph
from tw2.jit.samples.samples_data import RadialGraphJSONSampleData

yumobj = None
try:
    import yum

    yumobj = yum.YumBase()
    yumobj.setCacheDir()
except ImportError, e:
    import commands

def get_dependencies(package):
    if yumobj:
        # TODO -- fix this using the example from the Leafy Miracle
        pkg = yumobj.pkgSack.searchNevra(name=package)[0]
        deps_d = pkg.findDeps([pkg])
        deps = [tup[0] for tup in deps_d[deps_d.keys()[0]].keys()]
    else:
        deps = commands.getoutput(
            "yum deplist %s | grep dependency | awk ' { print $2 } '" % package)
        deps = list(set([dep.split('(')[0] for dep in deps.split('\n') if dep]))

    return deps

def get_dependency_tree(package, n=1, prefix=''):
    make_node = lambda package, prefix : { 
        'id': prefix + "___" + package,
        'name': package,
        'children': [],
        'data': {'hover_html':'<h2>%s</h2>' % package},
    }
    package = package.strip()
    print "Gathering dependencies of", package

    deps = get_dependencies(package)

    root = make_node(package, prefix)
    prefix = "%s_%s" % (prefix, package)

    if n > 0:
        [root['children'].append(
            get_dependency_tree(dep, n-1, prefix)) for dep in deps]
    else:
        [root['children'].append(make_node(dep, prefix)) for dep in deps]
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

    base_url = '/ajax_radialgraph_demo/'
    url_kw = {'key' : 'TurboGears'}

    background = { 'CanvasStyles':{ 'strokeStyle' : '#C73B0B' } }
    
    backgroundcolor = '#350608'

    Node = {
        'color' : '#C73B0B',
    }
            
    Edge = {
        'color': '#F2C545',
        'lineWidth':1.5,
    }

import tw2.core as twc
mw = twc.core.request_local()['middleware']
mw.controllers.register(DemoAjaxRadialGraph, 'ajax_radialgraph_demo')
