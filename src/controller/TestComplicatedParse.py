import numpy as np

from src.controller.ParserController import ParserController
import clipboard
import pandas as pd

from src.service.ComplicatedParser import ComplicatedParser
from src.service.SimpleParser import SimpleParser


def classification_evening_data(df):
    new_columns = []
    for index, item in enumerate(list(df.index)):
        time = int(df.loc[item, '일시'].split(" ")[1].split(':')[0])
        if time >= 18:
            new_columns.append(df.loc[item, '소음레벨dB(A)'])
            df.loc[item, '소음레벨dB(A)'] = np.nan
        else:
            new_columns.append(np.nan)

    df['Atfter 18:00'] = new_columns
    df.loc['MIN'] = df.min()
    df.loc['MAX'] = df.max()

    return df


clipboard_list = list(filter(lambda v: v, clipboard.paste().replace("\r\n", " ").split(" ")))


parser = SimpleParser()
test_case = ParserController(parser, clipboard_list)
test_case.run_parse()

print(test_case.get_result_dict())

df_list = [pd.DataFrame(test_case.get_result_dict()[i]).transpose() for i in test_case.get_result_dict()]
for item in df_list:
    print(classification_evening_data(item))
