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
from sqlalchemy import (
    Column, Integer, Unicode,
    MetaData, Table, ForeignKey,
)
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
import tw2.sqla as tws

session = tws.transactional_session()
Base = declarative_base(metadata=MetaData('sqlite:///sample_sqla.db'))
Base.query = session.query_property()

friends_mapping = Table(
    'persons_friends_mapping', Base.metadata,
    Column('friender_id', Integer,
           ForeignKey('persons.id'), primary_key=True),
    Column('friendee_id', Integer,
           ForeignKey('persons.id'), primary_key=True))

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    some_attribute = Column(Unicode(255), nullable=False)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    variety = Column(Unicode(255), nullable=False)
    owner_id = Column(Integer, ForeignKey('persons.id'))
    owner = relation(
        Person, primaryjoin=owner_id==Person.id,
        backref=backref('pets'))

    def __unicode__(self):
        return "%s the %s" % (self.name, self.variety)

Person.__mapper__.add_property('friends', relation(
    Person,
    primaryjoin=Person.id==friends_mapping.c.friendee_id,
    secondaryjoin=friends_mapping.c.friender_id==Person.id,
    secondary=friends_mapping,
    doc="List of this persons' friends!",
))

Base.metadata.create_all()

def populateDB(sess):
    import random

    firsts = ["Sally", "Suzie", "Sandy",
              "John", "Jim", "Joseph"]
    lasts = ["Anderson", "Flanderson", "Johnson",
             "Frompson", "Qadafi", "Mubarak", "Ben Ali"]

    for first in firsts:
        for last in lasts:
            p = Person(
                first_name=first, last_name=last,
                some_attribute="Fun fact #%i" % random.randint(0,255)
            )
            sess.add(p)

    pet_names = ["Spot", "Mack", "Cracker", "Fluffy", "Alabaster",
                 "Slim Pickins", "Lil' bit", "Balthazaar", "Hadoop"]
    varieties = ["dog", "cat", "bird", "fish", "hermit crab", "lizard"]

    for person in Person.query.all():
        for i in range(random.randint(0,7)):
            pet = Pet(name=pet_names[random.randint(0,len(pet_names)-1)],
                      variety=varieties[random.randint(0,len(varieties)-1)])
            sess.add(pet)
            person.pets.append(pet)


    qadafis = Person.query.filter_by(last_name='Qadafi').all()
    mubaraks = Person.query.filter_by(last_name='Mubarak').all()
    benalis = Person.query.filter_by(last_name='Ben Ali').all()
    dictators = qadafis + mubaraks + benalis

    print "populating dictators friends"
    for p1 in dictators:
        for p2 in dictators:
            if p1 == p2 or p1 in p2.friends:
                continue
            if random.random() > 0.25:
                p1.friends.append(p2)
                p2.friends.append(p1)

    print "populating everyone else's friends"
    for p1 in Person.query.all():
        for p2 in Person.query.all():
            if p1 == p2 or p1 in p2.friends:
                continue
            if random.random() > 0.95:
                p1.friends.append(p2)
                p2.friends.append(p1)

    print "done populating DB"

populateDB(session)
transaction.commit()


class DemoSQLARadialGraph(SQLARadialGraph):
    entities = [Person, Pet]
    url = '/db_radialgraph_demo/'

    background = { 'CanvasStyles':{ 'strokeStyle' : '#C73B0B' } }

    backgroundcolor = '#350608'

    postInitJSCallback = JSSymbol(
        src="""
        (function (jitwidget) {
        jitwidget.compute();
        jitwidget.plot();
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
