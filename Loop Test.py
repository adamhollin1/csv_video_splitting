from pandas import read_csv

data_directory = '/Users/adamhollin/downloads/'
filename = 'Copy of Arby 4 7 22_retimed'
path_to_data_file = data_directory + filename + '.csv'
data = read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
print(data.head())

# sample_size = 30000
# sample_rate = 100
# Grab the offset from ELAN, drop the final digit and / 100
n_slices = 5
n_samples = data.shape[0]

offset_on_elan = 1898.27
offset_from_elan = offset_on_elan * 100

slice_start = offset_from_elan
slice_end = slice_start + 30001
index_at_timestamp = float(data['timestamp'].loc[[offset_from_elan]]) * 100

for i in range(n_slices):

    #index_at_timestamp = float(data['timestamp'].loc[[offset_from_elan]])
    print('Index at timestamp is', index_at_timestamp)

    if offset_from_elan > index_at_timestamp:
        diff = offset_from_elan - (index_at_timestamp * 100)
    else:
     diff = index_at_timestamp - offset_from_elan
    print('the difference is', diff)

    new_offset = int(offset_from_elan) - int(diff)
    print('the new offset is:', new_offset)
    start_point = new_offset
    end_point = (start_point + 30001)

    data_slice = data.iloc[new_offset:end_point]

    timestamp = data_slice['timestamp']

    data_slice['timestamp'] = range(1, 1 + len(data_slice))
    data_slice['timestamp'] = data_slice['timestamp'].div(100).round(2)

    data_slice.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
    data_slice.to_csv('/Users/adamhollin/Desktop/Arby' + str(i+1) + '.csv', index=False, header=None)

    print('the end point is', end_point)

    new_start = int(data['timestamp'].loc[[end_point]]) * 100
    print('NEW START IS', new_start)
    print('end point is:', end_point)
    offset_from_elan = new_start
    end_point = new_start + 30000
    print(data_slice)
    print('new offset is:', new_offset)





