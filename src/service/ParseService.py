from abc import ABC, abstractmethod


class ParseService(ABC):
    @abstractmethod
    def extract_columns(self):
        pass

    @abstractmethod
    def conversion_error_value(self):
        pass

    @abstractmethod
    def classification_by_date(self):
        pass

    @abstractmethod
    def delete_other_value(self):
        pass

    @abstractmethod
    def extract_location(self):
        pass

    @abstractmethod
    def get_dict(self):
        pass
