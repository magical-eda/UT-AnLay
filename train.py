import tensorflow as tf
import numpy as np
import cnn.cnn as cnn
from models.classifier import Classifier
from data import dataset
from util import metric
import argparse

parser = argparse.ArgumentParser(description='Placement quality prediction training.')
parser.add_argument('--design', help="Select design. Default is OTA1.", default='OTA1', type=str)
parser.add_argument('--balance', nargs='?', help="Balanced dataset. Default is False.", const=True, default=False)
parser.add_argument('--D3', nargs='?', help="Select cnn model using 3D convolution. Default is 2D.", const=True, default=False)
parser.add_argument('--nofeat', nargs='?', help='Select whether to embed features. Default is embedded feature.', const=True, default=False)
parser.add_argument('--finetune', nargs='?', help='Set finetune training parameters automatically.', const=True, default=False)
parser.add_argument('--epochs', help='Training epochs. Default is 500.',type=int,default=500)
parser.add_argument('--alpha', help="Training data usage rate. Default is 0.8.", default=0.8, type=float)
parser.add_argument('--updates_per_epoch', help='Updates per epoch. Default is 64.',type=int,default=64)
parser.add_argument('--batch_size', help='Batch Size. Default is 16.',type=int,default=16)
parser.add_argument('--load_weights', nargs='?', help='Specify file to load weights. Default would random initialize.',default=None,type=str)
parser.add_argument('--save_weights', nargs='?', help='Specify file to store weights. Default would not save.', default=None,type=str)
args = parser.parse_args()

# Design to performance labeling method
design_performance = {
    'OTA1' : 'Offset_Voltage',
    'OTA2' : 'Offset_Voltage', 
    'OTA3' : 'Offset_Voltage',
    'OTA4' : 'CMRR'
}

if args.D3:
    if args.nofeat:
        selected_model = cnn.nofeat_3D
        obs_dim = 64*64*2
        img_ch = 2
    else:
        selected_model = cnn.feat_3D
        obs_dim = 64*64*18
        img_ch = 18
else:
    if args.nofeat:
        selected_model = cnn.nofeat_2D
        obs_dim = 64*64*2
        img_ch = 2
    else:
        selected_model = cnn.feat_2D
        obs_dim = 64*64*18
        img_ch = 18

if args.finetune:
    args.epochs = 100
    args.updates_per_epoch = 64
    args.batch_size = 16
else:
    args.epochs = 500
    args.updates_per_epoch = 64
    args.batch_size = 16

kwargs = {
    'batch_size': args.batch_size,
    'network': cnn.feat_2D,
    'observation_dim': obs_dim,
    'optimizer': tf.train.AdamOptimizer,
    "num_labels" : 2,
    "image_ch_dim" : img_ch
}

ds_args = dict()
ds_args['design'] = args.design
ds_args['performance'] = design_performance[args.design]
ds_args['balance'] = args.balance
ds_args['alpha'] = args.alpha
ds_args['nofeat'] = args.nofeat
ds = dataset.dataset(ds_args)

classifier = Classifier(**kwargs)

training_batch = ds.nextBatch(args.batch_size)

if args.load_weights:
    classifier.load_weights(args.load_weights)

bestAcc = 0

for epoch in range(args.epochs):
    trainingLoss = 0
    tp,tn,fp,fn = 0,0,0,0
    for _ in range(args.updates_per_epoch):
        x, label = next(training_batch)
        loss = classifier.update(x, label)
        trainingLoss += loss
        tpb,tnb,fpb,fnb = classifier.evaluate(x, label)
        tp += tpb
        tn += tnb
        fp += fpb
        fn += fnb
    trainAcc,trainPrec,_,_,trainFOR = metric.metric(tp,tn,fp,fn)

    x_test, label_test = ds.batchTest()
    tp,tn,fp,fn = classifier.evaluate(x_test, label_test)
    testAcc,testPrec,_,_,testFOR = metric.metric(tp,tn,fp,fn)
    
    trainingLoss /= args.updates_per_epoch
    s = "Loss: {: .4f}".format(trainingLoss)
    print(epoch, s)
    print("Training Accuracy = {:.4f}, Precision = {:.4f}, FOR = {:.4f}".format(trainAcc, trainPrec, trainFOR))
    print("Testing Accuracy = {:.4f}, Precision = {:.4f}, FOR = {:.4f}".format(testAcc, testPrec, testFOR))

if args.save_weights:
    classifier.save_weights(args.save_weights)

classifier.done()

