##
# @file compress.py
# @author Mingjie Liu
# @date July 2019
# @brief compress feature images to channel and label, save to hdf5 file format
#

import numpy as np
import glob
from scipy import misc
from tqdm import tqdm
import h5py

class compress(object):
    def __init__(self):
        # Dataset name
        self.name = 'OTA1'
        # Design layout path
        self.file = './benchmark/Telescopic_Three_stage/'
        # Label performance 
        self.label = 'Offset_Voltage'
        # Pruned Label percentile, will always be the majority label
        # if > 50 then prune from 0
        # if < 50 then prun to 100
        self.perc = 25
        # Whether dataset is balanced
        self.balance = True
    def setDesign(self, args):
        self.name = args['name']
        self.file = args['file']
        self.label = args['label']
        self.perc = args['perc']
        self.balance = args['balance']
    def getPerf(self, perfFile):
        performance = None
        with open(perfFile) as pf:
            for line in pf:
                split = line.split("=")
                if split[0] == self.label:
                    performance = float(split[1])
                    break
        assert performance, "Performance metric invalid"
        if self.label == 'Offset_Voltage':
            performance = abs(performance)
        return performance
    def loadData(self):
        fileList = glob.glob(self.file+'/*')
        N = len(fileList)
        # Obtain performance
        self.perf = list()
        self.labels = list()
        self.dataIdx = list()
        print("Loading performance from design", self.file)
        for path in tqdm(fileList):
            perfFile = path + '/performance.txt'
            self.perf.append(self.getPerf(perfFile))
        assert len(self.perf) == N, "Performance read error, length does not match"
        # Calculated critical performance 
        self.pos = self.perc
        self.neg = 100 - self.pos
        self.pos_crit = np.percentile(self.perf, self.pos)
        self.neg_crit = np.percentile(self.perf, self.neg)
        print("Labeling Data")
        for i, perf in enumerate(tqdm(self.perf)):
            # Boolean indicate if data saved
            save = True
            if self.balance:
                if self.pos < 50:
                    if perf <= self.pos_crit:
                        label = 1
                    elif perf >= self.neg_crit:
                        label = 0
                    else:
                        save = False
                else:
                    if perf <= self.neg_crit:
                        label = 0
                    elif perf >= self.pos_crit:
                        label = 1
                    else:
                        save = False
            else:
                if self.pos < 50:
                    label = int(perf <= self.pos_crit)
                else:
                    label = int(perf > self.pos_crit)
            if save:
                self.labels.append(label)
                self.dataIdx.append(i)
        N = len(self.labels)
        assert len(self.dataIdx) == N, "Balanced data, unmatched performance length"
        self.labels = np.array(self.labels).reshape((N,1))
        # Read all image files in path
        self.images = np.zeros((N, 64, 64, 6))
        index = 0
        print("Compressing images to channels")
        for i in tqdm(self.dataIdx):
            path = fileList[i]
            files = list()
        # Load images
            image = np.zeros((64,64,6))
            # Define image files to read
            files.append(path + "/nets.png")
            files.append(path + "/first_stage.png")
            files.append(path + "/other_stage.png")
            files.append(path + "/fb.png")
            files.append(path + "/cmfb.png")
            files.append(path + "/bias.png")
            # Read images
            for j, fileName in enumerate(files):
                image[:,:,j] = misc.imread(fileName, flatten=True, mode="L") 
            self.images[index,:,:,:] = image
            index += 1
        assert index == N, "Read images not matched"
    def embedCoord(self):
    # Apply coordinate channel embeddings to every channel
    # Resulting shape (N, 64, 64, 18)
        print("Embedding coordinate channels")
        N = len(self.labels)
        self.images_coord = np.zeros((N, 64, 64, 18))
        for i in tqdm(range(N)):
            curr_img = self.images[i,:,:,:]
            self.images_coord[i,:,:,0:18:3] = curr_img
            self.images_coord[i,:,:,1:18:3] = cordinate_img_x(curr_img)
            self.images_coord[i,:,:,2:18:3] = cordinate_img_y(curr_img)
    def saveData(self, hdf5):
        print("Saving to file", hdf5)
        f = h5py.File(hdf5, 'a')
        name = self.name + '_' + self.label + '_' + str(self.balance)
        print("Dataset group", name)
        grp = f.create_group(name)
        dataset = grp.create_dataset("images", self.images.shape, h5py.h5t.STD_U8BE, data=self.images, compression="gzip")
        metaset = grp.create_dataset("meta", self.labels.shape, h5py.h5t.STD_U8BE, data=self.labels, compression="gzip")
        f.close()
    def saveDesign(self, args, fileName):
        self.setDesign(args)
        self.loadData()
        self.saveData(fileName)
