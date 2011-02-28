""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import SQLARadialGraph

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

import transaction
from sqlalchemy import Column, Integer, Unicode, MetaData
from sqlalchemy.ext.declarative import declarative_base
import tw2.sqla as tws

session = tws.transactional_session()
Base = declarative_base(metadata=MetaData('sqlite:///sample_sqla.db'))
Base.query = session.query_property()

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    some_attribute = Column(Unicode(255), nullable=False)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

Base.metadata.create_all()

def populateDB(sess):
    import random

    firsts = ["Sally", "Suzie", "Sandy",
              "John", "Jim", "Joseph"]
    lasts = ["Anderson", "Flanderson", "Johnson",
             "Bean", "Kelsey", "Bean-Kelsey",
             "Frompson", "Qadafi", "Mubarak", "Ben Ali"]

    for first in firsts:
        for last in lasts:
            p = Person(
                first_name=first, last_name=last,
                some_attribute="Fun fact #%i" % random.randint(0,255)
            )
            sess.add(p)

    qadafis = Person.query.filter_by(last_name='Qadafi').all()
    mubaraks = Person.query.filter_by(last_name='Mubarak').all()
    benalis = Person.query.filter_by(last_name='Ben Ali').all()
    dictators = qadafis + mubaraks + benalis
#
#    for p1 in dictators:
#        for p2 in dictators:
#            if p1 == p2 or p1 in p2.friends:
#                continue
#            if random.random() > 0.25:
#                p1.friends.append(p2)
#    
#    for p1 in Person.query.all():
#        for p2 in Person.query.all():
#            if p1 == p2 or p1 in p2.friends:
#                continue
#            if random.random() > 0.75:
#                p1.friends.append(p2)

populateDB(session)
#session.commit()
transaction.commit()
print Person.query.all()


class DemoSQLARadialGraph(SQLARadialGraph):
    entity = Person
    url = '/db_radialgraph_demo/?key=1'

    background = { 'CanvasStyles':{ 'strokeStyle' : '#C73B0B' } }
    
    backgroundcolor = '#350608'

    postInitJSCallback = JSSymbol(src="""
        (function (jitwidget) {
              jitwidget.compute();
              jitwidget.plot();
              $('#wine').click();
         })""")
    
    Node = {
        'color' : '#C73B0B',
    }
            
    Edge = {
        'color': '#F2C545',
        'lineWidth':1.5,
    }

import tw2.core as twc
mw = twc.core.request_local()['middleware']
mw.controllers.register(DemoSQLARadialGraph, 'db_radialgraph_demo')
