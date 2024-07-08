from dataclasses import dataclass, field
from helpers import standard_to_pygame, pygame_to_standard


@dataclass
class Chain:
    """
    Chain of points connected by segments.
    If closed, first and last point are connected.
    """
    closed: bool = False
    points: list[tuple[float, float]] = field(default_factory=lambda: [])

    def __json__(self):
        return self.__dict__

    @staticmethod
    def from_json(raw_data) -> "Chain":
        """
        Load from json data.
        Usage:
            chain = None
            with open("chain.json", "r") as f:
                chain = Chain.from_json(f)
        """
        return Chain(**raw_data)

    def add_point(self, point: tuple[float, float]):
        """
        Adds a point to the chain.
        """
        self.points.append(pygame_to_standard(point))

    def get_points(self):
        return [standard_to_pygame(p) for p in self.points]

    def close(self):
        """
        Closes the chain.
        This means that the first and last point will be connected.
        """
        self.closed = True

    def open(self):
        """
        Opens the chain.
        This means that the first and last point will not be connected.
        """
        self.closed = False
