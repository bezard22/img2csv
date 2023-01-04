import os
import argparse
import cv2

def parseArgs() -> None:
    """Parse command line arguments, perfrom error checking, return dict containgin args.

    :raises SystemExit: srs file not found
    :raises SystemExit: dst file alreadu exists
    """    
    parser = argparse.ArgumentParser(prog="img2csv", description="convert an image to a csv")

    parser.add_argument("src", help="Path to file containing image")
    parser.add_argument("dst", nargs="?", help="Path to destination file")
    parser.add_argument("-m", "--mode", help="Color mode, default='RGB'", default="GRAY", type=str.upper, choices=["RGB", "HSV", "GRAY"])
    # TODO implement reverse mode
    # parser.add_argument("-r", "--reverse", help="rever flag, csv to image" action="store_true")
    parser.add_argument("-s", "--sep", help="Seperator, default=','", default=",")
    args = vars(parser.parse_args())

    if not os.path.exists(args["src"]):
        raise SystemExit(f'file: "{args["src"]}" does not exist')
    if args["dst"] is not None and os.path.exists(args["dst"]):
        raise SystemExit(f'file: "{args["dst"]}" already exists')

    return args

def convert(img, mode: str, sep: str):
    """Convert provided image to a csv string.

    :param img: image to be converted
    :type img: cv2.image
    :param mode: color mode
    :type mode: str
    :param sep: delimiter for csv file
    :type sep: str
    :return: csv string representation of image
    :rtype: str
    """    
    imgString = ""

    if mode == "RGB":
        title = ["Blue\n", "Green\n", "Red\n"]
        for i in range(3):
            imgString += title[i]
            for row in img:
                imgString += sep.join([str(px[i]) for px in row]) + "\n"
    
    if mode == "HSV":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        title = ["Hue\n", "Saturation\n", "VALUE\n"]
        for i in range(3):
            imgString += title[i]
            for row in img:
                imgString += sep.join([str(px[i]) for px in row]) + "\n"

    elif mode in ["GRAY", "GREY"]:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for row in img:
            imgString += sep.join([str(px) for px in row]) + "\n"
    
    imgString = imgString[:-1]
    return imgString

def reverse():
    pass

def main():
    """main function, parses command line arguments and executes img to csv conversion.
    """    
    args = parseArgs()
    # if args["reverse"]:
    #     pass
    # else:
    imgString = convert(cv2.imread(args["src"]), args["mode"], args["sep"])
    if args["dst"] is None:
        print(imgString)
    else:
        with open(args["dst"], "w") as dstFile:
            dstFile.write(imgString)

if __name__ == "__main__":
    main()