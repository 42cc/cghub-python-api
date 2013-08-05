.. About writing and using the documentation

Updating documentation
======================

Update files in the ``source`` directory. Build html pages with ``make html`` command.

Viewing documentation in browser
================================

.. code-block:: bash

    cd docs
    make html
    cd build/html/
    python -m SimpleHTTPServer 8001
    firefox http://127.0.0.1:8001
