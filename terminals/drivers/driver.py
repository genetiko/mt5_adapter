from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def instruments(self):
        pass

    @abstractmethod
    def instrument_data(self, instrument_id, instrument_type, start_time, end_time):
        pass

    @abstractmethod
    def shutdown(self):
        pass
