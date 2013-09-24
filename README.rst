vIPer
=====

vIPer is an application specifically designed to work with IPython notebooks.

With vIPer you can:

* Write and execute IPython notebooks.
* Generate static html views of IPython notebooks.
* Generate slideshow views of IPython notebooks.
* Split your screen to see how your changes in the current notebook are rendered in html and slideshow views.
* Record audio and video from your IPython sessions.
* Surf the web.
* And more is comming...

How to use it?
==============

\$ipython notebook --no-browser

*Note: Set the --notebook-dir as the vIPer directory or open ipython notebook in the same directory where vIPer and the notebooks you are working lives.*

\$python viper.py

(Dashboard page use port 8888, but you want to use another port, point to it using the address bar: Ctrl+a)

Dependencies
============

**Version 1.1**: now supporting the last IPython release and using the IPython.nbconvert machinery (as usual... you can play with it, but surely you will find several bugs, just report them).

* Python 2.7 (obviously...)
* IPython > 1.1.0 (with its own dependencies)
* PyQt > 4.9
* Jinja2
* Pygments
* RecordMyDesktop (if you want to record audio and video).

License
=======

BSD-Modified (also known as New BSD or  Revisited BSD).

Author: Damián Avila
====================

