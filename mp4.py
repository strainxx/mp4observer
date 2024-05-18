from io import BufferedReader


class Box:
    """Base box class"""
    size: int # First 4 bytes (big endian)
    name: str # Next 4 bytes

class FileTypeBox(Box):
    """First mp4 box with basic info"""
    maj_brand: str # 4 bytes
    min_brand: str # 4 bytes
    compatible_brands: list # 16 bytes

class MvhdBox(Box):
    """Main metadata box"""
    flags: int
    version: int
    creation_time: int
    modification_time: int
    timescale: int
    duration: int
    rate: int
    volume: int

class MoovBox(Box):
    """ Box that contain nested boxes """
    mvhd: MvhdBox
    # TODO

def hadle_ftyp(raw_box: Box, f: BufferedReader):
    box: FileTypeBox = FileTypeBox()
    assert raw_box.name == "ftyp"
    box.name = raw_box.name
    box.size = raw_box.size
    box.maj_brand = f.read(4).decode()
    box.min_brand = int.from_bytes(f.read(4))
    print("Version:",box.maj_brand, box.min_brand)
    comp = f.read(raw_box.size-16).decode()
    box.compatible_brands = []
    for i in range(0,16, 4):
        box.compatible_brands.append(comp[i:i+4])
    print(box.compatible_brands)
    return box

def handle_moov(raw_box: Box, f: BufferedReader):
    box: MoovBox = MoovBox()
    assert raw_box.name == "moov"
    box.name = raw_box.name
    box.size = raw_box.size
    readed = 8
    while readed<=box.size-8:
        sub_box = Box()
        sub_box.size = int.from_bytes(f.read(4))
        sub_box.name = f.read(4).decode()
        if sub_box.name == "mvhd":
            boxdata = f.read(sub_box.size-8)
            mvhd = MvhdBox()
            mvhd.timescale = boxdata[12:16]
            mvhd.duration = boxdata[16:20]
            print("Timescale:", int.from_bytes(mvhd.timescale))
            print("Duration:", int.from_bytes(mvhd.duration), f"(RAW: {mvhd.duration.hex()})")
            print(f"VIDEO DURATION: {int.from_bytes(mvhd.duration)/int.from_bytes(mvhd.timescale)} seconds!")
            print("--(moov) Handled mvhd box!")
        else:
            print("--(moov) Cant handle", sub_box.name, "box")
            f.read(sub_box.size-8)
        readed+=sub_box.size
    return box