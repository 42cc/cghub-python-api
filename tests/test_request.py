import os.path
import unittest
import urllib2

from StringIO import StringIO
from mock import patch

from cghub_python_api import WSAPIRequest, SOLRRequest


class RequestTestCase(unittest.TestCase):

    REQUEST_CLASS = WSAPIRequest
    TEST_FILE_PATH = os.path.join(
                            os.path.dirname(__file__),
                            'data/wsapi_details_10_results.xml')
    TEST_QUERY = {
                'last_modified': '[NOW-64DAY+TO+NOW-63DAY]',
                'state': 'live'}
    QUERY_TEST_DATA_SET = [
        {
            'query': {
                'study': ['phs000178', '*Other_Sequencing_Multiisolate', 'phs0004*'],
                'disease_abbr': ['BLCA', 'OR', 'BRCA'],
                'state': 'live'},
            'kwargs': {},
            'url': 'https://192.35.223.223/cghub/metadata/analysisDetail?'
            'study=%28phs000178%20OR%20%2AOther_Sequencing_Multiisolate%20OR%20phs0004%2A%29&'
            'disease_abbr=%28BLCA%20OR%20OR%20OR%20BRCA%29&state=live'
        }, {
            'query': {
                'study': '*Other_Sequencing_Multiisolate',
                'state': ['live'],
                'last_modified': '[NOW-1MONTH+TO+NOW]'},
            'kwargs': {},
            'url': 'https://192.35.223.223/cghub/metadata/analysisDetail?'
                'study=%2AOther_Sequencing_Multiisolate&'
                'last_modified=%5BNOW-1MONTH%20TO%20NOW%5D&state=%28live%29'
        }, {
            'query': {
                'study': '*Other_Sequencing_Multiisolate',
                'state': ['live']},
            'kwargs': {'limit': 10, 'offset': 10, 'sort_by': '-state'},
            'url': 'https://192.35.223.223/cghub/metadata/analysisDetail?'
                'study=%2AOther_Sequencing_Multiisolate&state=%28live%29&'
                'start=10&rows=10&sort_by=state:desc'
        }
    ]

    def _test_access_to_attributes(self, result):
        self.assertEqual(
                result.analysis_id.text,
                '3b4a2267-fafc-4185-ad44-bf0daadca912')
        self.assertEqual(
                result['analysis_id'].text,
                '3b4a2267-fafc-4185-ad44-bf0daadca912')
        self.assertEqual(result.analysis_id.exist, True)
        self.assertEqual(result['analysis_id'].exist, True)
        self.assertEqual(result.badattr.exist, False)
        self.assertEqual(result['badattr'].exist, False)
        self.assertEqual(result.badattr.text, None)
        file_attr = result['filename.0']
        self.assertTrue(file_attr.exist)
        self.assertTrue(file_attr.text.endswith('.bam'))
        file_attr = result['filename.1']
        self.assertTrue(file_attr.exist)
        self.assertTrue(file_attr.text.endswith('.bai'))

    def test_request(self):
        f = open(self.TEST_FILE_PATH, 'r')
        data = f.read()
        io = StringIO(data)
        with patch.object(urllib2, 'urlopen', return_value=io) as urllib2_urlopen_mock:
            request = self.REQUEST_CLASS(query=self.TEST_QUERY)
            results = []
            for result in request.call():
                results.append(result)
            self.assertEqual(len(results), 10)
            self.assertEqual(request.hits, 10)
            self._test_access_to_attributes(results[0])
            self.assertEqual(urllib2_urlopen_mock.call_count, 1)

    def test_request_build_query(self):

        f = open(self.TEST_FILE_PATH, 'r')
        data = f.read()
        io = StringIO(data)
        for data in self.QUERY_TEST_DATA_SET:
            io.seek(0)
            with patch.object(self.REQUEST_CLASS, 'get_xml_file', return_value=io) as get_xml_file_mock:
                request = self.REQUEST_CLASS(query=data['query'], **data['kwargs'])
                for i in request.call():
                    pass
                get_xml_file_mock.assert_called_once_with(data['url'])


class SOLRRequestTestCase(RequestTestCase):

    REQUEST_CLASS = SOLRRequest
    TEST_FILE_PATH = os.path.join(
                            os.path.dirname(__file__),
                            'data/solr_details_10_results.xml')
    QUERY_TEST_DATA_SET = [
        {
            'query': {
                'study': ['phs000178', '*Other_Sequencing_Multiisolate', 'phs0004*'],
                'disease_abbr': ['BLCA', 'OR', 'BRCA'],
                'state': 'live'},
            'kwargs': {},
            'url': 'http://127.0.0.1:8983/solr/select/?q=study%3A%28phs000178%20OR%20'
                '%2AOther_Sequencing_Multiisolate%20OR%20phs0004%2A%29+disease_abbr%3A%28BLCA%20'
                'OR%20OR%20OR%20BRCA%29+state%3Alive'
        }, {
            'query': {
                'study': '*Other_Sequencing_Multiisolate',
                'state': ['live'],
                'last_modified': '[NOW-1MONTH+TO+NOW]'},
            'kwargs': {},
            'url': 'http://127.0.0.1:8983/solr/select/?q=study%3A%2A'
                'Other_Sequencing_Multiisolate+last_modified%3A'
                '%5BNOW-1MONTH%20TO%20NOW%5D+state%3A%28live%29'
        }, {
            'query': {
                'study': '*Other_Sequencing_Multiisolate',
                'state': ['live']},
            'kwargs': {'limit': 10, 'offset': 10, 'sort_by': '-state'},
            'url': 'http://127.0.0.1:8983/solr/select/?q=study%3A%2A'
                'Other_Sequencing_Multiisolate+state%3A%28live%29&'
                'start=10&rows=10&sort=state+desc'
        }
    ]


if __name__ == '__main__':
    unittest.main()
