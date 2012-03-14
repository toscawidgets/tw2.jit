""" Samples of how to use tw2.jit

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from tw2.core.resources import JSSymbol

from tw2.jit.widgets import SQLARadialGraph

import transaction
from sqlalchemy import (
    Column, Integer, Unicode,
    MetaData, Table, ForeignKey,
)
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
import tw2.sqla as tws

session = tws.transactional_session()
Base = declarative_base(metadata=MetaData('sqlite:///%s.db' % __name__))
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
        return "<img src='%s' /> %s %s" % (
            self.gravatar_url(8), self.first_name, self.last_name)

    @property
    def email(self):
        return "%s.%s@socialistworker.org" % (self.first_name, self.last_name)

    def gravatar_url(self, size=64):
        # import code for encoding urls and generating md5 hashes
        import urllib
        try:
            from hashlib import md5
        except ImportError:
            import md5
            md5 = md5.new

        # construct the url
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        gravatar_url += urllib.urlencode({
            'gravatar_id': md5(self.email.lower()).hexdigest(),
            'size': size, 'd': 'monsterid',
        })
        return gravatar_url


    def __jit_data__(self):
        dictator = "This person is not a dictator."
        if self.last_name in ["Ben Ali", "Mubarak", "Qaddafi"]:
            dictator = "Probably needs to be overthrown."

        return {
            # This attribute is used to generate hoverover tips
            "hover_html" : """
            <div>
                <h3>person.__jit_data__()['hover_html']</h3>
                <img src="%s" />
                <p>%s %s with %i friends and %i pets.</p>
                <p>%s</p>
            </div>
            """ % (self.gravatar_url(), self.first_name, self.last_name,
                   len(self.friends), len(self.pets), dictator),

            # This attribute is ultimately just ignored but by
            # specifying it here, it is made available clientside
            # for any custom js you want to rig up.
            "some_attr" : self.some_attribute,

            "traversal_costs" : {
                # You can set this to 2 to change the way depth
                # accumulates during the generation of a json response.
                'friends' : 1
            }
        }


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

    def __jit_data__(self):
        # TODO -- in the future, let's add other attributes
        #         like 'click' or some js callbacks
        return {
            "hover_html" : """
            <div>
                <h3>pet.__jit_data__()['hover_html']</h3>
                <p>This content is specified in the sqlalchemy model.
                If you didn't know.  This is a Pet object.
                It is a %s that goes by the name %s.</p>
                <p>You might want to
                <a href="http://www.google.com/search?q=%s">
                    google for its name
                </a>, or something.</p>
            </div>""" % (self.variety, self.name, self.name),

            "traversal_costs" : {
                'owner' : 2,
            }
        }

Person.__mapper__.add_property('friends', relation(
    Person,
    primaryjoin=Person.id==friends_mapping.c.friendee_id,
    secondaryjoin=friends_mapping.c.friender_id==Person.id,
    secondary=friends_mapping,
    doc="List of this persons' friends!",
))

Base.metadata.create_all()

def populateDB(sess):
    if Person.query.count() > 0:
        print "Not populating DB.  Already stuff in there."
        return

    import random

    firsts = ["Sally", "Suzie", "Sandy",
              "John", "Jim", "Joseph"]
    lasts = ["Anderson", "Flanderson", "Johnson",
             "Frompson", "Qaddafi", "Mubarak", "Ben Ali"]

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


    qaddafis = Person.query.filter_by(last_name='Qaddafi').all()
    mubaraks = Person.query.filter_by(last_name='Mubarak').all()
    benalis = Person.query.filter_by(last_name='Ben Ali').all()
    dictators = qaddafis + mubaraks + benalis

    print "populating dictators friends"
    for p1 in dictators:
        for p2 in dictators:
            if p1 == p2 or p1 in p2.friends:
                continue
            if random.random() > 0.75:
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
    excluded_columns = ['id', 'owner_id']

    # Some initial target
    rootObject = Person.query.first()

    base_url = '/db_radialgraph_demo/'

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
mw.controllers.register(DemoSQLARadialGraph, 'db_radialgraph_demo')
