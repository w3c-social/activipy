About Activipy
==============

What is ActivityStreams?  How might it help me?
-----------------------------------------------

Activipy is a simple library which makes working with
`ActivityStreams <http://www.w3.org/TR/activitystreams-core/>`_ easy.
Which is a bit confusing, because ActivityStreams is already dead-easy.
Activipy helps us make things a bit more robust.

How easy is ActivityStreams?  Here's a valid ActivityStreams document
from a mad scientist type person::

  {"@id": "http://drboss.example/api/objects/123415/",
   "@type": "Create",
   "actor": {
       "@type": "Person",
       "@id": "http://drboss.example/me/",
       "displayName": "Professor BossManager"},
   "to": ["http://employeemine.example/jim/",
          "http://employeemine.example/sarah/"],
   "object": {
       "@type": "Note",
       "@id": "http://drboss.example/rants/power-productivity/",
       "content": "Thanks to my latest invention, productivity is up 1 million percent! MWAHAHA!!"}}

Here's another:

.. code-block:: python

  {"@id": "http://employeemine.example/sarah/blog/new-job-please/"
   "@type": "Note",
   "displayName": "New job, please.",
   "content": "Anyone know where I can get a job not managed by a mad scientist?"}
   
These objects aren't complex, and anyone can read them.  They're just
JSON, plus some
`common vocabulary <http://www.w3.org/TR/activitystreams-vocabulary/>`_,
including a convention that "@id" is the identifier of the object and
"@type" is the vocabulary type.  That's pretty simple!

And simple is good, because let's face it, most users of most web
application APIs are like poor Billy Scripter, a kid who has some
scripting language like Ruby or Python or Javascript and some JSON
parser in a toolbox and that's about it.  Billy Scripter knows how to
parse JSON pulled down from some endpoint, and that's about all he
knows how to do.  Poor Billy Scripter!  But it's okay, because
ActivityStreams is simple enough that Billy can make it by.  And
because the
`ActivityStreams Core <http://www.w3.org/TR/activitystreams-core/>`_
serialization specifies that the
`ActivityStreams Vocabulary <http://www.w3.org/TR/activitystreams-vocabulary/>`_
is always implied and that those terms must always be available,
Billy will always know what a `Like <http://www.w3.org/TR/activitystreams-vocabulary/#dfn-like>`_
object or a `Note <http://www.w3.org/TR/activitystreams-vocabulary/#dfn-note>`_
means.  Horray for Billy!

Meanwhile, you get the benefit of a well thought out "subject,
predicate, object" type structure (or in other words, "who did what").  The
`Core Classes <http://www.w3.org/TR/activitystreams-vocabulary/#types>`_
provide the basic structure, and that general structure combined with
the very minimal rules of `ActivityStreams Core <http://www.w3.org/TR/activitystreams-core/>`_
(roughly speaking, it's just JSON with the ActivityStreams vocabulary
implied, but if you need anything more, you can use `json-ld <http://json-ld.org/>`_)
means that you already have the general structure of all the "social"
type activities that happen on the modern web.  Throw in the
`Extended Classes <http://www.w3.org/TR/activitystreams-vocabulary/#extendedtypes>`_
and you've got all the right language to express what your users are
doing too.  Awesome.

But hey, what happens when the base
`ActivityStreams vocabulary <http://www.w3.org/TR/activitystreams-vocabulary/>`_
just isn't enough?  Maybe you're running a social network that's also
a game and you need some way to express that your players are beating
up goblins (wait, I take that back, don't beat up poor goblins!), or
you've got a highly interactive e-commerce site where users can share
coupons or whatever.  Look, whatever it is, you can express it in
ActivityStreams!

Yeah, I said it!  Sure, ActivityStreams gives you almost everything
you need out of the box, but if you need to get fancy and define your
own terms, you can do that too.  ActivityStreams is technically a
`json-ld <http://json-ld.org/>`_ document with an implied vocabulary,
but you can add on new vocabularies too.  Need to add Coupon objects,
or RpgBeatemup activities?  Yeah, you can do it!  And for all you
`RDF <http://www.w3.org/RDF/>`_ fans out there, you can transform
ActivityStreams objects into a full-on linked-data graph.  Go wild!

But you also don't *have* to.  Thanks to the promises made by the
ActivityStreams serialization, Billy Scripter can make it by just fine
with his Ruby and JSON toolkit.  And so can most of the rest of the
web!


How Activipy and ActivityStreams work together
----------------------------------------------

So if ActivityStreams is just JSON (and optionally json-ld), what do
you need Activipy for?  Good question!

Activipy provides a whole suite of useful tools, including friendly
and Pythonic constructors, a flexible and extensible method dispatch
system, and much more.  We could express the above like this::

  >>> from activipy import vocab
  >>> vocab.Create(
  ...   "http://drboss.example/api/objects/123415/",
  ...   actor=vocab.Person(
  ...     "http://drboss.example/me/",
  ...     displayName="Professor BossManager"),
  ...   to=["http://employeemine.example/jim/",
  ...       "http://employeemine.example/sarah/"],
  ...   object=vocab.Note(
  ...     "http://drboss.example/rants/power-productivity/",
  ...     content="Thanks to my latest invention, productivity is up 1 million percent! MWAHAHA!!"))

If we were writing our own diary application, we could specify an
environment that knows how to post notes to it::

  >>> from ourjournal import DiaryEnv
  >>> dear_diary = DiaryEnv.c.Note(
  ...     displayName="New job, please.",
  ...     content="Anyone know where I can get a job not managed by a mad scientist?")
  >>> dear_diary.m.post()

Activipy provides you with the basic tools you need to map
ActivityStreams to the world of your Python application.  And if
you're just starting out in writing a brand new social network
application?  You'd better believe Activipy is a good place to start!

Activipy means making your networked application social is easy.  And
best of all, you can speak a common language with other
ActivityStreams speaking applications across the net.

Sound good?  :ref:`Let's get started! <tutorial-chapter>`
