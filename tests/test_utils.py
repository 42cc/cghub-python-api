import os
import unittest
import urllib2

from mock import patch
from StringIO import StringIO

from cghub_python_api.utils import urlopen


class UtilsTestCase(unittest.TestCase):

    TEST_URL = 'https://192.35.223.223/cghub/metadata/analysisDetail'
    TEST_QUERY = {
            'last_modified': '[NOW-64DAY+TO+NOW-63DAY]',
            'state': 'live'}
    TEST_FILE_PATH = os.path.join(
                            os.path.dirname(__file__),
                            'data/wsapi_details_10_results.xml')

    def test_urlopen(self):
        f = open(self.TEST_FILE_PATH, 'r')
        data = f.read()
        io = StringIO(data)
        with patch.object(urllib2, 'urlopen', return_value=io) as urllib2_urlopen_mock:
            url = '%s?%s' % (self.TEST_URL, '&'.join(
                    ['%s=%s' for key, value in self.TEST_QUERY.iteritems()]))
            f = urlopen(url=url)
            data = f.read()
            self.assertIn('<analysis_id>', data)
            self.assertEqual(urllib2_urlopen_mock.call_count, 1)

    def test_urlopen_repeat_requests_on_urlerror(self):
        def raise_urlerror(req):
            raise urllib2.URLError('URL Error message')
        with patch('urllib2.urlopen') as urllib2_urlopen_mock:
            urllib2_urlopen_mock.side_effect = raise_urlerror
            url = '%s?%s' % (self.TEST_URL, '&'.join(
                    ['%s=%s' for key, value in self.TEST_QUERY.iteritems()]))
            attempts_count = 3
            try:
                f = urlopen(url=url, max_attempts=attempts_count)
            except urllib2.URLError as e:
                self.assertIn('%d attempts' % attempts_count, str(e))
            self.assertEqual(urllib2_urlopen_mock.call_count, attempts_count)

    def test_error_message_on_bad_request(self):
        message = 'Bad request'
        def raise_httperror(req):
            raise urllib2.HTTPError(
                    url='http://example.com', code=400,
                    msg=message, hdrs=None, fp=None)
        with patch('urllib2.urlopen') as urllib2_urlopen_mock:
            urllib2_urlopen_mock.side_effect = raise_httperror
            url = '%s?%s' % (self.TEST_URL, '&'.join(
                    ['%s=%s' for key, value in self.TEST_QUERY.iteritems()]))
            attempts_count = 3
            try:
                f = urlopen(url=url, max_attempts=attempts_count)
            except urllib2.URLError as e:
                self.assertNotIn('%d attempts' % attempts_count, str(e))
                self.assertIn(message, str(e))
            self.assertEqual(urllib2_urlopen_mock.call_count, 1)


if __name__ == '__main__':
    unittest.main()
