import pandas as pd
from import_elan_annotations import EafParser


def get_data():
    path_to_data_file = 'data/Arby 4_7_22_retimed.csv'
    return pd.read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])


if __name__ == '__main__':

    data = get_data()
    # Todo: automate with eaf reader
    # path_to_eaf = "..."
    # eaf = EafParser(path_to_eaf)
    # offset_from_elan = eaf.time_origin

    # Grab the offset from ELAN, drop the final digit and / 100
    n_slices = 5
    sample_rate = 100
    slice_duration = 300
    slice_length = slice_duration * sample_rate
    offset_from_elan = 189827

    timestamp_at_offset = float(data['timestamp'].loc[[offset_from_elan]])

    print(f'timestamp at index: {timestamp_at_offset}')

    diff = abs(timestamp_at_offset - (offset_from_elan / 100))

    print(f'the difference is: {diff}')

    new_offset = (offset_from_elan / 100) + diff

    print(f'the new offset is: {new_offset}')

    data['timestamp'] = data['timestamp'] - timestamp_at_offset
    start_point = 0
    for i in range(n_slices):
        start_idx = data['timestamp'].searchsorted(start_point)
        end_idx = data['timestamp'].searchsorted(start_point + slice_duration)
        # start_point = new_offset
        # end_point = new_offset + slice_length

        print('the start point is:', start_point)

        data_slice = data.iloc[start_idx:end_idx]
        data_slice.index = pd.TimedeltaIndex(data_slice['timestamp'], unit='s')
        retimed_data_slice = data_slice.resample('10L').interpolate()
        retimed_data_slice['timestamp'] = round(retimed_data_slice['timestamp'] - retimed_data_slice['timestamp'][0], 2)
        print(retimed_data_slice)

        retimed_data_slice.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
        retimed_data_slice.to_csv(f'data/Arby_test_slice_{i}.csv', index=False, header=None)
        start_point = start_point + slice_duration + 0.01
