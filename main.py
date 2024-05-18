import mp4

with open("s.mp4", "rb") as f:
    while True:
        try:
            box = mp4.Box()
            box.size = int.from_bytes(f.read(4))
            box.name = f.read(4).decode()
            if box.size == 0:
                break
            print(box.size, box.name)
        except UnicodeDecodeError:
            print("Error!")
            # break
            f.read(box.size)
            continue
        if box.name == "ftyp":
            handled: mp4.FileTypeBox = mp4.hadle_ftyp(box, f)
            print("Handled",handled.name)
        elif box.name == "moov":
            print("!! moov detected !!")
            handled: mp4.MoovBox = mp4.handle_moov(box, f)
            print("Handled",handled.name)
        else:
            print("Cant handle", box.name, "box")
            f.read(box.size-8)