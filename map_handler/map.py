from dataclasses import dataclass, field
import json
import json_fix

from map_handler.chain import Chain


@dataclass
class Map:
    """
    Represents map data in object form
    """
    name: str = ""
    chains: list[Chain] = field(default_factory=lambda: [Chain()])

    def __json__(self):
        """
        Function called by the `json-fix` module.
        Converts class to a JSON-friendly format.
        """
        ret = self.__dict__
        chains = [chain.__json__() for chain in self.chains]
        ret["chains"] = chains
        return ret

    @staticmethod
    def from_json(raw_data) -> "Map":
        """
        Load from json data.
        Usage:
            map = None
            with open(MAP_FILE, "r") as f:
                map = Map.from_json(f)
        """
        data = json.load(raw_data)
        chains_raw = data["chains"]

        chains = [Chain.from_json(chain) for chain in chains_raw]
        data["chains"] = chains

        return Map(**data)

    def add_point(self, point: tuple[float, float], index: int = -1):
        """
        Adds a point to the chain at the given index (default = -1 -> last).
        """
        self.chains[index].add_point(point)

    def close_chain(self, index: int = -1):
        """
        Closes the chain at the given index (default = -1 -> last).
        This means that the first and last point will be connected.
        """
        self.chains[index].close()

    def open_chain(self, index: int = -1):
        """
        Opens the chain at the given index (default = -1 -> last).
        This means that the first and last point will not be connected.
        """
        self.chains[index].open()

    def add_chain(self):
        """
        Adds a new empty chain to the list.
        """
        self.chains.append(Chain())
