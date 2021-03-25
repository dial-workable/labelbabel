# -*- coding: utf-8 -*-

import hashlib
import collections
import labelbabel.lib.k8s.cache as cache

from typing import Dict, Generator
from kubernetes import client, config, watch  # type: ignore

__all__ = ["cache"]

PodEvent = collections.namedtuple(
    "PodEvent",
    [
        "type",
        "node_name",
        "cluster",
        "ns",
        "name",
        "labels",
        "start_time",
        "stop_time",
        "uid",
        "checksum",
    ],
)


class Scraper:
    """Scraper class is responsible to implement the code which collects the raw information from the k8s cluster and perform
    an initial conditioning on it.
    Currently Scaper collects all the pod information that is found in "PodEvent" named tuple of this package. Additionally
    it suppresses all the pod events comming from the cluster which do not change the info we are not interested in.
    """

    def __init__(self, cluster_name: str) -> None:
        config.load_kube_config()
        self._k8s_v1 = client.CoreV1Api()
        self._k8s_watch = watch.Watch()
        self._interrupt = False
        self._cluster_name = cluster_name
        self._cache = cache.EventCache()

    @classmethod
    def _calculate_hash(cls, pod_uid: str, pod_labels: Dict[str, str]) -> str:
        """_calculate_hash method calculates a hash from a given labelbabel.lib.k8s.PodEvent namedtuple.

        Args:
            event (labelbabel.lib.k8s.PodEvent): The event object for which we want to calculate the hash

        Returns:
            str: The calculated has is based on the uid and the labels of the given object. Ordering of the labels
                in the event do not matter.

        Args:
            pod_uid (str): The uid of pod
            pod_labels (Dict[str,str]): The labels dictonary of a returned pod

        Returns:
            str: The calculated hash based on the given uid and the labels. Ordering of the labels
                in the event does not matter.
        """
        hasher = hashlib.md5()

        hasher.update(pod_uid.encode("utf-8"))

        sorted_keys = [] if not pod_labels else sorted(pod_labels.keys())
        for k in sorted_keys:
            hasher.update(k.encode("utf-8"))
            hasher.update(pod_labels[k].encode("utf-8"))

        return hasher.hexdigest()

    def _get_pods(self) -> Generator[PodEvent, None, None]:
        """returns the pods by watching k8s cluster.

        Yields:
            labelbabel.lib.k8s.PodEvent: A namedtuple representing an event from the lifecycle of a pod (e.g. creation, deletion, modification)
        """
        self._interrupt = False
        while not self._interrupt:
            for event in self._k8s_watch.stream(
                self._k8s_v1.list_pod_for_all_namespaces
            ):
                if self._interrupt:
                    self._k8s_watch.stop()

                result = PodEvent(
                    event["type"],
                    event["object"].spec.node_name,
                    self._cluster_name,
                    event["object"].metadata.namespace,
                    event["object"].metadata.name,
                    event["object"].metadata.labels,
                    event["object"].status.start_time,
                    None,
                    event["object"].metadata.uid,
                    self._calculate_hash(
                        event["object"].metadata.uid, event["object"].metadata.labels
                    ),
                )

                yield result

    def get_events(self) -> Generator[PodEvent, None, None]:
        for p in self._get_pods():
            new_event = self._cache.add_event(p)
            if p.type == "DELETED":
                self._cache.remove_event(p)
            if new_event or p.type == "DELETED":
                yield p
