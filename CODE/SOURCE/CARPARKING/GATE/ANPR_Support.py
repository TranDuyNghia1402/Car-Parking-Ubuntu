from GATE.ANPR import ANPR
from GATE.QRGenerator import QRCode
import cv2 as cv
import argparse
import imutils
import csv
from datetime import datetime

data_path = '/home/tran-duy-nghia/Desktop/CarParking/DATASAVE/data.csv'
diary_path = '/home/tran-duy-nghia/Desktop/CarParking/DATASAVE/diary.csv'


def cleanup_text(text):
    # strip out non ASCII text so we can draw the text on the image
    # using openCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip().replace("\n", "").replace('-> ', '')
# func: strip out non ASCII text so we can draw the text on the image
# parameter: string
# return values: string with only alphabet and number


def get_license_plate_text(image_path):
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--clear-border", type=int, default=True,
                    help="whether or to clear border pixels before OCR'ing")
    ap.add_argument("-p", "--psm", type=int, default=7,
                    help="default PSM mode for OCR'ing license plates")
    ap.add_argument("-d", "--debug", type=int, default=-1,
                    help="whether or not to show additional visualizations")
    args = vars(ap.parse_args())
    # initialize our ANPR class
    anpr = ANPR(debug=args["debug"] > 0)
    # grab all image paths in the input directory
    # imagePaths = sorted(list(paths.list_images(args["input"])))
    # loop over all image paths in the input directory
    image = cv.imread(image_path)
    image = imutils.resize(image, width=500)
    # apply automatic license plate recognition
    (lpText, lpCnt) = anpr.find_and_ocr(image, psm=args["psm"],
                                        clearBorder=args["clear_border"] > 0)
    # only continue if the license plate was successfully OCR'd
    if lpText is not None and lpCnt is not None:
        # fit a rotated bounding box to the license plate contour and
        # draw the bounding box on the license plate
        box = cv.boxPoints(cv.minAreaRect(lpCnt))
        box = box.astype("int")
        cv.drawContours(image, [box], -1, (0, 255, 0), 2)
        # compute a normal (unrotated) bounding box for the license
        # plate and then draw the OCR'd license plate text on the
        # image
        (x, y, w, h) = cv.boundingRect(lpCnt)
        cv.putText(image, cleanup_text(lpText), (x, y-15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        # show the output ANPR image
        print("[INFO] {}".format(lpText))
        cv.imshow("Output ANPR", image)
        return '-> ' + lpText
    else:
        print('License Plate not found')
        return None
# func: get license plate string from frame, images
# parameter: image's path
# return values: license plate string


def get_current_time():
    current_time = datetime.now().strftime("%D %H:%M")
    return current_time
# func: get current time
# parameter: None
# return values: current time (string) (day//month//year hour:minute)


def generate_qrcode():
    qrGen = QRCode()
    path, data = qrGen.generate_qr()
    return (path, data)
# func: generate qr code img, get identifier code from qr img
# parameter: None
# return values: path of qr image, identifier code


def write_data_to_csv(License_plate, Identifier, TimeIn):
    # Write data to a CSV file
    field_name = ["LICENSE PLATE", "IDENTIFER", "TIME IN"]
    with open(data_path, 'a', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=field_name)
        data = {"LICENSE PLATE": License_plate,
                "IDENTIFER": Identifier,
                "TIME IN": TimeIn}
        dict_writer.writerow(data)
        f.close()
# func: write License Plate, Identifier, Time In of the cars is in the parking lot to csv file
# parameter: License Plate String, Identifier String, Current Time String
# return values: None


def read_data_from_csv():
    with open(data_path, 'r') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            print(row)
        f.close()
# func: read data from csv file
# parameter: csv path
# return values: data


def check_data_is_correct(license_plate, identifier):
    with open(data_path, 'r') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            license_text = cleanup_text(row[0])
            identifier_code = cleanup_text(row[1])
            if license_text == license_plate and identifier_code == identifier:
                print("license plate: ", license_text)
                print("identifier code: ", identifier_code)
                f.close()
                return True
    return False
# func: check if data gate in == data gate out
# parameter: license plate, identifier
# return values: True // False


def get_time_in(license_plate):
    with open(data_path, 'r') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            if cleanup_text(license_plate) == cleanup_text(row[0]):
                time_in = row[2]
                print("time in: ", time_in)
                f.close()
                return time_in
# func: get time in
# parameter: license plate
# return values: time in


def get_total_time(license_plate, time_out):
    time_in = get_time_in(license_plate)
    print(time_in)
# func: cal total time in - out
# paramter: license plate, time out
# return values: total time


def remove_data(license_plate):
    lines = list()
    print(license_plate)
    with open(data_path, 'r') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            lines.append(row)
            if license_plate == cleanup_text(row[0]):
                lines.remove(row)
    with open(data_path, 'w', newline='') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerows(lines)
        f.close()
# func: remove data from csv
# parameter: data path
# return values: None
