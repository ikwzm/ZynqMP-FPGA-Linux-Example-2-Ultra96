import numpy as np
import os

class Udmabuf:
    """A simple udmabuf class"""

    def __init__(self, name):
        self.name           = name
        self.device_name    = os.path.join('/', 'dev', self.name)
        self.class_path     = self.get_class_path(self.name)
        self.phys_addr      = self.get_value('phys_addr', 16)
        self.buf_size       = self.get_value('size')
        self.sync_offset    = None
        self.sync_size      = None
        self.sync_direction = None

    def get_class_path(self, name):
        for class_name in ['u-dma-buf', 'udmabuf']:
            class_path = os.path.join('/', 'sys', 'class', class_name, name)
            if os.path.exists(class_path):
                return class_path
        raise FileNotFoundError
        

    def get_value(self, name, radix=10):
        value = None
        for line in open(self.class_path + '/' + name):
            value = int(line, radix)
            break
        return value

    def set_value(self, name, value):
        f = open(self.class_path + '/' + name, 'w')
        f.write(str(value))
        f.close

    def memmap(self, dtype, shape):
        self.item_size = np.dtype(dtype).itemsize
        self.array     = np.memmap(self.device_name, dtype=dtype, mode='r+', shape=shape)
        return self.array

    def set_sync_area(self, direction=None, offset=None, size=None):
        if offset is None:
            self.sync_offset    = self.get_value('sync_offset')
        else:
            self.set_value('sync_offset', offset)
            self.sync_offset    = offset
            
        if size   is None:
            self.sync_size      = self.get_value('sync_size')
        else:
            self.set_value('sync_size', size)
            self.sync_size      = size

        if direction is None:
            self.sync_direction = self.get_value('sync_direction')
        else:
            self.set_value('sync_direction', direction)
            self.sync_direction = direction

    def set_sync_to_device(self, offset=None, size=None):
        self.set_sync_area(1, offset, size)

    def set_sync_to_cpu(self, offset=None, size=None):
        self.set_sync_area(2, offset, size)

    def set_sync_to_bidirectional(self, offset=None, size=None):
        self.set_sync_area(3, offset, size)

    def sync_for_cpu(self):
        self.set_value('sync_for_cpu', 1)

    def sync_for_device(self):
        self.set_value('sync_for_device', 1)

