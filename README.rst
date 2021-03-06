kirchenreich
============

Place #7 in Django Dash 2012.


About
-----

**Kirchenreich** is a mashup using data from `Openstreetmap <http://www.openstreetmap.org>`_ 
and `Wikipedia <http://en.wikipedia.org>`_. The **purpose** of the site is to correlate 
informations about places of worship and show problems within the data.
We want to **encourage** users to fix the problems in Wikipedia and Openstreetmap.

*Kirche* is the German word for *church* and *reich* is German for *rich* or *realm*.
Of course this site not only has churches, but all **places of worship**.

We developed this site for the `DjangoDash <http://djangodash.com>`_ **at one weekend**.
We will improve this site in the future.
The whole sourcecode is on `Github <https://github.com/mfa/kirchenreich>`_ under BSD licence.

Feel free to fork the repository, file bugrequests or even send in feature wishes.


Live site
---------

Production site is http://kirchenreich.org/.


Developer information
---------------------

Install How-to
~~~~~~~~~~~~~~

* clone github repo

::

  # create virtualenv
  virtualenv env_kr
  # activate
  . env_kr/bin/activate
  # install requirements
  pip install -r requirements.d/dev-standalone.txt


* set in krprj/settings/local.py

::

  # SECRET_KEY - see http://www.miniwebtool.com/django-secret-key-generator/
  # DATABASES - see settings.py for template without user/pw


Run locally
~~~~~~~~~~~

* you need postgresql with postgis support!
* for some stuff you may need redis and celery.
* download world to world/data/:

::

  mkdir world/data
  cd world/data
  wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
  unzip TM_WORLD_BORDERS-0.3.zip
  rm TM_WORLD_BORDERS-0.3.zip

* import worlddata (in django shell):

::

  from world import load
  load.run()


* run testserver

::

  ./manage.py runserver


Deploy on kirchereich.org
~~~~~~~~~~~~~~~~~~~~~~~~~

* you need system user with sudo right on the server

List of available commands:

::

  fab -l

Run deployment on server:

::

  fab deploy -u <your system user>

Notice that you may have to specify your server user name with the -u flag.
