# -*- coding: utf-8 -*-

import labelbabel.lib.k8s as k8s
import unittest
import datetime

TEST_DATA_POD_EVENTS = [
    {
        'cluster': 'test-cluster-a',
        'ns': 'supernamespace',
        'name': 'apodname',
        'labels': {'label1': 'value1','label2': 'value2','label3': 'value3'},
        'start_time': datetime.datetime(2021,10,12,17,12,5),
        'stop_time': datetime.datetime(2021,10,12,16,10,4),
        'uid': 'dadf-adsf-asdf-asd-fa-sdf-asd',
    },
    {
        'cluster': 'test-cluster-a',
        'ns': 'supernamespace',
        'name': 'apodname',
        'labels': {'label1': 'value1','label2': 'value2','label3': 'value3'},
        'start_time': datetime.datetime(2021,10,12,17,12,5),
        'stop_time': None,
        'uid': 'dadf-adsf-asdf-asd-fa-sdf-asd',
    },
]



class PodEventTestCase(unittest.TestCase):
    def test_fields_positioning(self):
        """verify positioning of the PodEvent fields.
        The fields must be present and at the correct position.
        """
        for i in enumerate(TEST_DATA_POD_EVENTS):
            ds = i[1]
            e = k8s.PodEvent(
                ds['cluster'],
                ds['ns'],
                ds['name'],
                ds['labels'],
                ds['start_time'],
                ds['stop_time'],
                ds['uid'],
            )
            self.assertEqual(e.cluster, ds['cluster'], f'Processing data-set {i[0]}')
            self.assertEqual(e.ns, ds['ns'], f'Processing data-set {i[0]}')
            self.assertEqual(e.name, ds['name'], f'Processing data-set {i[0]}')
            self.assertEqual(e.labels, ds['labels'], f'Processing data-set {i[0]}')
            self.assertEqual(e.start_time, ds['start_time'], f'Processing data-set {i[0]}')
            self.assertEqual(e.stop_time, ds['stop_time'], f'Processing data-set {i[0]}')
            self.assertEqual(e.uid, ds['uid'], f'Processing data-set {i[0]}')