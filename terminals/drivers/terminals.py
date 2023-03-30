from typing import Any, Dict, List


class Terminals:
    def __init__(self):
        self.__terminals: Dict[int, Driver]

    def __initialize(self):
        ...

    def __synchronize(self):
        ...

    def __shutdown(self):
        ...

    def __reset(self):
        ...

    def terminals(self) -> List[Driver]:
        ...

    def terminal_descriptors(self):
        ...

    def is_terminal_active(self):
        ...

    def terminal_info(self, terminal_id: int) -> Dict[str, Any]:
        ...
