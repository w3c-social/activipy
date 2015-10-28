An Activipy tutorial
====================

.. TODO: Do we want to open up with a more "dive in" demo of the
   above?


Sweet beginnings
----------------

So say you and your friends are all conspiring to meet up for root
beer floats.  How could we structure that in Python?  First, let's
look at the ActivityStreams representation of this note, and then
we'll look at how we got there.

What vocabulary do we want to use?  Let's look at what comes out of
the box::

  >>> vocab.Create.notes
  'Indicates that the actor has created the object.'
  >>> vocab.Person.notes
  'Represents an individual person.'
  >>> vocab.Note.notes
  'Represents a short work typically less than a single paragraph in length.'

Those sound like the things we mean.  Great!  It's nice that Activipy
includes the notes from the
`Activity Vocabulary <http://www.w3.org/TR/activitystreams-vocabulary/>`_
so it's easy for us to keep track of what things mean.

So it turns out we can use these vocabulary definitions as friendly
constructors::

  # gives us the core vocabulary
  from activipy import vocab

  post_this = vocab.Create(
      "http://tsyesika.co.uk/act/foo-id-here/",
      actor=vocab.Person(
          "http://tsyesika.co.uk/",
          displayName="Jessica Tallon"),
      to=["acct:cwebber@identi.ca",
          "acct:justaguy@rhiaro.co.uk",
          "acct:ladyaeva@hedgehog.example"],
      object=vocab.Note(
          "htp://tsyesika.co.uk/chat/sup-yo/",
          content="Up for some root beer floats?"))

Oh, okay, that's pretty easy to read!  We can see that we've specified
who we are, who we want to send the message to, and the actual message
we're posting.

What does our message look like?  Let's see::

  >>> post_this.json()
  {"@id": "http://tsyesika.co.uk/act/foo-id-here/",
   "@type": "Create",
   "actor": {
       "@type": "Person",
       "@id": "http://tsyesika.co.uk/",
       "displayName": "Jessica Tallon"},
   "to": ["acct:cwebber@identi.ca",
          "acct:justaguy@rhiaro.co.uk",
          "acct:ladyaeva@hedgehog.example"],
   "object": {
       "@type": "Note",
       "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
       "content": "Up for some root beer floats?"}}

Oh interesting!  That looks pretty similar to the Python constructor
version.  In fact, we could have built this from the json itself::

  >>> from activipy import core, vocab
  >>> post_this = core.ASObj({
  ...     "@type": "Create",
  ...     "@id": "http://tsyesika.co.uk/act/foo-id-here/",
  ...     "actor": {
  ...         "@type": "Person",
  ...         "@id": "http://tsyesika.co.uk/",
  ...         "displayName": "Jessica Tallon"},
  ...     "to": ["acct:cwebber@identi.ca",
  ...            "acct:justaguy@rhiaro.co.uk",
  ...            "acct:ladyaeva@hedgehog.example"],
  ...     "object": {
  ...         "@type": "Note",
  ...         "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
  ...         "content": "Up for some root beer floats?"}},
  ...   vocab.BasicEnv)
  <ASObj Create>

Hm!  So it's nice to have "pythonic" constructors, but this json
representation isn't so complex... is it worth having a whole library
just for this?  Let's see what else Activipy gives us.

Activipy gives simple dictionary-style access::

  >>> post_this["to"]
  ['acct:cwebber@identi.ca', 'acct:justaguy@rhiaro.co.uk', 'acct:ladyaeva@hedgehog.example']

Helpful, but we could have gotten that from running .json() and
pulling out the right values!  But this is kinda nice::

  >>> root_beer_note = post_this["object"]
  >>> root_beer_note
  <ASObj Note "http://tsyesika.co.uk/chat/sup-yo/">
  
Cool, we've extracted the actual object we were going to post, and it
came back wrapped in an ASObj object.  Of course, we could always get
the json version of this if we wanted::

  >>> root_beer_note.json()
  {'@id': 'http://tsyesika.co.uk/chat/sup-yo/',
   '@type': 'Note',
   'content': 'Up for some root beer floats?'}

What kind of type is our newly extracted `root_beer_note`?  Let's see::

  >>> root_beer_note.types
  ['Note']

Wait, plural?  That's right, an ActivityStreams object's "type" is
actually a "composite type".  It turns out this is useful when
handling extensions to the vocabulary, but we'll come back to that
later.

Strings are less fun as types than ASTypes, so can we get that back?
We sure can::

  >>> root_beer_note.types_astype
  [<ASType Note>]

But hey, what's this thing::

  >>> root_beer_note.types_expanded
  ['http://www.w3.org/ns/activitystreams#Note']
  
Huh?  A URL?  This starts to hint at something more
complicated... something to do with extensions!  But we're getting
ahead of ourselves.  Extension stuff comes later!  Right now we're
itching to *do* something with these objects... so what can we do, and
how do we do it?


Methods for our madness
-----------------------

New environments, new friends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before we hop right into methods, a quick refresher.  Remember when we
said we could have built our post_this object like this?

.. code-block:: pycon

  >>> from activipy import core, vocab
  >>> post_this = core.ASObj({
  ...     # ... json stuff here
  ...   },
  ...   vocab.BasicEnv)
  <ASObj Create>

Wait, what's that BasicEnv thing hanging off the end?  That's pretty
curious.  What does it do?

Since we're passing into the object, it's a good (and correct) guess
to assume that the ASObj instance has access to it::

  >>> post_this.env
  <activipy.core.Environment at 0x7fecf206f5c0>

The environment helps us in a few ways.  For one thing, it contains a
set of vocabulary that our environment "knows" about.  In fact, we
could even do constructors that implicitly pass in the environment
directly from the environment itself, using the vocabulary it's been
informed of::

  >>> env = vocab.BasicEnv
  >>> root_beer_note = env.c.Note(
  ...   "htp://tsyesika.co.uk/chat/sup-yo/",
  ...   content="Up for some root beer floats?")
  >>> root_beer_note
  <ASObj.Note>

Well that's pretty neat!  It looks like the `Environment.c` accessor
is a friendly way to access vocabulary classes.  Cool!  So you can
already guess at one purpose for environments: if your application is
working with an extended vocabulary, it's possible for Activipy to
"know" about your vocabulary while determining types, etc.  The
BasicEnv is, as you would expect, the default and most minimal
environment, containing the core vocabulary and nothing else.  For
many applications, this is all you need.  If your application needs
additional terminology, we will cover this later in the manual, but
for now, we will only concern ourself with the core vocabulary.

Even if we stick with the core vocabulary, we may wish to use a
different environment than BasicEnv.  Why?  Well we keep saying that
we want to *do* something with our applications.  Aside from mapping
vocabulary, `Environment` objects can contain a mapping of methods!

So, we want to try something... what would be a good demo?  How about
storing things!  Sounds good to me!  In our case we're going to simply
serialize activitystreams objects to json and dump them in and out of
a minimalist key-value
`dbm database <https://docs.python.org/3/library/dbm.html>`_.
(Note: this will be a lot more efficient if you install the Python
bindings for `gdbm <http://www.gnu.org.ua/software/gdbm/>`_.)

Our dbm demo module contains a JsonDBM wrapper which conveniently
serializes/deserializes to/from json when pulling things in/out of the
database.  Let's give it a spin so we know what we're working with::

  >>> from activipy.demos import dbm
  >>> db = dbm.JsonDBM.open("/tmp/test.db")
  >>> db["foo"] = {"cat": "meow", "dog": "woof"}
  >>> db["foo"]
  {'cat': 'meow', 'dog': 'woof'}
  >>> "foo" in db
  True
  >>> del db["foo"]
  >>> "foo" in db
  False

Okay, so that's a pretty easy to use key-value store!  We could
clearly dump our ASObj objects to json and manually save them into
here.  It would be nice if there was a "save" method that could do
that for us though.  How could such a save method be made available?


Save one for me, please
~~~~~~~~~~~~~~~~~~~~~~~

Ah, here's a use for Environments!  You see, an `Environment`
object not only contains information about vocabulary, it contains
information about methods as well.  As it turns out, we have a handy
environment ready for you to play with which knows how to work with a
`JsonDBM` wrapped database.  Let's try it!

.. code-block:: pycon

  >>> env = dbm.DbmEnv
  >>> note = env.c.Note("http://example.org/notes/cookie-time/",
  ...                   content="I really want a cookie!")
  >>> note.m.save(db)
  >>> db["http://example.org/notes/cookie-time"]
  {'@id': 'http://example.org/notes/cookie-time/',
   '@type': 'Note',
   'content': 'I really want a cookie!'}

Hey, it worked!  That sure was handy... we got a .save() method
attached right to our Note!  How about a .delete()?

.. code-block:: pycon

  >>> "http://example.org/notes/cookie-time" in db
  True
  >>> note.m.delete(db)
  >>> "http://example.org/notes/cookie-time" in db
  False

How convenient!

You may notice that we don't call `note.save()` or `note.delete()`;
instead, we call `note.m.save()` and `note.m.delete()`!  That's
because the `.m` attribute is a proxy object to all the methods the
`ASObj.env` knows about (in this case, DbmEnv)::

  >>> dbm.DbmEnv.methods
  {(<MethodId save>, <ASType Object>): <function activipy.demos.dbm.dbm_save>,
   (<MethodId delete>, <ASType Object>): <function activipy.demos.dbm.dbm_delete>}

In fact, we could have used DbmEnv.m instead::

  >>> dbm.DvmEnv.m.save(note, db)
  >>> # is the same as
  >>> note.m.save(db)

But that's way more verbose!  Why not just use `note.m.save(db)`
instead?  So convenient!

What happens if we save a more complicated, nested note to the db?
Remember our root beer float friend?

.. code-block:: pycon

  >>> post_this.json()
  {"@id": "http://tsyesika.co.uk/act/foo-id-here/",
   "@type": "Create",
   "actor": {
       "@type": "Person",
       "@id": "http://tsyesika.co.uk/",
       "displayName": "Jessica Tallon"},
   "to": ["acct:cwebber@identi.ca",
          "acct:justaguy@rhiaro.co.uk",
          "acct:ladyaeva@hedgehog.example"],
   "object": {
       "@type": "Note",
       "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
       "content": "Up for some root beer floats?"}}
  
So we now remember that when post_this was set up, it used the general
purpose environment.  This means that there is no `post_this.m.save()`
method for us to call, because that method is not set up in the
BasicEnv environment.  We can't even use `BasicEnv.m.save()`,
because Activipy safeguards against this::

  >>> dbm.DbmEnv.m.save(post_this, db)
  Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/cwebber/devel/activipy/activipy/core.py", line 464, in method_dispatcher
    method = self.asobj_get_method(asobj, method_id)
  File "/home/cwebber/devel/activipy/activipy/core.py", line 550, in asobj_get_method
    "ASObj attempted to call method with an Environment "
  activipy.core.EnvironmentMismatch: ASObj attempted to call method with an Environment it was not bound to!

This makes sense, because different environments provide different
vocabularies and handle different methods, and subtle bugs could creep
in if we permitted this.  Normally this is no problem, one application
will in general only make use of a single `Environment` tuned to that
application.  Even here, it is easy to correct... let's just recast
`post_this` to our new environment::

  >>> post_this = core.ASObj(post_this.json(), dbm.DbmEnv)

Now we can save away:::

  >>> post_this.m.save(db)
  >>> db["http://tsyesika.co.uk/act/foo-id-here/"]
  {"@id": "http://tsyesika.co.uk/act/foo-id-here/",
   "@type": "Create",
   "actor": {
       "@type": "Person",
       "@id": "http://tsyesika.co.uk/",
       "displayName": "Jessica Tallon"},
   "to": ["acct:cwebber@identi.ca",
          "acct:justaguy@rhiaro.co.uk",
          "acct:ladyaeva@hedgehog.example"],
   "object": {
       "@type": "Note",
       "@id": "htp://tsyesika.co.uk/chat/sup-yo/",
       "content": "Up for some root beer floats?"}}
  
Horray, our note is in the database!  That's really nice.


Save a few more
~~~~~~~~~~~~~~~

But wait, is this really how we want?  Notice that this activity
contains two nested ActivityStreams objects: `actor` and `object`!
Wouldn't it be nice if the `.save()` method was able to be smart about
this and "normalize" the data for us, saving the child ActivityStreams
objects as their own database references, and pulling them out as
needed?

Let's think about this for a moment.  We know that the root activity
that we're posting here is of the type `Create`.  We could look at the
`ActivityStreams Vocabulary document <http://www.w3.org/TR/activitystreams-vocabulary/>`_
to find out the inheritence chain, but we don't even have to... Activipy
can help us out here::

  >>> post_this.types_inheritance
  [<ASType Create>, <ASType Activity>, <ASType Object>]

Looking at this, we know that `Create` is a type of `Activity`, which
is itself a type of `Object`.  Looking at the vocabulary document,
it's clear to us that the `actor` and `object` fields
`inherit from Activity <http://www.w3.org/TR/activitystreams-vocabulary/#dfn-activity>`_.

It seems fine to save a general `Object` type as-is as we already are,
and indeed, you may have noticed that the save method was operating
precisely on this ASType::

  >>> dbm.DbmEnv.methods
  {(<MethodId save>, <ASType Object>): <function activipy.demos.dbm.dbm_save>,
   (<MethodId delete>, <ASType Object>): <function activipy.demos.dbm.dbm_delete>}

So, since a `Create` *is* an Object, of course the basic save happens
here.  But it's even more an `Activity` than a mere `Object`, and if
we think about it, hey!  Pretty much on any `Activity` ASType (whether
it's a `Create` or a `Delete` or a `Like`...) it would be really nice
to normalize the `actor` and `object` fields.  Is there a way to
specify that we'd like to treat Activity objects a bit differently?
Indeed, there is!  As you've already guessed, if our `Environment` had
a separate method that did something different for `save` on
`Activity`, that would be really helpful.  And it turns out,
we've already supplied you with such an environment::

  >>> dbm.DbmNormalizedEnv.methods
  {(<MethodId save>, <ASType Object>): <function activipy.demos.dbm.dbm_save>,
   (<MethodId save>, <ASType Activity>): <function activipy.demos.dbm.dbm_activity_normalized_save>,
   (<MethodId denormalize>, <ASType Object>): <function activipy.demos.dbm.dbm_denormalize_object>,
   (<MethodId denormalize>, <ASType Activity>): <function activipy.demos.dbm.dbm_denormalize_activity>,
   (<MethodId delete>, <ASType Object>): <function activipy.demos.dbm.dbm_delete>}

Neat, this does indeed provide us with a separate method for Activity.
Let's switch to using the `DbmNormalizedEnv` instead and cast
`post_this` to use it (again, you wouldn't normally need to do this in
an application that uses just one environment)::

  >>> env = dbm.DbmNormalizedEnv
  >>> post_this = core.ASObj(post_this.json(), dbm.DbmNormalizedEnv)

Now what happens if we save the object?

.. code-block:: pycon

  >>> post_this.m.save(db)
  >>> db["http://tsyesika.co.uk/act/foo-id-here/"]
  {'@id': 'http://tsyesika.co.uk/act/foo-id-here/',
   '@type': 'Create',
   'actor': 'http://tsyesika.co.uk/',
   'object': 'http://tsyesika.co.uk/chat/sup-yo/',
   'to': ['acct:cwebber@identi.ca',
          'acct:justaguy@rhiaro.co.uk',
          'acct:ladyaeva@hedgehog.example']}
  >>> db["http://tsyesika.co.uk/"]
  {'@id': 'http://tsyesika.co.uk/',
   '@type': 'Person',
   'displayName': 'Jessica Tallon'}  
  >>> db["http://tsyesika.co.uk/chat/sup-yo/"]
  {'@id': 'http://tsyesika.co.uk/chat/sup-yo/',
   '@type': 'Note',
   'content': 'Up for some root beer floats?'}

Awesome... that is *exactly* what we were hoping for!

There and back again
~~~~~~~~~~~~~~~~~~~~

Just to bring things full circle, here's a method that demonstrates
pulling an object out of the database::

  >>> def dbm_fetch(id, db, env):
  ...     return core.ASObj(db[id], env)
  ...
  >>> normalized_post = dbm_fetch("http://tsyesika.co.uk/act/foo-id-here/",
  ...                             db, dbm.DbmNormalizedEnv)
  >>> normalized_post
  <ASObj Create "http://tsyesika.co.uk/act/foo-id-here/">
  >>> normalized_post.json()
  {'@id': 'http://tsyesika.co.uk/act/foo-id-here/',
   '@type': 'Create',
   'actor': 'http://tsyesika.co.uk/',
   'object': 'http://tsyesika.co.uk/chat/sup-yo/',
   'to': ['acct:cwebber@identi.ca',
          'acct:justaguy@rhiaro.co.uk',
          'acct:ladyaeva@hedgehog.example']}

We could make use of the environment's denormalize method::

  >>> normalized_post.m.denormalize(db)
  <ASObj Create "http://tsyesika.co.uk/act/foo-id-here/">
  >>> normalized_post.m.denormalize(db).json()
  {'@id': 'http://tsyesika.co.uk/act/foo-id-here/',
   '@type': 'Create',
   'actor': {'@id': 'http://tsyesika.co.uk/',
             '@type': 'Person',
             'displayName': 'Jessica Tallon'},
   'object': {'@id': 'http://tsyesika.co.uk/chat/sup-yo/',
              '@type': 'Note',
              'content': 'Up for some root beer floats?'},
   'to': ['acct:cwebber@identi.ca',
          'acct:justaguy@rhiaro.co.uk',
          'acct:ladyaeva@hedgehog.example']}

Hey look, it's our original post back, with the `actor` and `object`
filled in!  This time, they were extracted from their own entries'
key-value pairs in the database.  Neat!

And finally, we could simplify this whole thing, and write a method to
pull data out of the database in a denormalized fashion, making use of
our environment's denormalize methods::

  >>> def dbm_fetch_denormalized(id, db, env):
  ...     return env.m.denormalize(
  ...         dbm_fetch(id, db, env), db)
  ...
  >>> denormalized_post = dbm_fetch_denormalized(
  ...     "http://tsyesika.co.uk/act/foo-id-here/",
  ...     db, dbm.DbmNormalizedEnv)
  >>> denormalized_post
  <ASObj Create "http://tsyesika.co.uk/act/foo-id-here/"
  >>> denormalized_post.json()
  {'@id': 'http://tsyesika.co.uk/act/foo-id-here/',
   '@type': 'Create',
   'actor': {'@id': 'http://tsyesika.co.uk/',
             '@type': 'Person',
             'displayName': 'Jessica Tallon'},
   'object': {'@id': 'http://tsyesika.co.uk/chat/sup-yo/',
              '@type': 'Note',
              'content': 'Up for some root beer floats?'},
   'to': ['acct:cwebber@identi.ca',
          'acct:justaguy@rhiaro.co.uk',
          'acct:ladyaeva@hedgehog.example']}
  
Whew, what a round trip!

A word to the enwisened
~~~~~~~~~~~~~~~~~~~~~~~

This whole process above of calling the appropriate methods for the
appropriate type (or in our case, ASType) is called "method dispatch".
You may have noticed that we do things fairly differently from most
Python libraries, which usually use Python's native classes as an
inheritance chain, something like this::

  class Object(ASClass):
      class_id = "http://www.w3.org/ns/activitystreams#Object"
      # bla bla
      def save(self, db):
           # save thing here
           pass

  class Activity(Object):
      class_id = "http://www.w3.org/ns/activitystreams#Activity"
      # more bla bla
      def save(self, db):
           # save a bit differently
           pass
           
  class Create(Activity):
      class_id = "http://www.w3.org/ns/activitystreams#Create"

  # also define Note, etc here

We aren't doing that... we're using this intermediate `Environment`
thing instead, and ASObj instances are all just instances of ASObj.
Why?  Why not just use Python's normal class heirarchy?  Why have an
`Environment` at all?

There are a few reasons:

1. ActivityStreams technically has "composite types"... an "@type" can
   actually have *multiple* values set here, and the functionality
   provided by the ASObj will be a union of those types.  Because of
   this, Python's classes really don't work at all to track
   inheritence.  Luckily, there are other benefits of going with an
   `Environment`....

2. Different applications need to do different things.  It's useful to
   have a general way of handling method dispatch that appropriately
   pays respect to the inheritence system of the ActivityStreams base
   vocabulary, and it's nice to make that as Pythonic as posible, but
   you might never save ActivityStreams objects to a DBM store (very
   few production applications would).  You very well may store
   objects to an SQL database, or some object store, or who knows
   what.  You may wish to use Activipy for a desktop client or a
   server application, and those might do very different things.  What
   methods you specify are up to you, but Environments are built in
   such a way that sharing methods between them, picking and choosing
   the ones useful to you, and defining entirely new methods is easy.

3. The core vocabulary is good enough for most social web
   applications, but not for all.  You may well need to define
   entirely new vocabulary, and Activipy allows you to do this.
   Allowing a user to define their own Environment means that this is
   not difficult to do, and how to transfer to those to the
   appropriate ASType represenations (and then to know how to operate
   upon them) is very possible.

There's more to say on these subjects, but hopefully this section
helped put some of this into perspective.  Hopefully the rest of this
will become clear shortly, including how to expand our vocabulary
without tripping over each others' definitions between applications.
   

The more we change, the more we stay the same
---------------------------------------------

.. TODO: We need functional setters for this part to work :)

*TODO: Fill in this section on the immutable properties of Activipy*


Expanding our vocabulary
------------------------

Remember when we did this?

.. code-block:: pycon

  >>> root_beer_note.types_expanded
  ['http://www.w3.org/ns/activitystreams#Note']

This starts to make more sense when we think about naming
conflicts... if you send me a message about "running a mile", and I
send you a message about "running a program", those are obviously two
very different definitions of "running", and it might create a lot of
problems if they become confused.  There should be an unambiguous way
to represent things, and that's exactly where `json-ld
<http://json-ld.org/>`_ comes in.  In json-ld, json objects can be
"expanded" to an unambiguous format, and then "compacted" to the right
definitions for our own local server, so we'll never get confused
between two different definitions of "running" again.  Here's a brief
hint towards that right now::

  >>> post_this.expanded()
  [{'@type': ['http://www.w3.org/ns/activitystreams#Create'],
    'http://www.w3.org/ns/activitystreams#actor': [{'@id': 'http://tsyesika.co.uk/',
      '@type': ['http://www.w3.org/ns/activitystreams#Person'],
      'http://www.w3.org/ns/activitystreams#displayName': [{'@value': 'Jessica Tallon'}]}],
    'http://www.w3.org/ns/activitystreams#object': [{'@id': 'http://tsyesika.co.uk/chat/sup-yo/',
      '@type': ['http://www.w3.org/ns/activitystreams#Note'],
      'http://www.w3.org/ns/activitystreams#content': [{'@value': 'Up for some root beer floats?'}]}],
    'http://www.w3.org/ns/activitystreams#to': [{'@id': 'acct:cwebber@identi.ca'},
     {'@id': 'acct:justaguy@rhiaro.co.uk'}]}]

That might look a bit complicated, but normally you wouldn't work in
an expanded document, you'd compact to your local context.  If this
seems confusing, don't worry about it for now; Activipy uses json-ld
under the hood but you usually won't need to interact with it.  One
nice feature though is that ActivityStreams 2.0 documents have
an "implied context" of
`the core ActivityStreams vocabulary <http://www.w3.org/TR/activitystreams-vocabulary/>`_.
This means that a "Note" will always mean the ActivityStreams version
of a Note, even if you don't do any fancy context things and are using
just plain old json.  Even when you get into extension land, Activipy
makes things so that you can think as in terms of pythonic constructors
rather than json-ld, so your code will look like simple Python, just
like at the very beginning of our tutorial.

*TODO: Finish this section!*
