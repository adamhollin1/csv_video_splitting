from pandas import read_csv
import datetime


data_directory = '/Users/adamhollin/downloads/'
filename = 'Arby_4_7_22.csv_retimed'
path_to_data_file = data_directory + filename + '.csv'
data = read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
print(data.head())

# sample_size = 30000
# Grab the offset from ELAN, drop the final digit and / 100
n_slices = 5
offset_on_elan = 1898.27
offset_from_elan = offset_on_elan * 100

for i in range(n_slices):
    index_at_timestamp = float(data['timestamp'].loc[[offset_from_elan]])
    print('index_at_timestamp_is', index_at_timestamp)

    if offset_from_elan > index_at_timestamp:
        diff = offset_from_elan - (index_at_timestamp * 100)
    else:
        diff = index_at_timestamp - offset_from_elan
# CHECK THIS LINE IT NEEDS TO BE AUTOMATED
    if diff > 421:
        diff = diff - 421

    print('the difference is:', diff)

    new_offset = int(offset_from_elan) + int(diff)
    print('the new offset is:', new_offset)

    timestamp_at_new_offset = (data['timestamp'].loc[new_offset])
    print('timestamp at new offset is:', timestamp_at_new_offset)
    slice_end_timestamp = timestamp_at_new_offset + 300
    print('slice end timestamp:', slice_end_timestamp)
    index_value = data.index[data.timestamp == int(slice_end_timestamp)]
    indices = data.index[data.timestamp == int(slice_end_timestamp)]
    index_value = indices[0]
    print('index value is:', index_value)

    start_point = new_offset
    end_point = index_value
    print('the start point is:', start_point)

    data_slice = data.iloc[start_point:end_point]
    timestamp = data_slice['timestamp']

    dup_test = data_slice.duplicated().sum()
    print('There are', dup_test, 'duplicates in the dataframe')
    good_samples = (~data_slice.duplicated()).sum()
    print('There are', good_samples, 'unique samples')
    new_df = data_slice.drop_duplicates(subset=None, keep='last', inplace=False)
    print(new_df)

    # Check dups in all columns instead of just timestamp

    new_df['timestamp'] = range(1, 1+len(data_slice))
    new_df.reset_index(level=None, drop=True, inplace=True, col_level=1, col_fill='')
    new_df['timestamp'] = new_df['timestamp'].div(100).round(2)
    new_df.to_csv('/Users/adamhollin/Desktop/Arby' + str(i+1) + '.csv', index=False, header=None)

    print('The end point is:', end_point)

    # After export, the following is adjusting the start to run the loop again:

    num1 = int(end_point)
    print('num 1 is:', num1)
    offset_at_index = float(data['timestamp'].loc[[num1]])
    print('the offset at index is:', offset_at_index)
    offset_from_elan = int(offset_at_index * 100)
    print('the offset from elan is:', offset_from_elan)

    # CHANGE THE FOLLOWING UP RESET TIMECODE OF VIDEO CLIPS
    timestamp_reset = timestamp_at_new_offset - 1898.26  # <THIS NUMBER
    timestamp_conversion = timestamp_reset
    print('conversion number is:', timestamp_conversion)
    x = float(timestamp_conversion)
    print(str(datetime.timedelta(seconds=x)) + ' start of slice ' + str(i + 1))

    duration = good_samples / 100
    print('the duration should be:', duration)
    y = float(duration)
    print(str(datetime.timedelta(seconds=y)) + ' duration of slice ' + str(i + 1))

    s = datetime.timedelta(seconds=x) + datetime.timedelta(seconds=y)
    str(s)
    print('Video end timestamp is:', s)






