import sys
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
sys.path.append(BASE_DIR)

from HALO.data import TelemetryData
from HALO.core import AHG, Searcher
from HALO.config import Config

from bools.log import Logger

if __name__ == '__main__':
    Config.init(
        damping_score_threshold=0.999,
        sampling=2
    )
    data = pd.read_csv(f'{BASE_DIR}/static/test_data.csv')

    telemetry_data = TelemetryData(data, 'Failures', 'Successes')
    Logger.info(f'初始属性列表：{telemetry_data.attrs}\n')

    ahg = AHG(telemetry_data.attrs)
    ahg.extract(telemetry_data)
    search_paths = ahg.random_walk(telemetry_data)

    [Logger.info(comb) for comb in Searcher.search(telemetry_data, search_paths)]
