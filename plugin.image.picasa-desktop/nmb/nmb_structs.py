
import struct

class NMBError(Exception): pass


class NMBSessionMessage:

    HEADER_STRUCT_FORMAT = '>BBH'
    HEADER_STRUCT_SIZE = struct.calcsize(HEADER_STRUCT_FORMAT)

    def __init__(self):
        self.reset()

    def reset(self):
        self.type = 0
        self.flags = 0
        self.data = ''

    def decode(self, data, offset):
        data_len = len(data)

        if data_len < offset + self.HEADER_STRUCT_SIZE:
            # Not enough data for decoding
            return 0

        self.reset()
        self.type, self.flags, length = struct.unpack(self.HEADER_STRUCT_FORMAT, data[offset:offset+self.HEADER_STRUCT_SIZE])

        if self.flags & 0x01:
            length |= 0x010000

        if data_len < offset + self.HEADER_STRUCT_SIZE + length:
            return 0

        self.data = data[offset+self.HEADER_STRUCT_SIZE:offset+self.HEADER_STRUCT_SIZE+length]
        return self.HEADER_STRUCT_SIZE + length
