import numpy as np
from tqdm import tqdm
import h5py
from util import cordinate_img

class dataset(object):
    def __init__(self, args=None):
        self.file = h5py.File("./data/data.hdf5", 'a')
        if args:
            group_name = args['design'] + '_' + args['performance'] + '_' + str(args['balance'])
            self.alpha = args['alpha']
        else:
            group_name = 'OTA1_Offset_Voltage_True'
            self.alpha = 0.8
        self.group = self.file[group_name]
        self.image = np.array(self.group['images'])
        self.label = np.array(self.group['meta'])
        self.testRatio = 0.2
        if args['nofeat']:
            self.nofeat()
        else:
            self.feat()
        self.file.close()
    def __del__(self):
        self.file.close()
    def nofeat(self):
        # Only contain nets and compacted layout
        # Data shape (N, 64, 64, 2)
        # Channel 0: net.png
        # Channel 1: entire layout
        # The model should be cnn.nofeat_2D or cnn.nofeat_3D
        N = self.image.shape[0]
        self.data = np.zeros((N, 64, 64, 2))
        self.data[:,:,:,0] = self.image[:,:,:,0] 
        self.data[:,:,:,1] = np.sum(self.image[:,:,:,1:6], axis=3).astype(float)
    def feat(self):
        # This include all features: deviceType, seperate Channels and coordinate embeddings
        # Data shape (N, 64, 64, 18)
        # Channel 0-2: net.png with coordinate channels
        # Channel 3-5: first_stage.png with coordinate channels
        # etc..
        # The model should be cnn.feat_2D or cnn.feat_3D
        N = self.image.shape[0]
        self.data = np.zeros((N, 64, 64, 18))
        if 'images_coord' in self.group:
            print("Found coordinate embedded")
            self.image_coord = np.array(self.group['images_coord'])
        else:
            self.embedCoord()
        self.data = self.image_coord 
    def embedCoord(self):
    # Apply coordinate channel embeddings to every channel
    # Resulting shape (N, 64, 64, 18)
        print("Embedding coordinate channels")
        N = len(self.label)
        self.image_coord = np.zeros((N, 64, 64, 18))
        for i in tqdm(range(N)):
            curr_img = self.image[i,:,:,:]
            self.image_coord[i,:,:,0:18:3] = curr_img
            self.image_coord[i,:,:,1:18:3], self.image_coord[i,:,:,2:18:3] = cordinate_img(curr_img)
        dataset_embed = self.group.create_dataset("images_coord", self.image_coord.shape, h5py.h5t.STD_U8BE, data=self.image_coord, compression="gzip")
    def nextBatch(self, num):
        """
        @brief get next batch data
        @param number of data points in a batch
        @return image, label
        """
        idx = np.arange(0, int(len(self.data)*self.alpha))
        while True:
            # Random batch input
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
