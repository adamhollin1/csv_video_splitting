from pandas import read_csv

data_directory = '/Users/adamhollin/downloads/'
filename = 'Arby_4_7_22.csv_retimed'
path_to_data_file = data_directory + filename + '.csv'
data = read_csv(path_to_data_file, header=None, names=['timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'])
print(data.head())

# sample_size = 30000
# sample_rate = 100
# Grab the offset from ELAN, drop the final digit and / 100
n_slices = 5
offset_on_elan = 1898.27
print('the offset visible on ELAN is:', offset_on_elan)

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

start_point = data.iloc[new_offset]
print(start_point)
end_point = data.iloc[new_offset + 30000]
print(end_point)

data_slice = data.iloc[start_point:end_point]
print(data_slice)





