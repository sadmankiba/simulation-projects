from __future__ import annotations
from dataclasses import dataclass, field
import heapq
import enum
from typing import List, NamedTuple


@enum.unique
class EventKind(enum.Enum):
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"
    NONE = "NONE"

@dataclass
class Event:
    time: float 
    kind: EventKind 
    
@dataclass
class ArrivalEvent(Event):
    kind: EventKind = field(default= EventKind.ARRIVAL)

@dataclass
class DepartEvent(Event):
    kind: EventKind = field(default= EventKind.DEPARTURE)
    

class QueueEntry(NamedTuple):
    time: float
    event_id: int
    event: Event


class EvQueue:
    """A priority queue to store the simulation's pending events."""
    next_event_id: int = 0

    def __init__(self) -> None:
        self._queue: List[QueueEntry] = []

    def enqueue(self, e: Event):
        heapq.heappush(self._queue, QueueEntry(e.time, EvQueue.next_event_id, e))
        EvQueue.next_event_id += 1

    def dequeue(self) -> Event | None:
        if not self.empty():
            return heapq.heappop(self._queue).event

    def clear(self):
        self._queue = []

    def empty(self) -> bool:
        return not self._queue

    def __str__(self):
        return str(self._queue)
