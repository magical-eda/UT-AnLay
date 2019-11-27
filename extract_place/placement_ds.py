##
# @file placement_ds.py
# @author Keren Zhu
# @date May 2019
# @brief Data structure for reading the Magical placement results
#

import geometry as geo

class Macro_pin(object):
    def __init__(self):
        self._name = ""
        self._layers = []
        self._shapes = []
        self._bbox = geo.Rect()
    def set_name(self, name):
        self._name = name
    def name(self):
        return self._name
    def add_shape(self, layer, x_lo, y_lo, x_hi, y_hi):
        self._layers.append(layer)
        self._shapes.append(geo.Rect(x_lo, y_lo, x_hi, y_hi))
    def layer(self, idx):
        return self._layers[idx]
    def shape(self, idx):
        return self._shapes[idx]
    def num_shapes(self):
        return len(self._shapes)
    def bbox(self):
        return self._bbox
    def compute_bbox(self):
        assert len(self._shapes) > 0
        """
        Here need a deep copy. Re-construct a new object for covenience
        """
        self._bbox = geo.Rect(self._shapes[0].x_lo(),  self._shapes[0].y_lo(), self._shapes[0].x_hi(), self._shapes[0].y_hi())
        for idx in range(1, len(self._shapes)):
            self._bbox.union(self._shapes[idx])
    def to_str(self):
        string = ""
        string += "name of shapes "
        string += str(len(self._layers)) + "    "
        for idx in range(len(self._layers)):
            string += " layer " + str(self._layers[idx])
            string += " shape " + self._shapes[idx].to_str()
        string += " bounding box " + self._bbox.to_str()
        return string


class Macro(object):
    def __init__(self):
        self._name = ""
        self._pins = []
        self._pin_name_map = {}
    def set_name(self, name):
        self._name = name
    def create_pin(self, name):
        """
        @brief create a new pin
        @param the name of the pin
        @return the inddx of the pin
        """
        self._pins.append(Macro_pin())
        self._pins[-1].set_name(name)
        self._pin_name_map[name] = len(self._pins) - 1
        return len(self._pins) - 1
    def pin_idx(self, idx):
        return self._pins[idx]
    def pin_name(self, name):
        idx = self._pin_name_map[name]
        return self.pin_idx(idx)
    def num_pins(self):
        return len(self._pins)
    def pin_list(self):
        return self._pins
    def to_str(self):
        string = ""
        string += "Macro name: "
        string += self._name
        string += "\n"
        for pin in self._pins:
            string += "Pin name " + pin.name() + "    "
            string += pin.to_str()
            string += "\n"
        return string
    

class Device(object):
    def __init__(self, name=""):
        self._name = name
        self._device_type = -1
        self._rect = geo.Rect()
        self._pin_list = []
        self._pin_name_map = {}
    def name(self):
        return self._name
    def set_type(self, device_type):
        self._device_type = device_type
    def device_type(self):
        return self._device_type
    def set_xy_lo(self, x_lo, y_lo):
        self._rect.set_ll(geo.XY(x_lo, y_lo))
    def set_xy_hi(self, x_hi, y_hi):
        self._rect.set_ur(geo.XY(x_hi, y_hi))
    def set_rect(self, x_lo, y_lo, x_hi, y_hi):
        self._rect = geo.Rect(x_lo, y_lo, x_hi, y_hi)
    def x_lo(self):
        return self._rect.x_lo()
    def y_lo(self):
        return self._rect.y_lo()
    def x_hi(self):
        return self._rect.x_hi()
    def y_hi(self):
        return self._rect.y_hi()
    def width(self):
        return self._rect.width()
    def height(self):
        return self._rect.height()
    def rect(self):
        return self._rect
    def add_pin(self, pin_idx, name):
        self._pin_list.append(pin_idx)
        self._pin_name_map[name] = len(self._pin_list) - 1
    def pin_list(self):
        return self._pin_list
    def num_pin(self):
        return len(self._pin_list)
    def pin_idx(self, idx):
        return self._pin_list[idx]
    def pin_name(self, pin_name):
        idx = self._pin_name_map[pin_name]
        return self._pin_list[idx]
    def to_str(self):
        string = ""
        string += "Type: "
        string += str(self._device_type)
        string += "\nBBOX: "
        string += self._rect.to_str()
        string += "\nPin indices: "
        for pin in self._pin_list:
            string += str(pin) + " " 
        return string

class Pin(object):
    def __init__(self):
        self._device_idx = -1
        self._rect = geo.Rect()
        self._net_idx = -1
        self._name = ""
    def set_name(self, name):
        self._name = name
    def name(self):
        return self._name
    def set_device_idx(self, device_idx):
        self._device_idx = device_idx
    def device_idx(self):
        return self._device_idx
    def set_xy_lo(self, x_lo, y_lo):
        self._rect.set_ll(geo.XY(x_lo, y_lo))
    def set_xy_hi(self, x_hi, y_hi):
        self._rect.set_ur(geo.XY(x_hi, y_hi))
    def set_rect(self, x_lo, y_lo, x_hi, y_hi):
        self._rect = geo.Rect(x_lo, y_lo, x_hi, y_hi)
    def rect(self):
        return self._rect
    def x_lo(self):
        return self._rect.x_lo()
    def y_lo(self):
        return self._rect.y_lo()
    def x_hi(self):
        return self._rect.x_hi()
    def y_hi(self):
        return self._rect.y_hi()
    def width(self):
        return self._rect.width()
    def height(self):
        return self._rect.height()
    def set_net_idx(self, net_idx):
        self._net_idx = net_idx
    def net_idx(self):
        return self._net_idx
    def init_with_macro_pin(self, macro_pin, offset_x, offset_y):
        """
        @brief initialize this pin with a Macro_pin object
        @param Macro_pin
        """
        self._rect = macro_pin.bbox()
        self._rect.offset_by(offset_x, offset_y)
    def to_str(self):
        string = ""
        return string

class Net(object):
    def __init__(self, name=""):
        self._pin_list = []
        self._name = name
    def name(self):
        return self._name
    def add_pin(self, pin_idx):
        self._pin_list.append(pin_idx)
    def pin_list(self):
        return self._pin_list
    def num_pin(self):
        return len(self._pin_list)
    def pin(self, idx):
        return self._pin_list[idx]
    def to_str(self):
        string = ""
        string += "Name: " + self._name + "\n  Pins in net:"
        for pin_idx in self._pin_list:
            string += str(pin_idx) + " "
        string += "\n"
        return string

class Circuit(object):
    def __init__(self):
        self._devices = []
        self._pins = []
        self._nets = []
        self._device_name_map = {}
        self._img_size = 64 # the size of the images
    def initialize(self):
        """
        @brief wrapper of the initialize functions
        """
        self.calculate_design_bbox() # Calculate the boundary for the design
    def calculate_design_bbox(self):
        """
        @brief Going through all the devices and find the boundary for the design
        """
        self._bbox = geo.Rect()
        for device in self._devices:
            self._bbox.union(device.rect())
    def set_img_size(self, img_size):
        self._img_size = img_size
    def scale_x(self, x):
        return x #TODO: add option to decides whether to scale
    def scale_y(self, y):
        return y #TODO: add option to decides whether to scale
    def pixel_x(self, x, img_size=None):
        """
        @brief which pixel in x this coordinate belongs to
        @param x: the x coordinate
        @param img_size: the size of the image. Default: self._img_size
        @return the index of the pixel
        """
        if img_size is None:
            img_size = self._img_size
        scale = self.scale_x(x)
        pixel =  (scale - self._bbox.x_lo()) * img_size / self._bbox.width()
        if pixel < 0:
            return 0
        elif pixel >= img_size:
            return img_size - 1
        else:
            return pixel
    def pixel_y(self, y, img_size=None):
        """
        @brief which pixel in y this coordinate belongs to
        @param x: the x coordinate
        @param img_size: the size of the image. Default: self._img_size
        @return the index of the pixel
        """
        if img_size is None:
            img_size = self._img_size
        scale = self.scale_y(y)
        pixel =  (scale - self._bbox.y_lo()) * img_size / self._bbox.height()
        if pixel < 0:
            return 0
        elif pixel >= img_size:
            return img_size - 1
        else:
            return pixel
    def pin_idx_by_name_name(self, device_name, pin_name):
        device_idx = self._device_name_map[device_name]
        pin_idx = self._devices[device_idx].pin_name(pin_name)
        return pin_idx
    def num_devices(self):
        return len(self._devices)
    def device_idx(self, idx):
        return self._devices[idx]
    def device_name(self, name):
        return self._devices[self._device_name_map[name]]
    def device_list(self):
        return self._devices
    def create_device(self, device_name):
        """
        @return: the idx of created device (was put in the end of the list)
        """
        self._devices.append(Device(name=device_name))
        idx = len(self._devices) - 1
        self._device_name_map[device_name] = idx
        #self._devices[-1].set_name(device_name)
        return idx
    def num_pins(self):
        return len(self._pins)
    def pin(self, idx):
        return self._pins[idx]
    def pin_list(self):
        return self._pins
    def create_pin_idx(self, device_idx, pin_name):
        """
        @return: the idx of the created pin (was put in the end of the list)
        """
        self._pins.append(Pin())
        pin_idx = len(self._pins) - 1
        self._pins[pin_idx].set_name(pin_name)
        self._devices[device_idx].add_pin(pin_idx, pin_name)
        return pin_idx
    def create_pin_name(self, device_name, pin_name):
        """
        @return: the idx of the created pin (was put in the end of the list)
        """
        device_idx = self._device_name_map[device_name]
        self._pins.append(Pin())
        pin_idx = len(self._pins) - 1
        self._pins.set_name(pin_name)
        self._devices[device_idx].add_pin(pin_idx, pin_name)
        return pin_idx
    def num_nets(self):
        return len(self._nets)
    def net(self, idx):
        return self._nets[idx]
    def net_list(self):
        return self._nets
    def create_net(self, netname):
        """
        @return: the idx of the created net (was put in the end of the list)
        """
        self._nets.append(Net(name=netname))
        return len(self._nets) - 1
    def to_str(self):
        string = ""
        string += "Number of devices: "
        string += str(self.num_devices()) + "\n"
        for device in self._devices:
            string += "Device: "
            string += device.to_str()
        #Net
        string += "\n Number of nets:"
        string += str(self.num_nets()) + "\n"
        for net in self._nets:
            string += "Net: "
            string += net.to_str()
        return string


class Database(object):
    def __init__(self):
        self._circuit = Circuit()
        self._macros = []
        self._macro_name_map = {}
        self._net_name_map = {}
    def initialize(self):
        """
        @brief wrapper of the initialize functions
        """
        self._circuit.initialize()
    def pin_idx(self, idx):
        """
        @brief get the pin object with index
        @return a pin object
        """
        return self._circuit.pin(idx)
    def create_pin_device_name(self, device_name, pin_name):
        """
        @brief create a new pin with device name
        @return the index of pin
        """
        return self._circuit.create_pin_name(device_name, pin_name)
    def create_pin_device_idx(self, device_idx, pin_name):
        """
        @brief create a new pin with device index
        @return the index of pin
        """
        return self._circuit.create_pin_idx(device_idx, pin_name)
    def create_device(self, device_name):
        """
        @param the name for the device
        @return the index of the created device in self._circuit
        """
        return self._circuit.create_device(device_name)
    def pin_idx_by_name_name(self, device_name, pin_name):
        return self._circuit.pin_idx_by_name_name(device_name, pin_name)
    def device_name(self, name):
        return self._circuit.device_name(name)
    def device_idx(self, idx):
        return self._circuit.device_idx(idx)
    def num_devices(self):
        return self._circuit.num_devices()
    def create_macro(self, macro_name):
        """
        @param the name for the macro
        @return the index of the created macro
        """
        self._macros.append(Macro())
        idx = len(self._macros) - 1
        self._macros[idx].set_name(macro_name)
        self._macro_name_map[macro_name] = idx
        return idx
    def macro_name(self, macro_name):
        return self._macros[self._macro_name_map[macro_name]]
    def macro_idx(self, macro_idx):
        return self._macros[macro_idx]
    def print_macros(self):
        for idx in range(len(self._macros)):
            print("Macro idx", idx)
            print(self._macros[idx].to_str())
    def create_net(self, netname):
        """
        @param the name for the net
        @return the index of the created net
        """
        net_idx = self._circuit.create_net(netname)
        self._net_name_map[netname] = net_idx
        return net_idx
    def net_idx(self, net_idx):
        return self._circuit.net(net_idx)
    def net_name(self, net_name):
        return self._circuit.net(self._net_name_map[net_name])
    def num_nets(self):
        return self._circuit.num_nets()
    def circuit(self):
        return self._circuit

