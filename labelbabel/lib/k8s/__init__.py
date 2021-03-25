# -*- coding: utf-8 -*-

import collections

from kubernetes import client, config, watch

__all__ = ["cache"]

PodEvent = collections.namedtuple(
    'PodEvent', ['type', 'cluster', 'ns', 'name', 'labels', 'start_time', 'stop_time', 'uid']
)


class Scraper:
    """Scraper class is responsible to implement the code which collects the raw information from the k8s cluster and perform
    an initial conditioning on it.
    Currently Scaper collects all the pod information that is found in "PodEvent" named tuple of this package. Additionally
    it suppresses all the pod events comming from the cluster which do not change the info we are not interested in.
    """

    def __init__(self, cluster_name):
        config.load_kube_config()
        self._k8s_v1 = client.CoreV1Api()
        self._k8s_watch = watch.Watch()
        self._interrupt = False
        self._cluster_name = cluster_name
        self._cache = {}

    def _get_pods(self):
        """returns the pods by watching k8s cluster.

        Yields:
            scraper.Event: The named tupple
        """
        self._interrupt = False
        while not self._interrupt:
            for event in self._k8s_watch.stream(
                self._k8s_v1.list_pod_for_all_namespaces
            ):
                if self._interrupt:
                    self._k8s_watch.stop()

                result = PodEvent(
                    event['type'],
                    self._cluster_name,
                    event['object'].metadata.namespace,
                    event['object'].metadata.name,
                    event['object'].metadata.labels,
                    event['object'].status.start_time,
                    None,
                    event['object'].metadata.uid,
                )

                yield result

    def get_events(self):
        for i in self._get_pods():
            yield i
