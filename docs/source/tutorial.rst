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

.. code-block:: python

  # gives us the core vocabulary
  from activipy import vocab

  post_this = vocab.Create(
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
  {"@type": "Create",
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
  >>> core.ASObj({
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
  ['acct:cwebber@identi.ca', 'acct:justaguy@rhiaro.co.uk']

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


The more we change, the more we stay the same
---------------------------------------------

.. TODO: We need functional setters for this part to work :)


Expanding our vocabulary
------------------------

Remember when we did this?

.. code-block:: python

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
