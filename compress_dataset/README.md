# Dataset Generation #
This python script generates the data images and labels based on the raw data from ./benchmark/ \
The extracted data set are compressed and saved to the hdf5 file under ./data \
Run the script under UT-Anlay:
```
python  extract_feature.py
```

### Labeling ###
Layouts are labeled according to the rank percentile in the post layout performance simulation. The selected performance metric are as follows:

| Design | OTA1           | OTA2           | OTA3           | OTA4 | 
|:------:|:--------------:|:--------------:|:--------------:|:----:|
| Metric | Offset_Voltage | Offset_Voltage | Offset_Voltage | CMRR |

During label, we assign the worst 25% performance labeled as positive. For a balanced dataset, the best 25% performance would be labeled as negative. For an imbalanced dataset, the rest 75% good performance would be labeled as positive. \
The balanced OTA1 would be used for pretraining the model. The pretrained model would be then finetuned on the unbalanced datasets. 

![label][./../images/label.pdf]
