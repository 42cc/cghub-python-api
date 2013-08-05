.. Testing the API

Testing
=======

.. code-block:: bash

    virtualenv .env --no-site-packages
    source .env/bin/activate
    pip install -r test_requirements.txt

    python -m unittest -v tests


Result:

.. code-block:: bash

    test_request (tests.test_request.RequestTestCase) ... ok
    test_request_build_query (tests.test_request.RequestTestCase) ... ok
    test_urlopen (tests.test_utils.UtilsTestCase) ... ok
    test_urlopen_repeat_requests_on_urlerror (tests.test_utils.UtilsTestCase) ... ok
