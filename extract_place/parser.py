##
# @file parser.py
# @author Keren Zhu
# @date May 2019
# @brief Parser for extracting placement
#

import placement_ds as ds
import json

class Parser(object):
    def __init__(self, db):
        """
        @param a ds.Database object
        """
        self._db = db
        self.dum = 1000 # the unit for one um
    def parse_dot_pin_file(self, filename):
        """
        @brief read .pin file
        @param the filename for the .pin file
        """
        #macro_idx = -1
        with open(filename, 'r') as f:
            for line in f:
                words = line.split()
                length = len(words)
                if length == 1:
                    inst_name = words[0]
                    macro_idx = self._db.create_macro(inst_name)
                elif length == 2:
                    pin_name = words[0]
                    pin_idx = self._db.macro_idx(macro_idx).create_pin(pin_name)
                    num_shapes = int(words[1])
                else:
                    macro_pin = self._db.macro_idx(macro_idx).pin_idx(pin_idx)
                    # shapes will always be rectangles
                    for i in range(num_shapes):
                        layer = words[i*5]
                        xl = int(float(words[i*5+1].strip("()")) * self.dum)
                        yl = int(float(words[i*5+2].strip("()")) * self.dum)
                        xh = int(float(words[i*5+3].strip("()")) * self.dum)
                        yh = int(float(words[i*5+4].strip("()")) * self.dum)
                        macro_pin.add_shape(layer, xl, yl, xh, yh)
                    macro_pin.compute_bbox()

    def parse_place_result_final(self, filename):
        """
        @brief read .result.final file. The file with the coordinate of each device
        @param the filename for the .result.final
        """
        with open(filename, 'r') as f:
            for line in f:
                words = line.split()
                length = len(words)
                if length != 5:
                    print("Warning: read unexpected syntax in .result.final file", line)
                    continue
                device_name = words[0]
                xl = int(float(words[1]) * self.dum)
                yl = int(float(words[2]) * self.dum)
                xh = int(float(words[3]) * self.dum) + xl
                yh = int(float(words[4]) * self.dum) + yl
                idx = self._db.create_device(device_name) # the index of the device in the database
                device = self._db.device_idx(idx)
                device.set_rect(xl, yl, xh, yh)
        self.process_device_pin()

    def process_device_pin(self):
        """
        @brief after reading in the macro and device information, process the data
        """
        for device_idx in range(0, self._db.num_devices()):
            device = self._db.device_idx(device_idx)
            device_name = device.name() # In this version of flow, device name and macro name are identical
            macro = self._db.macro_name(device_name)
            for macro_pin in macro.pin_list():
                pin_idx = self._db.create_pin_device_idx(device_idx, macro_pin.name())
                pin = self._db.pin_idx(pin_idx)
                pin.init_with_macro_pin(macro_pin, device.x_lo(), device.y_lo())

    def parse_connection(self, filename):
        """
        @brief read .connection file. This file contains the information of connectivity in the level of pins
        @param the filename for the .connection
        """
        with open(filename, 'r') as f:
            for line in f:
                words = line.split()
                if len(words) <=1:
                    print("Warning: read unexpected syntax in .connection file", line)
                    continue
                netname = words[0]
                devices = []
                pins = []
                for pin_idx in range(0, (len(words) - 1) / 2):
                    device_name = words[1 + pin_idx *2]
                    pin_name = words[1 + pin_idx*2 + 1]
                    if pin_name == "B" or pin_name == "BULK":
                        continue
                    devices.append(device_name)
                    pins.append(pin_name)
                net_idx = self._db.create_net(netname)
                net = self._db.net_idx(net_idx)
                for idx in range(0, len(devices)):
                    device_name = devices[idx]
                    pin_name = pins[idx]
                    pin_idx = self._db.pin_idx_by_name_name(device_name, pin_name)
                    net.add_pin(pin_idx) # Add pin to net
                    self._db.pin_idx(pin_idx).set_net_idx(net_idx)

    def parse_device_type(self, filename):
        """
        @brief read the JSON file for the type of each devices
        @param the filename for the JSON file
        """
        with open(filename) as f:
            types = json.load(f)
            for device_name in types:
                device_type = types[device_name]
                device = self._db.device_name(device_name)
                if device_type == "NMOS":
                    device.set_type(1)
                elif device_type == "PMOS":
                    device.set_type(2)
                elif device_type == "CAP":
                    device.set_type(3)
                elif device_type == "RES":
                    device.set_type(4)
                else:
                    continue

def main(pfile, ffile, cfile, jfile):
    """
    @param pfile: the .pin file
    @param ffile: the .result.final file
    @param cfile: the .connection file
    @param jfile: the device type json file
    """
    db = ds.Database()
    parser = Parser(db)
    parser.parse_dot_pin_file(pfile)
    db.print_macros()
    parser.parse_place_result_final(ffile)
    parser.parse_connection(cfile)
    parser.parse_device_type(jfile)
    print(db._circuit.to_str())
    db.initialize()

if __name__ == '__main__':
    main(pfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.pin",
         ffile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/DataTest/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.result.final",
         cfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/Telescopic_Three_stage_flow.connection",
         jfile="/home/local/eda09/keren/projects/magical_place/magical/execution/results/Telescopic_Three_stage_flow/device_type.json")
