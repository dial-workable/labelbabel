from labelbabel.lib.k8s import cache

import labelbabel.lib.k8s as k8s
import unittest
import datetime

TEST_EVENT_DATA = [
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            {'app': 'application1', 'process': 'web'},
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            datetime.datetime(2021, 2, 13, 19, 15, 25),
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'c83cdafef94251b535616814c57da72e',
        ),
    },
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            {'process': 'web', 'app': 'application1'},
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            datetime.datetime(2021, 2, 13, 19, 15, 25),
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'c83cdafef94251b535616814c57da72e',
        ),
    },
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            {},
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            datetime.datetime(2021, 2, 13, 19, 15, 25),
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'fb78ccff9715954b486f6a2634209b2b',
        ),
    },
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            None,
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            None,
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'fb78ccff9715954b486f6a2634209b2b',
        ),
    },
]


TEST_EVENT_DATA_UNIQUE = [
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            {'process': 'web', 'app': 'application1'},
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            datetime.datetime(2021, 2, 13, 19, 15, 25),
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'c83cdafef94251b535616814c57da72e',
        ),
    },
    {
        'event': k8s.PodEvent(
            'MODIFY',
            'node1',
            'cluster',
            'ns',
            'name',
            {},
            datetime.datetime(2021, 2, 12, 18, 11, 5),
            datetime.datetime(2021, 2, 13, 19, 15, 25),
            'dsasdf-adsf-asdf-faf2323f4rdsfs-3432-f3fefs-3243fwefw',
            'fb78ccff9715954b486f6a2634209b2b',
        ),
    },
]


class CacheTestCase(unittest.TestCase):
    def test_cache_clearing(self) -> None:
        """test the cache clearing method
        The test load and clears the cache two time to catch possible regression errors in the cases
        where we add add items in a previously "cleared" cache.
        """
        c = cache.EventCache()

        # Load test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            c.add_event(data["event"])
            self.assertTrue(
                data["event"] in c,
                f"Item with index(zero-based) {count} should exist in the cache",
            )
            count += 1

        # Remove all test events
        c.clear()

        # Load test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            self.assertFalse(
                data["event"] in c,
                f"Item with index(zero-based) {count} should not exist in the cache",
            )
            self.assertTrue(
                c.add_event(data["event"]),
                f"Item with index(zero-based) {count} should be missing from the cache",
            )
            count += 1

        # Remove all test events
        c.clear()

        # Load test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            self.assertTrue(
                c.add_event(data["event"]),
                f"Item with index(zero-based) {count} should be missing from the cache after 2nd clearing",
            )
            count += 1

    def test_item_removal(self) -> None:
        """test the cache ability to "forget" an item
        """
        c = cache.EventCache()

        # Load test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            c.add_event(data["event"])
            self.assertTrue(
                data["event"] in c,
                f"Item with index(zero-based) {count} should exist in the cache",
            )
            count += 1

        # Remove test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            self.assertTrue(
                c.remove_event(data["event"]),
                f"Item with index(zero-based) {count} should exist in the cache in order to be removed",
            )
            self.assertFalse(
                c.remove_event(data["event"]),
                f"Item with index(zero-based) {count} should not exist in the cache after being removed",
            )
            count += 1

        # Load test events
        count = 0
        for data in TEST_EVENT_DATA_UNIQUE:
            c.add_event(data["event"])
            self.assertTrue(
                data["event"] in c,
                f"Item with index(zero-based) {count} should exist in the cache",
            )
            count += 1

        # Remove test events in reverse order
        count = 0
        for data in reversed(TEST_EVENT_DATA_UNIQUE):
            self.assertTrue(
                c.remove_event(data["event"]),
                f"Item with index(zero-based) {count} should exist in the cache in order to be removed",
            )
            self.assertFalse(
                c.remove_event(data["event"]),
                f"Item with index(zero-based) {count} should not exist in the cache after being removed",
            )
            count += 1
