from pandas import read_csv
data_directory = '/Users/adamhollin/downloads/'
filename = 'Scramble 4 7 22_retimed'
path_to_data_file = data_directory + filename + '.csv'
data = read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
print(data.head())

sample_size = 30000
offset_from_elan = int(99227)
outer_index = 1


def correct_drift():
    index_at_timestamp = int(data['timestamp'].loc[[offset_from_elan]]) * 100
    print("The number at index is:", index_at_timestamp)

    # offset_from_elan = int(offset_from_elan)  # Original offset

    if offset_from_elan > index_at_timestamp:
        diff = offset_from_elan - index_at_timestamp
    else:
        diff = index_at_timestamp - offset_from_elan

    new_offset = int(offset_from_elan) + int(diff)
    print("The new offset is:", new_offset)

    global start_point
    global end_point
    start_point = int(index_at_timestamp)
    end_point = int(index_at_timestamp + sample_size)


for outer_index in range(5):
    correct_drift()
#data.to_csv('/Users/adamhollin/Desktop/Scramble_',outer_index,'.csv')
    data_slice = data.iloc[start_point:end_point, :]

#    start_sample = end_sample
#   end_sample = start_sample + (window_size * sample_rate)

# output_name = f'Scramble_{n+1}.csv'
    output_name = f'/Users/adamhollin/Desktop/Scramble_{outer_index}.csv'
    first_timestamp = data_slice['timestamp'].iloc[0]
#    data_slice['timestamp'] = data_slice.loc['timestamp'] - first_timestamp
# current_slice = data[(data['timestamp'] >= start_time) & (data['timestamp'] <= end_time)]
    data_slice.to_csv(output_name, index=False, header=None)










#data.to_csv('/Users/adamhollin/Desktop/file_name.csv')