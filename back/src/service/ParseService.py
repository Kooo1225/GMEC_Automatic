from abc import ABC, abstractmethod


class ParseService(ABC):
    @abstractmethod
    def extract_columns(self, table_list):
        pass

    @abstractmethod
    def conversion_error_value(self, non_columns_list):
        pass

    @abstractmethod
    def delete_other_value(self, conversion_error_list):
        pass

    @abstractmethod
    def classification_by_date(self, filtered_list):
        pass

    @abstractmethod
    def extract_location(self, classification_list):
        pass

    @abstractmethod
    def get_dict(self, classification_list, location_list):
        pass
