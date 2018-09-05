.. _dev-notes:

Notes to developers
===================

Installation
------------


Code style
----------


Documentation
-------------

Build the docs locally by first setting up the sphinx environment with (executed
from top-level folder)

.. code-block:: bash

    sphinx-apidoc -f -o doc/api windnode_kwum

And then you build the html docs on your computer with

.. code-block:: bash

    sphinx-build -E -a doc/ doc/_build/html/

Please make sure Sphinx' build path (doc/_build/ in this case) is included in the
.gitignore file to avoid pushing your local docs.
