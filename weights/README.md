# Pretrained Models #
This contains two pretrained models on OTA1_Offset_Voltage_True. The data is on OTA1 with Offset_Voltage as the performance metric and having balanced training data. They are generated as follows:
```
python train.py --design OTA1 --balance --save_weights ./weights/OTA1_feat2D_pretrain.ckpt
python train.py --design OTA1 --balance --D3 --save_weights ./weights/OTA1_feat3D_pretrain.ckpt
```
