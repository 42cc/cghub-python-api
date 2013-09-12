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

API can get data from server in json format. To enable this option,
`format` variable should be set to Request.FORMAT_JSON:

.. code-block:: python

    >>> from cghub_python_api import WSAPIRequest as Request
    >>> request = Request(query={'state': 'live'}, format=Request.FORMAT_JSON, limit=1)
    >>> for i in request.call():
    ...     print i
    ... 
    {'upload_date': u'2013-05-16T00:00:09Z', 'center_name': u'BCCAGSC', 'aliquot_id': u'141c9cd0-719f-4591-bbd4-13b19b011540', 'disease_abbr': u'KIRP', 'sample_id': u'70e32971-74e6-4c92-8424-d10541d39360', 'analysis_id': u'0170e9db-e96b-4bfd-a35f-0391cd4b658a', 'sample_type': u'01', 'analysis_data_uri': u'https://test2.cghub.ucsc.edu/cghub/data/analysis/download/0170e9db-e96b-4bfd-a35f-0391cd4b658a', 'platform': u'ILLUMINA', 'state': u'live', 'participant_id': u'4d02010e-9e69-40d3-9bf0-3d4510aa0614', 'library_strategy': u'miRNA-Seq', 'files': [{'checksum': {'#text': u'87f71bf50596ee574b95b3069921476c', '@type': u'md5'}, 'filesize': 191879529, 'filename': u'TCGA-AL-3467-01A-02R-1350-13_mirna.bam'}, {'checksum': {'#text': u'bab77e2ae7ccbc385629efcdae292db1', '@type': u'md5'}, 'filesize': 4048968, 'filename': u'TCGA-AL-3467-01A-02R-1350-13_mirna.bam.bai'}], 'refassem_short_name': u'GRCh37-lite', 'reason': u'', 'last_modified': u'2013-05-16T20:43:40Z', 'analysis_submission_uri': u'https://test2.cghub.ucsc.edu/cghub/metadata/analysisSubmission/0170e9db-e96b-4bfd-a35f-0391cd4b658a', 'analyte_code': u'R', '@id': 1, 'study': u'phs000178', 'legacy_sample_id': u'TCGA-AL-3467-01A-02R-1350-13', 'sample_accession': u'', 'tss_id': u'AL', 'published_date': u'2013-05-16T00:05:05Z', 'analysis_full_uri': u'https://test2.cghub.ucsc.edu/cghub/metadata/analysisFull/0170e9db-e96b-4bfd-a35f-0391cd4b658a'}

Result format is different for xml/json options.
