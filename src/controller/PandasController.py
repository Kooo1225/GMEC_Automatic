import pandas as pd
import numpy as np

from src.exception.CustomException import NoneException
from src.service.PandasService import PandasService


class PandasController:
    def __init__(self):
        self.service = PandasService()
        self.evening_data = None

    def get_dataframe(self):
        return self.evening_data

    def classification_evening_data_from_dataframe(self, dataframe, parser_name: str):
        self.evening_data = self.service.classification_evening_data(dataframe, parser_name)