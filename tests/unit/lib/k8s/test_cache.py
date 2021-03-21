from labelbabel.lib.k8s import cache

import labelbabel.lib.k8s as k8s
import unittest

class CacheTestCase(unittest.TestCase):
    def test_message(self):
        c = cache.EventCache()
        self.assertEqual(c.message(), k8s.PodEvent('type', 'cluster', 'ns', 'name', 'labels', 'start_time', 'uid'))
