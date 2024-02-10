import logging
from typing import List
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np
import pandas as pd

from events import EvQueue, ArrivalEvent, DepartEvent, EventKind

logging.basicConfig(level="ERROR")

# Single server queue simulation
# Interarrival time ~ Exp(1)
# Service time ~ [Exp(0.5), Exp(0.6), Exp(0.7), Exp(0.8), Exp(0.9)]
# Simulate for 1000 customers
# Stop simulation when 1000 customers have departed
# Observations:
  # Avg delay in queue grows exponentially with service time
  # When service time < interarrival time
    # server util = service time / interarrival time
    # total sim time = number of customers * interarrival time
  # When service time > interarrival time
    # server util = 1
    # total sim time ~ number of customers * service time

class ServerState:
    IDLE = auto()
    BUSY = auto()

@dataclass
class Customer:
    arv_time: float

class Sim:
    def __init__(self, it, st):
        self.MAX_CUSTM = 1000
        self._interarv_tm = it
        self._serv_tm = st
        self.clock = 0.0
        self._evq = EvQueue()
        self._serv_state = ServerState.IDLE
        self._evq.enqueue(ArrivalEvent(self.gen_random(self._interarv_tm)))
        self._cq: List[Customer] = list()
        self._n_custm_arvd = 0
        self.total_q_tm = 0
        self.total_serv_tm = 0
        
    def time_adv(self):
        while True:
            nxtev = self._evq.dequeue()
            if nxtev is not None:
                self.clock = nxtev.time
                logging.info("[" + str(round(self.clock, 2)) + "]:" + str(nxtev))

                if nxtev.kind == EventKind.ARRIVAL:
                    self._arrival()
                elif nxtev.kind == EventKind.DEPARTURE:
                    self._depart()
            else:
                break

    def _arrival(self):
        cs = Customer(self.clock)
        self._n_custm_arvd += 1
        # Allow maximum 1000 customers to arrive
        if self._n_custm_arvd < self.MAX_CUSTM: 
            self._evq.enqueue(
                ArrivalEvent(self.clock + self.gen_random(self._interarv_tm))
            )

        if self._serv_state == ServerState.IDLE:
            self._serv_state = ServerState.BUSY
            serv_tm = self.gen_random(self._serv_tm)
            self._evq.enqueue(DepartEvent(self.clock + serv_tm))
            self.total_serv_tm += serv_tm

        else:
            self._cq.append(cs)

        logging.info(
            f"[{str(round(self.clock, 2))}]: Arrive. Queue len {len(self._cq)}"
        )

    def _depart(self):
        self._serv_state = ServerState.IDLE

        if len(self._cq) > 0:
            cs = self._cq.pop(0)
            self.total_q_tm += self.clock - cs.arv_time
            self._serv_state = ServerState.BUSY
            serv_tm = self.gen_random(self._serv_tm)
            self._evq.enqueue(DepartEvent(self.clock + serv_tm))
            self.total_serv_tm += serv_tm

        logging.info(
            f"[{str(round(self.clock, 2))}]: Depart. Queue len {len(self._cq)}"
        )

    def gen_random(self, expected: float):
        return -np.log(1 - (np.random.uniform(low=0.0, high=1.0))) * expected


if __name__ == "__main__":
    df = pd.DataFrame(
        columns=[
            "Interarrival time (mins)",
            "Service time (mins)",
            "Avg delay in queue (mins)",
            "Server utilization (mins)",
            "Total sim time (mins)",
        ]
    )

    interarv_time = 1
    N_SIM = 5
    for serv_time in [0.5, 0.6, 0.7, 0.8, 0.9]:
        logging.info(f"IT {interarv_time}, ST {serv_time}")
        avg_delay = 0
        serv_util = 0
        total_time = 0
        for _ in range(N_SIM):
            sim = Sim(interarv_time, serv_time)
            sim.time_adv()
            avg_delay += sim.total_q_tm / sim.MAX_CUSTM
            serv_util += sim.total_serv_tm / sim.clock
            total_time += sim.clock

        new_row = pd.Series(
            [
                interarv_time,
                serv_time,
                round(avg_delay / N_SIM, 2),
                round(serv_util / N_SIM, 2),
                round(total_time / N_SIM, 2),
            ],
            index=df.columns,
        )
        df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        
    df.to_csv("metrics.csv", index=False)

    exp = np.array([ np.random.exponential(1) for _ in range(100) ])
    print(f"Exp: min {np.min(exp)}, max {np.max(exp)}, median {np.median(exp)}")
    uni = np.array([ np.random.uniform() for _ in range(100) ])
    print(f"Uni: min {np.min(uni)}, max {np.max(uni)}, median {np.median(uni)}")