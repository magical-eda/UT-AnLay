# Data Set #
The file data.hdf5 contains the following data:
- OTA1_Offset_Voltage_True
- OTA1_Offset_Voltage_False
- OTA2_Offset_Voltage_False
- OTA3_Offset_Voltage_False
- OTA4_CMRR_False

| Data                       | Metric         | Number| Positive| 
|:---------------------------|:---------------|:-----:|:-------:| 
| OTA1_Offset_Voltage_True   | Offset_Voltage | 16376 | 50% |
| OTA1_Offset_Voltage_False  | Offset_Voltage | 16376 | 25% |
| OTA2_Offset_Voletage_False | Offset_Voltage | 16381 | 25% |
| OTA3_Offset_Voltage_False  | Core_test_flow | 16384 | 25% |
| OTA4_CMRR_False            | Core_FF        | 16363 | 25% |

The current data does not contain coordinate embeddings. Run before training:
```
python prepare_dataset.py
```
