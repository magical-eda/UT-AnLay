import tensorflow as tf
import numpy as np
import sys
import cnn.cnn as cnn
from models.classifier import Classifier
import h5py

class dataset(object):
    def __init__(self):
        self.file = h5py.File("./data/data.hdf5", 'r')
        self.group = self.file['OTA1_Offset_Voltage_True']
        self.image = self.group['images']
        self.label = self.group['meta']
        self.testRatio = 0.2
        self.nofeat(True)
    def nofeat(self, deviceType=True):
        # Only contain nets and compacted layout, no device type embedding
        # deviceType flag if Flase would remove deviceType image intensity
        N = self.image.shape[0]
        self.data = np.zeros((N, 64, 64, 2))
        self.data[:,:,:,0] = self.image[:,:,:,0]/255.0
        if deviceType:
            self.data[:,:,:,1] = np.sum(self.image[:,:,:,1:6], axis=3).astype(float)
        else:
            self.data[:,:,:,1] = (np.sum(self.image[:,:,:,1:6], axis=3) > 0).astype(float)
    def nextBatch(self, num):
        """
        @brief get next batch data
        @param number of data points in a batch
        @return first: input image
        @return second: label
        """
        idx = np.arange(0, int(len(self.data)*(1-self.testRatio)))
        while True:
            np.random.shuffle(idx)
            for offset in range(0, len(idx), num):
                curr_idx = idx[offset:offset+num]
                dataShuffle = [self.data[i] for i in curr_idx]
                labelShuffle = [self.label[i][0] for i in curr_idx]
                yield dataShuffle, labelShuffle
    def batchTest(self):
        idx = np.arange(int(len(self.data)*(1-self.testRatio))+1 , len(self.data))
        data = [self.data[i] for i in idx]
        label = [float(self.label[i][0]) for i in idx]
        return data, label

def metric(tp, tn, fp, fn):
    tot = tp + tn + fp + fn
    acc = (tp + tn)/(tp + tn + fp + fn)
    prec = tp / (tp + fp)
    rec = tp / tp + fn
    f1 = 2*tp/(2*tp+fp+fn)
    FOR = fn / (fn + tn)
    return acc,prec,rec,f1,FOR
        
re_flags = tf.flags # flags for reconstructing task
re_flags.DEFINE_integer(
    "obs_dim", 64*64*2, "dimension of observation space")
re_flags.DEFINE_integer("img_ch", 2, "Number of channels in the input image")
re_flags.DEFINE_integer("num_labels", 2, "Number of labels")
re_flags.DEFINE_integer("batch_size", 16, "Batch size")
re_flags.DEFINE_integer("epochs", 500, "number of epoch")
re_flags.DEFINE_integer("updates_per_epoch", 64, "mini-batch")
FLAGS = re_flags.FLAGS


kwargs = {
    'batch_size': FLAGS.batch_size,
    'network': cnn.nofeat_2D,
    'observation_dim': FLAGS.obs_dim,
    'optimizer': tf.train.AdamOptimizer,
    "num_labels" : FLAGS.num_labels,
    "image_ch_dim" : FLAGS.img_ch
}

ds = dataset()
classifier = Classifier(**kwargs)
training_batch = ds.nextBatch(FLAGS.batch_size)

for epoch in range(FLAGS.epochs):
    trainingLoss = 0
    tp,tn,fp,fn = 0,0,0,0
    for _ in range(FLAGS.updates_per_epoch):
        x, label = next(training_batch)
        loss = classifier.update(x, label)
        trainingLoss += loss
        tpb,tnb,fpb,fnb = classifier.evaluate(x, label)
        tp += tpb
        tn += tnb
        fp += fpb
        fn += fnb
    trainAcc,trainPrec,_,_,trainFOR = metric(tp,tn,fp,fn)

    x_test, label_test = ds.batchTest()
    tp,tn,fp,fn = classifier.evaluate(x_test, label_test)
    testAcc,testPrec,_,_,testFOR = metric(tp,tn,fp,fn)
    
    trainingLoss /= FLAGS.updates_per_epoch
    s = "Loss: {: .4f}".format(trainingLoss)
    print(epoch, s)
    print("Training Accuracy = {:.4f}, Precision = {:.4f}, FOR = {:.4f}".format(trainAcc, trainPrec, trainFOR))
    print("Testing Accuracy = {:.4f}, Precision = {:.4f}, FOR = {:.4f}".format(testAcc, testPrec, testFOR))
classifier.done()

