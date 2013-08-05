.. API Documentation

API Documentation
=================

Main Interface
--------------

All functionality is implemented in class ``cghub_python_api.Request``.

As argument it takes an query. Query should be a dict, for example:

.. code-block:: python

    {
        'state': 'live',
        'study': ['phs000178', '*Other_Sequencing_Multiisolate']
    }

Every value can be list of strings or one string. In case when value is list,
it will be translated into string:

.. code-block:: python

    ['phs000178', '*Other_Sequencing_Multiisolate']
    will become
    '(phs000178 OR *Other_Sequencing_Multiisolate)'

Also next attributes can be specified while creating Request object:

    - offset - how many results should be skipped
    - limit - how many records output should have
    - sort_by - the attribute by which the results should be sorted (use '-' for reverse)
    - server_url - server url where WSAPI works
    - uri - uri that will be used to access data on WSAPI server

The most useful Request method is ``call()``.
It returns generator that returns results.
Example:

.. code-block:: python

    >>> request = Request(query={'state': 'live'}, limit=10)
    >>> for i in request.call():
    ...     print i
    ... 
    <cghub_python_api.api.Result object at 0x1c8d750>
    ...

``call()`` returns cghub_python_api.api.Result objects.
Result object is just wrapper for xml.etree.ElementTree object.
It allows to access to tree nodes using attributes.

Example:

.. code-block:: python

    result = Result(tree)
    print result.analysis_id
    print result['analysis_id']


To access to deeper elements like a filename:

.. code-block:: xml

    <files>
        <file>
            <filename>somefilename.txt</filename>

can be used next syntax:

.. code-block:: python

    print result['files.file.filename']

If files node has few file nodes, can be used indexes:

.. code-block:: python

    print result['files.file.0.filename']

Every node has ``text`` and ``attrib`` attributes.
The first returns text inside element and the second - dict with attributes specified inside tag:

.. code-block:: python

    >>> print results[1]['files.file.1.filename'].text
    UNCID_1176640.2bdc311e-59cc-449f-b8dc-6662052678fd.sorted_genome_alignments.bam.bai
    >>> print results[1]['files.file.0.checksum'].attrib
    {'type': 'MD5'}

If requested node was not found, will be returned cghub_python_api.api.NonExistent object.
To check is requested node exists can be used 'exist' attribute:

.. code-block:: python

    result.files.exist == True
    result.badattr.exist == False

Request has few methods that can be overrided.
For example, if we need to access to first file filename just by result.filename,
we can implement this by overriding patch_result method:

.. code-block:: python

    from cghub_python_api import Request


    class MyRequst(Request):

        def patch_result(self, result, result_xml):
            result.filename = result['files.file.0.filename']
