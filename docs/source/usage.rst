.. About using the API

Usage
=====

WSI API
-------

Web service interface (WSI) to CGHub data is described in `CGHub documentation <https://cghub.ucsc.edu/help/help.html>`__
(look for `User's Guide`).
The Python API described in this documentation provides Python interface to it.

At the moment WSI API provides several metadata resources (``analysisId``, ``analysisDetail``, 
``analysisSubmission``, ``analysisFull``, ``analysisObject``, ``analysisAttributes``)

In the Python API wrapper ``analysisId``, ``analysisDetail`` and ``analysisFull`` are used now.
One may see example of possible responses for a specific id with HTTP requests as shown below:

https://cghub.ucsc.edu/cghub/metadata/analysisId?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

https://cghub.ucsc.edu/cghub/metadata/analysisDetail?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

https://cghub.ucsc.edu/cghub/metadata/analysisFull?aliquot_id=c0cfafbc-6d07-4ed5-bfdc-f5c3bf8437f6

Data can be returned in json or xml format.

The later returns more details for each query, while the former returns just enough information that could be used
by the download program.

In case of using WSI API, ``cghub_python_api.WSAPIRequest`` should be used.

SOLR API
--------

This package also can be used with `SOLR <http://lucene.apache.org/solr/>`__.

In case of using SOLR, ``cghub_python_api.SOLRRequest`` should be used.

Using Python API
----------------

Example:

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

.. code-block:: python

    >>> request = Request(query={'state': 'live', 'study': ['phs000178', '*Other_Sequencing_Multiisolate']}, limit=10)
    >>> for i in request.call():
    ...     print i
    ... 
    <cghub_python_api.api.Result object at 0x1c8d750>
    <cghub_python_api.api.Result object at 0x1ee11d0>
    <cghub_python_api.api.Result object at 0x1ee1c10>
    <cghub_python_api.api.Result object at 0x1ee4650>
    <cghub_python_api.api.Result object at 0x1ee9090>
    <cghub_python_api.api.Result object at 0x1ee9a90>
    <cghub_python_api.api.Result object at 0x1eed510>
    <cghub_python_api.api.Result object at 0x1eedf10>
    <cghub_python_api.api.Result object at 0x1ef1950>
    <cghub_python_api.api.Result object at 0x1ef8410>
    >>> request.hits
    45205
