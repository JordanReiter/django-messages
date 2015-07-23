==========================================
A user-to-user messaging system for Django
==========================================

Django-messages enables your users to send private messages to each other.
It provides a basic set of functionality that you would expect from such a system.
Every user has an Inbox, an Outbox and a Trash. Messages can be composed and
there is an easy, url-based approach to preloading the compose-form with the
recipient-user, which makes it extremly easy to put "send xyz a message" links
on a profile-page.

Currently django-messages comes with these translations:

* ar (thanks to speedy)
* da (thanks Michael Lind Mortensen)
* de
* el (thanks Markos Gogoulos)
* es (thanks paz.lupita)
* es_AR (thanks Juanjo-sfe)
* fa
* fr (thanks froland and dpaccoud)
* it (thanks to Sergio Morstabilini)
* lt
* ko
* nl (thanks krisje8)
* pl (thanks maczewski)
* pt_BR (thanks Diego Martins)
* ru (thanks overkrik)
* zh_CN (thanks Gene Wu)


Versions
--------

<<<<<<< HEAD
+-------+-------------------------------------------------------------------+
| 0.5.x | compatible with Django 1.4, 1.5, 1.6 and 1.7; if you are          |
|       | upgrading from 0.4.x to trunk please read the UPGRADING docs.     |
+-------+-------------------------------------------------------------------+
| 0.4.x | compatible with Django 1.1 (may work with Django 1.0/1.2), no     |
|       | longer maintained                                                 |
+-------+-------------------------------------------------------------------+
| 0.3   | compatible with Django 1.0, no longer maintained                  |
+-------+-------------------------------------------------------------------+
=======
* The current trunk/head is compatible with Django 1.2; users of Django 1.1 
  should continue using messages-0.4.x; if you are upgrading from 0.4.x to trunk 
  please read the UPGRADING docs.
* messages-0.4.x is compatible with Django 1.1 (and may work with Django 1.0). 
  The code is avaliable as a Branch.
* messages-0.3 is compatible with Django 1.0, but no longer maintained
* messages-0.2 is still compatible with Django 0.96.x, but not longer maintaned.
  The code is avalibale as a Branch.
>>>>>>> 84790982dbd00f32a8f722fd9878dd99a76b6da0


Documentation
-------------

<<<<<<< HEAD
The documentation is contained in the /docs/ directory and can be build with
sphinx. A HTML version of the documentation is available at:
http://django-messages.readthedocs.org
=======
The documentation is contained in the /docs/ directory and can be build with 
sphinx. A HTML version of the documentation is available at: 
http://files.arnebrodowski.de/software/django-messages/Documentation/
>>>>>>> 84790982dbd00f32a8f722fd9878dd99a76b6da0


Install
-------
<<<<<<< HEAD
Download the tar archive, unpack and run python setup.py install or checkout
the trunk and put the ``django_messages`` folder on your ``PYTHONPATH``.
Released versions of django-messages are also available on pypi and can be
=======
Download the tar archive, unpack and run python setup.py install or checkout 
the trunk and put the ``django_messages`` folder on your ``PYTHONPATH``. 
Released versions of django-messages are also available on pypi and can be 
>>>>>>> 84790982dbd00f32a8f722fd9878dd99a76b6da0
installed with easy_install or pip.


Usage
-----

<<<<<<< HEAD
Add ``django_messages`` to your ``INSTALLED_APPS`` setting and add an
``include('django_messages.urls')`` at any point in your url-conf.

The app includes some default templates, which are pretty simple. They
extend a template called ``base.html`` and only emit stuff in the block
``content`` and block ``sidebar``. You may want to use your own templates,
=======
Add ``django_messages`` to your ``INSTALLED_APPS`` setting and add an 
``include('django_messages.urls')`` at any point in your url-conf.

The app includes some default templates, which are pretty simple. They 
extend a template called ``base.html`` and only emit stuff in the block 
``content`` and block ``sidebar``. You may want to use your own templates, 
>>>>>>> 84790982dbd00f32a8f722fd9878dd99a76b6da0
but the included ones are good enough for testing and getting started.


Dependencies
------------

<<<<<<< HEAD
Django-messages has no external dependencies except for django. However, if
django-notification and/or django-mailer are found, it will make use of them.
Note: as of r65 django-messages will only use django-notification if
'notification' is also added to the INSTALLED_APPS setting. This has been
done to make situations possible where notification is on pythonpath but
should not be used, or where notification is another python package, such as
=======
Django-messages has no external dependencied except for django. But if 
django-notification and/or django-mailer are found it will make use of them. 
Note: as of r65 django-messages will only use django-notification if 
'notification' is also added to the INSTALLES_APPS setting. This has been 
done to make situations possible where notification is on pythonpath but 
should not be used, or where notification is an other python package as 
>>>>>>> 84790982dbd00f32a8f722fd9878dd99a76b6da0
django-notification which has the same name.



