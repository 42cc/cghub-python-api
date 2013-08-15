.. API Documentation

API Documentation
=================

Main Interface
--------------

All functionality are implemented in classes ``cghub_python_api.WSAPIRequest`` and ``cghub_python_api.SOLRRequest``.

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

Also next attributes can be specified while creating *Request object:

    - offset - how many results should be skipped
    - limit - how many records output should have
    - sort_by - the attribute by which the results should be sorted (use '-' for reverse)
    - server_url - server url where WSAPI works
    - uri - uri that will be used to access data on WSAPI server

The most useful Request method is ``call()``.
It returns generator that returns results.
Example:

.. code-block:: python

    >>> from cghub_python_api import WSAPIRequest as Request
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

If files node has few file nodes, can be used indexes:

.. code-block:: python

    print result['filename.0']

Default index - 0.

Every node has ``text`` and ``attrib`` attributes.
The first returns text inside element and the second - dict with attributes specified inside tag:

.. code-block:: python

    >>> print results[1]['filename.0'].text
    UNCID_1176640.2bdc311e-59cc-449f-b8dc-6662052678fd.sorted_genome_alignments.bam.bai
    >>> print results[1]['checksum.0'].attrib
    {'type': 'MD5'}
    # If used SOLRRequest, checksum type attribute will be stored in:
    print results[1]['checksum_method.0'].text

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
            result.main_file_name = result['filename.0']
