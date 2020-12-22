from enum import IntEnum
class packet_header(IntEnum):
    """headers to identify Packets"""
    FILE_TRANSFER_HEADER = 0x00
    FILE_TRANSFER_DATA = 55
