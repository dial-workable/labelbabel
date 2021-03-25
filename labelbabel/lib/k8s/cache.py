# -*- coding: utf-8 -*-

from typing import Set

import labelbabel.lib.k8s as k8s


class EventCache:
    """EventCache is a class which is meant to act as a deduplication cache for PodEvent objects.
    It is primarily meant to be used by the labelbabel.lib.k8s.Scraper class to filter-out the
    pod modification events which are not modifying any fields we are interested in.
    """

    def __init__(self) -> None:
        self._cache: Set[str] = set()

    def add_event(self, event: k8s.PodEvent) -> bool:
        """add_event method is used to add a new event into the cache.
        The method calculates a hash form the data in the event to check if
        a similar object exists inside the cache.

        Args:
            event (labelbabel.lib.k8s.PodEvent): This is the event we are trying to add in the cache.

        Returns:
            bool: True if the added event has been successfully added.
                  False if the object was already in the cache.
        """
        if not isinstance(event, k8s.PodEvent):
            raise TypeError(
                "add_event method only accepts parameters of type labelbabel.lib.k8s.PodEvent"
            )

        if event.checksum not in self._cache:
            self._cache.add(event.checksum)
            return True

        return False

    def remove_event(self, event: k8s.PodEvent) -> bool:
        """remove_event method cand an event and remove/forget from the cache if it is sored in it

        Args:
            event (labelbabel.lib.k8s.PodEvent): The event to be removed from the cache

        Raises:
            TypeError: The method will throw a type error if the event parameter is of the wrond type.

        Returns:
            bool: True if the event has been found in the cache and removed.
                  False if the event has not been found in the cache, so there is nothing to remove.
        """
        if not isinstance(event, k8s.PodEvent):
            raise TypeError(
                "remove_event method only accepts parameters of type labelbabel.lib.k8s.PodEvent"
            )

        try:
            self._cache.remove((event.checksum))
        except KeyError:
            return False

        return True

    def clear(self) -> None:
        """clear method can be used to clear the cache from all the previously stored items."""
        self._cache = set()

    def __contains__(self, item: object) -> bool:
        """__contains__ magic method implementation allows us to use the "in" operator on the EventCache object"""
        return isinstance(item, k8s.PodEvent) and (item.checksum in self._cache)
