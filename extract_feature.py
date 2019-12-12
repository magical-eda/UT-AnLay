from extract_place import extract_place

benchmark_dir = './benchmark/'
path_to_json = './benchmark/JsonFile/'

OTA1 = 'Telescopic_Three_stage'
OTA2 = 'Telescopic_Three_stage_1'
OTA3 = 'Core_test_flow'
OTA4 = 'Core_FF'

print("Extracting Features for OTA1:", OTA1)
extract_place.main(benchmark_dir, path_to_json, OTA1)
print("Extracting Features for OTA2:", OTA2)
extract_place.main(benchmark_dir, path_to_json, OTA2)
print("Extracting Features for OTA3:", OTA3)
extract_place.main(benchmark_dir, path_to_json, OTA3)
print("Extracting Features for OTA4:", OTA4)
extract_place.main(benchmark_dir, path_to_json, OTA4)

