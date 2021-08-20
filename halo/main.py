import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
sys.path.append(BASE_DIR)

from halo.data import TelemetryData
from halo.core import AHG

from bools.log import Logger

if __name__ == '__main__':
    data = pd.read_csv(f'{BASE_DIR}/static/test_data.csv')

    telemetry_data = TelemetryData(data, 'Failures', 'Successes')
    Logger.info(f'初始属性列表：{telemetry_data.attrs}\n')

    ahg = AHG(telemetry_data.attrs)
    ahg.extract(telemetry_data)

    Logger.info(f'Attribute Hierarchy Graph：{ahg.attrs}\n')
