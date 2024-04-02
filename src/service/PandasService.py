import pandas as pd
import numpy as np


class PandasService:
    def classification_evening_data(self, data_frame: pd.DataFrame, parser_name: str, set_min_max=True):
        new_columns = []

        if not parser_name == "간단이":
            for index, item in enumerate(list(data_frame.index)):
                time = int(data_frame.loc[item, '일시'].split(" ")[1].split(':')[0])
                if time >= 18:
                    new_columns.append(data_frame.loc[item, '소음레벨dB(A)'])
                    data_frame.loc[item, '소음레벨dB(A)'] = np.nan
                else:
                    new_columns.append(np.nan)

            data_frame['Atfter 18:00'] = new_columns

        if set_min_max:
            data_frame.loc['MIN'] = data_frame.min()
            data_frame.loc['MAX'] = data_frame.max()

        return data_frame

