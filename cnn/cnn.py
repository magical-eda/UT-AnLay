import tensorflow as tf
from tensorflow.contrib.layers import flatten

def nofeat_2D(x, phase_train=True, obs_dim=841, input_ch=1, num_labels=2):
    with tf.variable_scope("cnn"):
        conv1 = tf.layers.conv2d(x, 128, 5, padding='same',activation=tf.nn.relu)
        conv1 = tf.layers.max_pooling2d(conv1, 3, 2, )
        conv2 = tf.layers.conv2d(conv1, 64, 5, padding='same',activation=tf.nn.relu)
        conv2 = tf.layers.max_pooling2d(conv2, 3, 2)
        conv3 = tf.layers.conv2d(conv2, 32, 5, padding='same',activation=tf.nn.relu)
        conv3 = tf.layers.max_pooling2d(conv3, 3, 2)
        conv4 = tf.layers.conv2d(conv3, 32, 5, padding='same',activation=tf.nn.relu)
        conv4 = tf.layers.max_pooling2d(conv4, 3, 2)
        fc1 = tf.contrib.layers.flatten(conv4)
        fc1 = tf.layers.dense(fc1, 128)
        fc2 = tf.layers.dense(fc1, 16) 
        fc3 = tf.layers.dense(fc2, num_labels) 
    return fc3

def feat_2D(x, phase_train=True, obs_dim=841, input_ch=1, num_labels=2):
    with tf.variable_scope("cnn"):
        conv1_temp = []
        for i in range(input_ch):
            conv1_temp.append(tf.layers.conv2d(x[:,:,:,3*i:3*i+3], 24, 5, padding='same', activation=tf.nn.relu, kernel_initializer=tf.keras.initializers.he_normal()))
        conv1 = tf.concat(conv1_temp,axis=3)
        conv2 = tf.layers.conv2d(conv1, 64, 5, padding='same',activation=tf.nn.relu)
        conv2 = tf.layers.max_pooling2d(conv2, 3, 2)
        conv3 = tf.layers.conv2d(conv2, 32, 5, padding='same',activation=tf.nn.relu)
        conv3 = tf.layers.max_pooling2d(conv3, 3, 2)
        conv4 = tf.layers.conv2d(conv3, 32, 5, padding='same',activation=tf.nn.relu)
        conv4 = tf.layers.max_pooling2d(conv4, 3, 2)
        fc1 = tf.contrib.layers.flatten(conv4)
        fc1 = tf.layers.dense(fc1, 128, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 16, activation=tf.nn.relu) 
        fc3 = tf.layers.dense(fc2, num_labels) 
    return fc3


def nofeat_3D(x, phase_train=True, obs_dim=841, input_ch=1, num_labels=2):
    with tf.variable_scope("cnn"):
        conv1 = tf.layers.conv3d(x, 128, (3,5,5) , padding='same', activation=tf.nn.relu)
        conv1 = tf.layers.max_pooling3d(conv1, (1,3,3), (1,2,2))
        conv2 = tf.layers.conv3d(conv1, 64, (3,5,5), padding='same', activation=tf.nn.relu)
        conv2 = tf.layers.max_pooling3d(conv2, (1,3,3), (1,2,2))
        conv3 = tf.layers.conv3d(conv2, 32, (2,5,5), padding='same', activation=tf.nn.relu)
        conv3 = tf.layers.max_pooling3d(conv3, (1,3,3), (1,2,2))
        conv4 = tf.layers.conv3d(conv3, 32, (2,5,5), padding='same', activation=tf.nn.relu)
        conv4 = tf.layers.max_pooling3d(conv4, (1,3,3), (1,2,2))
        fc1 = tf.contrib.layers.flatten(conv4)
        fc1 = tf.layers.dense(fc1, 128, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 16, activation=tf.nn.relu) 
        fc3 = tf.layers.dense(fc2, num_labels) 
    return fc3

def feat_3D(x, phase_train=True, obs_dim=841, input_ch=1, num_labels=2):
    with tf.variable_scope("cnn"):
        conv1_temp = []
        for i in range(input_ch):
            conv1_temp.append(tf.layers.conv2d(x[:,:,:,3*i:3*i+3], 128, 5, padding='same', activation=tf.nn.relu, kernel_initializer=tf.keras.initializers.he_normal()))
        conv1 = tf.stack(conv1_temp,axis=1)
        conv2 = tf.layers.conv3d(conv1, 64, (3,5,5), padding='same', activation=tf.nn.relu)
        conv2 = tf.layers.max_pooling3d(conv2, (1,3,3), (1,2,2))
        conv3 = tf.layers.conv3d(conv2, 32, (3,5,5), padding='same', activation=tf.nn.relu)
        conv3 = tf.layers.max_pooling3d(conv3, (1,3,3), (1,2,2))
        conv4 = tf.layers.conv3d(conv3, 32, (2,5,5), padding='same', activation=tf.nn.relu)
        conv4 = tf.layers.max_pooling3d(conv4, (1,3,3), (1,2,2))
        fc1 = tf.contrib.layers.flatten(conv4)
        fc1 = tf.layers.dense(fc1, 128, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 16, activation=tf.nn.relu)
        fc3 = tf.layers.dense(fc2, num_labels) 
    return fc3

