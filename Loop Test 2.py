from pandas import read_csv

data_directory = '/Users/adamhollin/downloads/'
filename = 'Arby_4_7_22.csv_retimed'
path_to_data_file = data_directory + filename + '.csv'
data = read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
print(data.head())

# Grab the offset from ELAN, drop the final digit and / 100
n_slices = 5
offset_on_elan = 1898.27
offset_from_elan = offset_on_elan * 100

index_at_timestamp = float(data['timestamp'].loc[[offset_from_elan]])
print('index_at_timestamp_is', index_at_timestamp)

if offset_from_elan > index_at_timestamp:
    diff = offset_from_elan - (index_at_timestamp * 100)
else:
    diff = index_at_timestamp - offset_from_elan
print('the difference is:', diff)

new_offset = int(offset_from_elan) + int(diff)
print('the new offset is:', new_offset)

for i in range(n_slices):

    start_point = new_offset
    end_point = new_offset + 30000
    print('the start point is:', start_point)

    data_slice = data.iloc[start_point:end_point]
    timestamp = data_slice['timestamp']
    print(data_slice)

    data_slice['timestamp'] = range(1, 1+len(data_slice))
    data_slice['timestamp'] = data_slice['timestamp'].div(100).round(3)

    data_slice.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
    data_slice.to_csv('/Users/adamhollin/Desktop/Arby' + str(i+1) + '.csv', index=False, header=None)

    print('The end point is:', end_point)

    num1 = int(end_point)
    new_offset = num1
