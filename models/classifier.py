import tensorflow as tf
import math
import numpy as np

class Classifier(object):
    def __init__(self, batch_size, network,
                 observation_dim=814,
                 learning_rate=3e-4,
                 optimizer=tf.train.AdamOptimizer,
                 image_ch_dim=1,
                 num_labels = 10,
                 decay_step=430,
                 decay_rate=0.9):

        self._batch_size = batch_size
        self._network = network
        self._observation_dim = observation_dim
        self._learning_rate = learning_rate
        self._optimizer = optimizer
        self._image_ch_dim = image_ch_dim
        self._decay_step = decay_step
        self._decay_rate = decay_rate
        self._num_labels = num_labels
        self._step = 0
        self._write_summary = False
        self._build_graph()

    def _build_graph(self):
        tf.reset_default_graph()
        dim = int(math.sqrt(self._observation_dim / self._image_ch_dim))

        with tf.variable_scope('cla'):
            self.x = tf.placeholder(tf.float32, shape=[None, dim, dim, self._image_ch_dim])
            self.y = tf.placeholder(tf.int64, (None))
            self.phase_train = tf.placeholder(tf.bool)

        with tf.variable_scope('nn', reuse=tf.AUTO_REUSE):
            logits = self._network(self.x, self.phase_train, self._observation_dim, self._image_ch_dim, self._num_labels)

        with tf.variable_scope('loss'):
            cross_entropy = self.soft_max_cross_entropy(logits, self.y)
            self._loss = cross_entropy + self.l2_regularization(0.1)

        with tf.variable_scope('evaluate'):
            predict = tf.argmax(logits, 1)
            actual =  tf.argmax(tf.one_hot(self.y, self._num_labels), 1)
            self._correctness = tf.equal(predict, actual)
            self._accuracy = tf.reduce_mean(tf.cast(self._correctness, tf.float32))
            self._tp = tf.cast(tf.count_nonzero(predict * actual), tf.float32)
            self._tn = tf.cast(tf.count_nonzero((predict - 1) * (actual - 1)), tf.float32)
            self._fp = tf.cast(tf.count_nonzero(predict * (actual - 1)), tf.float32)
            self._fn = tf.cast(tf.count_nonzero((predict - 1) * actual), tf.float32)

        with tf.variable_scope('lr_scheduler'):
            global_step = tf.Variable(0, trainable=False)
            self._decay_learning_rate = tf.train.exponential_decay(self._learning_rate, global_step,
                                                                   self._decay_step, self._decay_rate)
        with tf.variable_scope('optimizer'):
            optimizer = tf.train.AdamOptimizer(
                learning_rate=self._decay_learning_rate)

        with tf.variable_scope('training-step'):
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self._train = optimizer.minimize(self._loss)

        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5, allow_growth=True)
        self._sesh = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self._train_writer = tf.summary.FileWriter("./summaries/train", self._sesh.graph)
        init = tf.global_variables_initializer()
        tf.local_variables_initializer().run(session=self._sesh)
        self._sesh.run(init)

        tf.summary.scalar('loss', self._loss)
        self._merge =tf.summary.merge_all()

    def soft_max_cross_entropy(self, logits, labels):
        return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=tf.one_hot(labels, self._num_labels)))

    def l2_regularization(self, weight=0.2):
        vars = tf.trainable_variables()
        lossL2 = tf.add_n([tf.nn.l2_loss(v) for v in vars]) * weight
        return lossL2
    
    def update(self, x, y):
        if self._write_summary:
            _, loss, summ = self._sesh.run([self._train, self._loss, self._merge], feed_dict={ self.x: x, self.y: y, self.phase_train: True})
            self._train_writer.add_summary(summ, self._step)
        else:
            _, loss = self._sesh.run([self._train, self._loss], feed_dict={
                                     self.x: x, self.y: y, self.phase_train: True})
        self._step += 1
        return loss

    def evaluate(self, X_data, y_data):
        num_examples = len(X_data)
        tp,tn,fp,fn = 0,0,0,0
        for offset in range(0, num_examples, self._batch_size):
            batch_x, batch_y = X_data[offset:offset+self._batch_size], y_data[offset:offset+self._batch_size]
            tpb,tnb,fpb,fnb = self._sesh.run([self._tp, self._tn, self._fp, self._fn], feed_dict={self.x: batch_x, self.y: batch_y, self.phase_train: False})
            tp += tpb
            tn += tnb
            fp += fpb
            fn += fnb
        return tp, tn, fp, fn

    def reset_session(self):
        tf.reset_default_graph()

    def save_weights(self, path):
        print("Save weights to ", path)
        saver = tf.train.Saver()
        saver.save(self._sesh, path)
    
    def load_weights(self, path):
        print("Load weights from ", path)
        saver = tf.train.Saver()
        saver.restore(self._sesh, path)

    def done(self):
        self._train_writer.close()
        
