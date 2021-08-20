import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__name__))))

from halo.data import TelemetryData
from halo.core import AHG

from bools.log import Logger

if __name__ == '__main__':
    data = pd.DataFrame({
        'Datacenter': ['DC1'] * 5 + ['DC2'] * 4,
        'OSVersion': ['V_1.1'] * 4 + ['V_1.2'] * 2 + ['V_1.3', 'V_1.3', 'V_1.4'],
        'Cluster': [f'PrdC0{n}' for n in [1, 1, 1, 2, 2, 3, 3, 4, 4]],
        'Node': [f'N0{n}' for n in [1, 1, 2, 3, 3, 4, 5, 6, 6]],
        'API': ['GET-FILES', 'POST-RESET', 'GET-FILES', 'GET-FILES', 'GET-RESET',
                'POST-PWD', 'GET-FILES', 'POST-RESET', 'GET-PWD'],
        'Failures': [180, 10, 150, 5, 0, 0, 5, 2, 20],
        'Successes': [220, 30, 160, 20, 20, 125, 120, 100, 220]
    })

    telemetry_data = TelemetryData(data, 'Failures', 'Successes')
    Logger.info(f'初始属性列表：{telemetry_data.attrs}\n')

    ahg = AHG(telemetry_data.attrs)
    ahg.extract(telemetry_data)

    Logger.info(f'Attribute Hierarchy Graph：{ahg.attrs}\n')
