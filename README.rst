vIPer
=====

vIPer is an application specifically designed to work with IPython notebooks.

With vIPer you can:

* Write and execute IPython notebooks.
* Generate static html views of IPython notebooks: http://www.staticviper.oquanta.info
* Generate slideshow views of IPython notebooks: http://www.slideviper.oquanta.info
* Split your screen to see how your changes in the current notebook are rendered in html and slideshow views.
* Record audio and video from your IPython sessions: http://www.youtube.com/watch?v=n5IWwJnWkzQ&feature=g-upl
* Surf the web.
* And more is comming...

How to use it?
==============

\$ipython notebook --pylab=inline --no-browser

(pylab is optional)

Note: Set the --notebook-dir as the vIPer directory or open ipython notebook in the same directory where vIPer and the notebooks you are working lives.

\$python viper.py

(Dashboard page use port 8888, but you want to use another port, point to it using the address bar: Ctrl+a)

Dependencies
============

Ver: 0.13 (this is a very alpha release, you can play with it... but surely you will found several bugs.

* Python 2.7
* IPython > 0.12 (with its own dependencies)
* PyQt > 4.9
* Jinja2
* Pygments
* Latest Docutils

For example:

curl http://docutils.svn.sourceforge.net/viewvc/docutils/trunk/docutils/?view=tar > docutils.gz

pip install -U docutils.gz

* RecordMyDesktop (if you want to record audio and video).

License
=======

TBD (some code derived from others work is under APACHE license).

Author: Damián Avila, Jul 2012
==============================

