# fileName: configs/features.py
# copyright ©️ 2021 nabilanavab

import os

class(object):
    AIO = os.environ.get("AIO", True)
    OCR = os.environ.get("OCR", True)
    TEXT = os.environ.get("TEXT", True)
    ZOOM = os.environ.get("ZOOM", True)
    STOP = os.environ.get("STOP", False)
    SPLIT = os.environ.get("SPLIT", True)
    MERGE = os.environ.get("MERGE", True)
    IMAGE = os.environ.get("IMAGE", True)
    RENAME = os.environ.get("RENAME", True)
    ADD_PG = os.environ.get("ADD_PG", True)
    DIL_PG = os.environ.get("DIL_PG", True)
    ROTATE = os.environ.get("ROTATE", True)
    TXT2PDF = os.environ.get("TXT2PDF", True)
    WEB2PDF = os.environ.get("WEB2PDF", True)
    ENCRYPT = os.environ.get("ENCRYPT", True)
    DECRYPT = os.environ.get("DECRYPT", True)
    PDF2URL = os.environ.get("PDF2URL", True)
    FILTERS = os.environ.get("FILTERS", True)
    METADATA = os.environ.get("METADATA", True)
    WATERMARK = os.environ.get("WATERMARK", True)
    PDF_FORMAT = os.environ.get("PDF_FORMAT", True)
    COMPRESSION = os.environ.get("COMPRESSION", True)
