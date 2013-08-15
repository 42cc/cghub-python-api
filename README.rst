CGHub Python API
================

CGHub Python API.

Installation
------------

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/42cc/cghub-python-api.git#egg=cghub_python_api


Usage
-----

.. code-block:: python

    >>> from cghub_python_api import WSAPIRequest as Request
    >>> results = []
    >>> request = Request(query={'analysis_id': ['016cc2ca-db11-44af-b846-18e9275a4c4b', '01a589db-02d8-4d75-a2da-bb0bd8140a32']})
    >>> for result in request.call():
    ...     print result.state.text
    ...     results.append(result)
    ...
    live
    live
    >>> print results[0].disease_abbr.text
    BRCA
    >>> print results[0]['disease_abbr'].text
    BRCA
    >>> print results[1]['filename'].text
    UNCID_1176640.2bdc311e-59cc-449f-b8dc-6662052678fd.sorted_genome_alignments.bam
    >>> print results[1]['filename.0'].text
    UNCID_1176640.2bdc311e-59cc-449f-b8dc-6662052678fd.sorted_genome_alignments.bam
    >>> print results[1]['filename.1'].text
    UNCID_1176640.2bdc311e-59cc-449f-b8dc-6662052678fd.sorted_genome_alignments.bam.bai
    >>> print results[1]['checksum.0'].attrib
    {'type': 'MD5'}
    >>> results[0].analysis_id.exist
    True
    >>> results[0].somebadattr
    <cghub_python_api.api.NonExistent object at 0x1ef1950>
    >>> results[0].somebadattr.exist
    False
    >>> print results[0].somebadattr.text
    None


Read more in ``docs/source/*.rst``.


Running tests
-------------

.. code-block:: bash

    python -m unittest -v tests


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ cd cghub-python-api
    $ virtualenv .env --no-site-packages
    $ source .env/bin/activate
    $ python setup.py install
    $ pip install -r test_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
