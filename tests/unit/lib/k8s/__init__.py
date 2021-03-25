# -*- coding: utf-8 -*-

import labelbabel.lib.k8s as k8s
import unittest
import datetime

TEST_DATA_POD_EVENTS = [
    {
        "type": "MODIFY",
        "node_name": "node1",
        "cluster": "test-cluster-a",
        "ns": "supernamespace",
        "name": "apodname",
        "labels": {"label1": "value1", "label2": "value2", "label3": "value3"},
        "start_time": datetime.datetime(2021, 10, 12, 17, 12, 5),
        "stop_time": datetime.datetime(2021, 10, 12, 16, 10, 4),
        "uid": "dadf-adsf-asdf-asd-fa-sdf-asd",
        "checksum": '14c833711bdbf8cdbef24e471ac41488',
    },
    {
        "type": "MODIFY",
        "node_name": "node1",
        "cluster": "test-cluster-a",
        "ns": "supernamespace",
        "name": "apodname",
        "labels": {"label1": "value1", "label2": "value2", "label3": "value3"},
        "start_time": datetime.datetime(2021, 10, 12, 17, 12, 5),
        "stop_time": None,
        "uid": "dadf-adsf-asdf-asd-fa-sdf-asd",
        "checksum": '14c833711bdbf8cdbef24e471ac41488',
    },
    {
        "type": "ADD",
        "node_name": "node2",
        "cluster": "test-cluster-b",
        "ns": "namespace",
        "name": "podname",
        "labels": {"label1": "value1", "label2": "value2", "label3": "value3"},
        "start_time": datetime.datetime(2021, 10, 12, 17, 12, 6),
        "stop_time": datetime.datetime(2021, 10, 12, 17, 12, 16),
        "uid": "dadf-adsf-asdf-asd-fa-sdf-asd",
        "checksum": '14c833711bdbf8cdbef24e471ac41488',
    },
    {
        "type": "MODIFY",
        "node_name": "node1",
        "cluster": "test-cluster-a",
        "ns": "supernamespace",
        "name": "apodname",
        "labels": {"label1": "value1", "label2": "value21", "label3": "value32"},
        "start_time": datetime.datetime(2021, 10, 12, 17, 12, 5),
        "stop_time": None,
        "uid": "dadf-adsf-asdf-asd-fa-sdf-asd",
        "checksum": '862db5091b054b864468edd40eff96bb',
    },
]
TEST_DATA_POD_EVENTS_UNIQUE_COUNT = 2


class PodEventTestCase(unittest.TestCase):
    def test_fields_positioning(self):
        """verify positioning of the PodEvent fields.
        The fields must be present and at the correct position.
        """
        for i in enumerate(TEST_DATA_POD_EVENTS):
            ds = i[1]
            e = k8s.PodEvent(
                ds["type"],
                ds["node_name"],
                ds["cluster"],
                ds["ns"],
                ds["name"],
                ds["labels"],
                ds["start_time"],
                ds["stop_time"],
                ds["uid"],
                ds["checksum"],
            )
            self.assertEqual(e.type, ds["type"], f"Processing data-set {i[0]}")
            self.assertEqual(e.cluster, ds["cluster"], f"Processing data-set {i[0]}")
            self.assertEqual(e.ns, ds["ns"], f"Processing data-set {i[0]}")
            self.assertEqual(e.name, ds["name"], f"Processing data-set {i[0]}")
            self.assertEqual(e.labels, ds["labels"], f"Processing data-set {i[0]}")
            self.assertEqual(
                e.start_time, ds["start_time"], f"Processing data-set {i[0]}"
            )
            self.assertEqual(
                e.stop_time, ds["stop_time"], f"Processing data-set {i[0]}"
            )
            self.assertEqual(e.uid, ds["uid"], f"Processing data-set {i[0]}")


class ScraperTestCase(unittest.TestCase):
    @classmethod
    def _get_pods_demo_data1(self):
        return [
            k8s.PodEvent(
                e["type"],
                e["node_name"],
                e["cluster"],
                e["ns"],
                e["name"],
                e["labels"],
                e["start_time"],
                e["stop_time"],
                e["uid"],
                e["checksum"],
            )
            for e in TEST_DATA_POD_EVENTS
        ]

    @classmethod
    def setUpClass(cls):
        cls._original_get_pods = k8s.Scraper._get_pods
        k8s.Scraper._get_pods = cls._get_pods_demo_data1

    @classmethod
    def tearDownClass(cls):
        k8s.Scraper._get_pods = cls._original_get_pods
        cls._original_get_pods = None

    def test_podevent_hash(self):
        """test the hashing algorithm for the PodEvent objects"""
        count = 0
        for data in TEST_DATA_POD_EVENTS:
            self.assertEqual(
                k8s.Scraper._calculate_hash(data['uid'], data['labels']),
                data['checksum'],
                f'Testing dataset with index(zero-based) {count}',
            )
            count += 1

    def test_scrape(self):
        """Validate if the scraper gets back the correct number of events"""
        s = k8s.Scraper("test-cluster-a")
        scraped_events = 0
        for e in s.get_events():
            scraped_events += 1
        self.assertEqual(scraped_events, TEST_DATA_POD_EVENTS_UNIQUE_COUNT)
