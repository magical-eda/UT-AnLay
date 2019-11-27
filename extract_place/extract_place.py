##
# @file extract_place.py
# @author Keren Zhu
# @date May 2019
# @brief The main part of the extracting placement into image project
#

import parser
import placement_ds as ds
import geometry as geo
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def export_grayscale_image(img, img_size, filename):
    #img_np = np.reshape(img, [img_size, img_size, 1])
    plt.imsave(filename, img, cmap = cm.gray)

class Extractor(object):
    def __init__(self):
        self._db = ds.Database()
        self._image_size = 64 # _image_size * _image_size outputs
    def parse(self, pfile, ffile, cfile, jfile):
        parse = parser.Parser(self._db)
        parse.parse_dot_pin_file(pfile)
        parse.parse_place_result_final(ffile)
        parse.parse_connection(cfile)
        parse.parse_device_type(jfile)
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


def main(pfile, ffile, cfile, jfile):
    """
    @param pfile: the .pin file
    @param ffile: the .result.final file
    @param cfile: the .connection file
    @param jfile: the device type json file
    """
    ex = Extractor()
    ex.parse(pfile, ffile, cfile, jfile)
    ex.export_device_type_placement(1, "/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/extracted/nmos.png")
    ex.export_device_type_placement(2, "/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/extracted/pmos.png")
    ex.export_device_type_placement(3, "/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/extracted/cap.png")
    ex.export_device_type_placement(4, "/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/extracted/res.png")
    ex.export_connect_net_bbox("/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/extracted/nets.png")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        main(pfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.pin",
             ffile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/DataTest/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.result.final",
             cfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.connection",
             jfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/device_type.json")
    else:
        main(pfile=sys.argv[1], ffile=sys.argv[2], cfile=sys.argv[3], jfile=sys.argv[4])

