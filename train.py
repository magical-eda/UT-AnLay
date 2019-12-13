import tensorflow as tf
import numpy as np
import sys
import coders.cnn_coding as coding
from models.classifier import Classifier
import h5py

class dataset(object):
    def __init__():
        self.file = h5py.File("./data/data.hdf5")
        self.group = self.file['OTA1_Offset_Voltage_True']
        self.data = self.group['image']
        self.label = self.group['label']
    def nextBatch(self, num):
        """
        @brief get next batch data
        @param number of data points in a batch
        @return first: input image
        @return second: label
        """
        idx = np.arange(0, int(len(self.img)*(1-self._testRatio)))
        while True:
            np.random.shuffle(idx)
            for offset in range(0, len(idx), num):
                curr_idx = idx[offset:offset+num]
                dataShuffle = [self.img[i] for i in curr_idx]
                labelShuffle = [self.label[i] for i in curr_idx]
                yield dataShuffle, labelShuffle

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
    'network': coding.cnn,
    'observation_dim': FLAGS.obs_dim,
    'optimizer': tf.train.AdamOptimizer,
    "num_labels" : FLAGS.num_labels,
    "image_ch_dim" : FLAGS.img_ch
}


classifier = Classifier(**kwargs)
training_batch = nextBatch(FLAGS.batch_size)

for epoch in range(FLAGS.epochs):
    trainingLoss = 0
    for _ in range(FLAGS.updates_per_epoch):
        x, label = next(training_batch)
        loss = classifier.update(x, label)
        trainingLoss += loss

    x_test, label_test = ds.batchTest()
    testAcc,testTP,testRecall = classifier.evaluate(x_test, label_test)
    
    trainingLoss /= FLAGS.updates_per_epoch
    s = "Loss: {: .4f}".format(trainingLoss)
classifier.done()

