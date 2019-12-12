##
# @file extract_place.py
# @author Keren Zhu, Mingjie Liu
# @date May 2019
# @brief The main part of the extracting placement into image project
#

import parser
import placement_ds as ds
import geometry as geo

import os 
import glob

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

from tqdm import tqdm

def export_grayscale_image(img, img_size, filename):
    img_np = np.reshape(img, [img_size, img_size, 1])
    plt.imsave(filename, img, cmap = cm.gray, vmin=0, vmax=4)

class Extractor(object):
    def __init__(self):
        self._db = ds.Database()
        self._image_size = 64 # _image_size * _image_size outputs
    def parse(self, pfile, ffile, cfile, jfile, jchan=None):
        parse = parser.Parser(self._db)
        parse.parse_dot_pin_file(pfile)
        parse.parse_place_result_final(ffile)
        parse.parse_connection(cfile)
        parse.parse_device_type(jfile)
        if jchan:
            parse.parse_device_channel(jchan)
        self._db.initialize()
    def export_device_type_placement(self, device_type, filename):
        """
        @brief export device placements with given device_type into images
        @param device_type: the type of the devices
        @param filename: the filename of the output images
        """
        img = np.zeros((self._image_size, self._image_size), dtype=int)
        for dev_idx in range(0, self._db.num_devices()):
            device = self._db.device_idx(dev_idx)
            if device.device_type() !=  device_type:
                continue
            xl_px = self._db.circuit().pixel_x(device.x_lo()) 
            yl_px = self._db.circuit().pixel_y(device.y_lo())
            xh_px = self._db.circuit().pixel_x(device.x_hi())
            yh_px = self._db.circuit().pixel_y(device.y_hi())
            for x_px in range(xl_px, xh_px):
                for y_px in range(yl_px, yh_px):
                    img[y_px][x_px] += 1 # Increment the value
        export_grayscale_image(img, self._image_size, filename)
    def export_device_channel_placement(self, device_channel, filename):
        """
        @brief export device placements with given device_channel into images, device type automatically embeded
        @param device_channel: the channel to export
        @param filename: the filename of the output images
        """
        img = np.zeros((self._image_size, self._image_size), dtype=int)
        for dev_idx in range(0, self._db.num_devices()):
            device = self._db.device_idx(dev_idx)
            if not device_channel in device.device_channel():
                continue
            xl_px = self._db.circuit().pixel_x(device.x_lo()) 
            yl_px = self._db.circuit().pixel_y(device.y_lo())
            xh_px = self._db.circuit().pixel_x(device.x_hi())
            yh_px = self._db.circuit().pixel_y(device.y_hi())
            for x_px in range(xl_px, xh_px):
                for y_px in range(yl_px, yh_px):
                    img[y_px][x_px] = device.device_type() # Increment the value
        export_grayscale_image(img, self._image_size, filename)
    def export_connect_net_bbox(self, filename):
        """
        @brief try to catch the connectivity information into images
        @param filename: the file name of the output images
        """
        img = np.zeros((self._image_size, self._image_size), dtype=int)
        for net_idx in range(0, self._db.num_nets()):
            #print("Net ", net_idx)
            net = self._db.net_idx(net_idx)
            bbox = geo.Rect()
            for pin_idx in net.pin_list():
                pin = self._db.pin_idx(pin_idx)
                #print(pin.rect().to_str())
                bbox.union(pin.rect())
            #print("BBOX: ", bbox.to_str())
            xl_px = self._db.circuit().pixel_x(bbox.x_lo())
            yl_px = self._db.circuit().pixel_y(bbox.y_lo())
            xh_px = self._db.circuit().pixel_x(bbox.x_hi())
            yh_px = self._db.circuit().pixel_y(bbox.y_hi())
            for x_px in range(xl_px, xh_px):
                for y_px in range(yl_px, yh_px):
                    img[y_px][x_px] += 1 # Increment the value
        export_grayscale_image(img, self._image_size, filename)
        
def extract_feature(filedir, jfile):
    """
    Export different channels according to device type
    @param filedir: to design
    @param jfile: device type json file 
    """
    ex = Extractor()
    pfile = filedir + '/place.pin'
    ffile = filedir + '/place.result'
    cfile = filedir + '/place.connection'
    ex.parse(pfile, ffile, cfile, jfile)
    nmosfile = filedir + '/nmos.png'
    pmosfile = filedir + '/pmos.png'
    capfile = filedir + '/cap.png'
    resfile = filedir + '/res.png'
    netfile = filedir + '/nets.png'
    ex.export_device_type_placement(1, nmosfile)
    ex.export_device_type_placement(2, pmosfile)
    ex.export_device_type_placement(3, capfile)
    ex.export_device_type_placement(4, resfile)
    ex.export_connect_net_bbox(netfile)

def extract_feature_channel(filedir, jfile, jchan=None):
    """
    Export different channels based on subcircuit encodings, device type automatically embedded in intensity
    @param filedir: to design layout folder
    @param jfile: device type json file 
    @param jchan: device channel json file
    """
    ex = Extractor()
    pfile = filedir + '/place.pin'
    ffile = filedir + '/place.result'
    cfile = filedir + '/place.connection'
    ex.parse(pfile, ffile, cfile, jfile, jchan)
    chanfile_1 = filedir + '/first_stage.png'
    chanfile_2 = filedir + '/other_stage.png'
    chanfile_3 = filedir + '/fb.png'
    chanfile_4 = filedir + '/cmfb.png'
    chanfile_5 = filedir + '/bias.png'
    netfile = filedir + '/nets.png'
    ex.export_device_channel_placement(1, chanfile_1)
    ex.export_device_channel_placement(2, chanfile_2)
    ex.export_device_channel_placement(3, chanfile_3)
    ex.export_device_channel_placement(4, chanfile_4)
    ex.export_device_channel_placement(5, chanfile_5)
    ex.export_connect_net_bbox(netfile)

def main(benchmark_dir, path_to_json, circuit_name):
    """
    @param path_to_data: path to the benchmark folder
    @param path_to_json: path to the circuit json feature files
    @param circuit_name: name of the circuit
    """
    jfile = path_to_json + circuit_name + '.json'
    jchan = path_to_json + circuit_name + '.channel'
    path_to_data = benchmark_dir + circuit_name
    for layout_folder in tqdm(glob.glob(path_to_data + "/*")):
        extract_feature_channel(layout_folder, jfile, jchan)

