"""
Service layer for restroom-adjacent business logic that doesn't belong in a
view or a model. Keeping it here means the PNR provider can be swapped
(e.g. for IRCTC's official partner API) without touching views.py.
"""
import hashlib
import random
from dataclasses import dataclass, field


@dataclass
class UpcomingStation:
    code: str
    name: str
    eta_minutes: int
    distance_km: float


@dataclass
class TrainRoute:
    pnr: str
    train_number: str
    train_name: str
    current_station: str
    upcoming_stations: list = field(default_factory=list)


class PNRLookupService:
    """
    NOTE (prototype): Indian Railways doesn't expose a free public PNR API,
    so this returns deterministic mock data keyed off the PNR string —
    the same PNR always returns the same "route" so the demo is stable.

    To go live, replace `get_train_route` with a call to a licensed PNR
    status provider (e.g. IRCTC's partner API) and keep the same return
    shape so nothing else in the codebase has to change.
    """

    _SAMPLE_STATIONS = [
        ("NDLS", "New Delhi"), ("GZB", "Ghaziabad"), ("MB", "Moradabad"),
        ("BE", "Bareilly"), ("LKO", "Lucknow"), ("CNB", "Kanpur Central"),
        ("ALD", "Prayagraj"), ("MGS", "Mughalsarai"), ("PNBE", "Patna"),
        ("HWH", "Howrah"),
    ]

    @classmethod
    def get_train_route(cls, pnr: str) -> TrainRoute:
        seed = int(hashlib.sha256(pnr.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)

        stations = rng.sample(cls._SAMPLE_STATIONS, k=min(5, len(cls._SAMPLE_STATIONS)))
        upcoming = [
            UpcomingStation(
                code=code,
                name=name,
                eta_minutes=(i + 1) * rng.randint(20, 60),
                distance_km=round((i + 1) * rng.uniform(15, 80), 1),
            )
            for i, (code, name) in enumerate(stations)
        ]

        return TrainRoute(
            pnr=pnr,
            train_number=str(10000 + seed % 9999),
            train_name=f"{stations[0][1]} - {stations[-1][1]} Express",
            current_station=stations[0][1],
            upcoming_stations=upcoming,
        )
