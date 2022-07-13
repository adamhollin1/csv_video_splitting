from pandas import read_csv
data_directory = '/Users/adamhollin/downloads/'
filename = 'Copy of Arby 4 7 22_retimed'
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
    print('the difference is:', diff)

    new_offset = int(offset_from_elan) + int(diff)
    print('the new offset is:', new_offset)



# find the 'timestamp' at new offset, then add 300 to get the end of the slice.
    # then, use the 'timestamp' value at the end, and find the index value
    # use the index value as the start point for the next slice


    index_at_new_offset = float(data['timestamp'].loc[[new_offset]])
    print('index at new offset is:', index_at_new_offset)
    slice_end_timestamp = index_at_new_offset + 300
    print('slice end timestamp:', slice_end_timestamp)
    slice_end_timestamp = int(slice_end_timestamp)
    index_at_slice_end = data.loc[slice_end_timestamp]
    print('index at slice end is:', index_at_slice_end)






    start_point = new_offset
    end_point = (start_point + 30001)
    print('the start point is:', start_point)

    data_slice = data.iloc[start_point:end_point]
    timestamp = data_slice['timestamp']





    data_slice['timestamp'] = range(1, 1+len(data_slice))
    data_slice['timestamp'] = data_slice['timestamp'].div(100).round(2)

    data_slice.reset_index(level=None, drop=True, inplace=True, col_level=0, col_fill='')
    data_slice.to_csv('/Users/adamhollin/Desktop/Arby' + str(i+1) + '.csv', index=False, header=None)

    print('The end point is:', end_point)






    num1 = int(end_point)
    print('num 1 is:', num1)
    offset_at_index = float(data['timestamp'].loc[[num1]])
    print('the offset at index is:', offset_at_index)
    offset_from_elan = int(offset_at_index * 100)
    print(offset_from_elan)
