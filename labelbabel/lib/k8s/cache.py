# -*- coding: utf-8 -*-

import labelbabel.lib.k8s as k8s

class EventCache():
    def __init__(self):
        self._cache = {}

    def add_event(self):
        return True

    def message(slef):
        return k8s.PodEvent('type', 'cluster', 'ns', 'name', 'labels', 'start_time', 'uid')