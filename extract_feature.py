from extract_place import extract_place
from compress_dataset import compress

benchmark_dir = './benchmark/'
path_to_json = './benchmark/JsonFile/'
compressed_data = "./data/data.hdf5"

OTA1 = 'Telescopic_Three_stage'
OTA2 = 'Telescopic_Three_stage_1'
OTA3 = 'Core_test_flow'
OTA4 = 'Core_FF'

# Extract feature images
print("Extracting Features for OTA1:", OTA1)
extract_place.main(benchmark_dir, path_to_json, OTA1)
print("Extracting Features for OTA2:", OTA2)
extract_place.main(benchmark_dir, path_to_json, OTA2)
print("Extracting Features for OTA3:", OTA3)
extract_place.main(benchmark_dir, path_to_json, OTA3)
print("Extracting Features for OTA4:", OTA4)
extract_place.main(benchmark_dir, path_to_json, OTA4)


# Compress and data labeling
args = {
    "name" : "OTA1", 
    "file" : benchmark_dir + OTA1,
    "label" : "Offset_Voltage",
    "perc" : 75,
    "balance": True
}
print("Settings", args)
compressor = compress.compress()
compressor.saveDesign(args, compressed_data)

args['balance'] = False
print("Settings", args)
compressor = compress.compress()
compressor.saveDesign(args, compressed_data)

args['name'] = 'OTA2'
args['file'] = benchmark_dir + OTA2
print("Settings", args)
compressor = compress.compress()
compressor.saveDesign(args, compressed_data)

args['name'] = 'OTA3'
args['file'] = benchmark_dir + OTA3
print("Settings", args)
compressor = compress.compress()
compressor.saveDesign(args, compressed_data)

args['name'] = 'OTA4'
args['file'] = benchmark_dir + OTA4
args['label'] = "CMRR"
args['perc'] = 25
print("Settings", args)
compressor = compress.compress()
compressor.saveDesign(args, compressed_data)

