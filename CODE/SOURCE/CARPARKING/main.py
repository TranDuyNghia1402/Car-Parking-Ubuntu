import cv2 as cv
import os
from GATE.ANPR_Support import *
from GATE.Gate import Gate

path = '/home/tran-duy-nghia/Desktop/CarParking/IMAGES/TEST_IMG/'
img_name1 = 'test1.jpg'
img_name2 = 'test2.jpg'
img_name3 = 'test3.jpg'
img_name4 = 'test4.jpg'
img_name5 = 'test5.jpg'
img_name6 = 'test6.jpg'


def gateIn():
    # capture = cv.VideoCapture(0)
    # isTrue, frame = capture.read()
    # gateIn = Gate(camera_frame=frame)
    # while isTrue:
    #     gateIn.plate_regconition()
    #     isTrue, frame = capture.read()
    #     cv.imshow('frame', frame)
    #     if cv.waitKey(1) & 0xFF == ord('s'):
    #         print('s')
    #         gate_in.send_command(ser, OPEN_COMMAND)
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         print('quit')
    #         gate_in.send_command(ser, CLOSE_COMMAND)
    #         # break
    # capture.release()
    # cv.destroyAllWindows()
    image = cv.imread(os.path.join(path, img_name2))
    gate_in = Gate(image_input=image)
    is_number_plate_in, cap_in_img = gate_in.plate_regconition()
    if is_number_plate_in:
        license_text_in = get_license_plate_text(cap_in_img).replace('/n', '')
        current_time_in = get_current_time()
        if license_text_in is not None:
            qr_path, data = generate_qrcode()
            write_data_to_csv(license_text_in, data, current_time_in)
            print(qr_path)
            cv.imshow('IDENTIFIER', cv.imread(qr_path))
    read_data_from_csv()
    cv.waitKey(0)


def gateOut():
    image = cv.imread(os.path.join(path, img_name1))
    gate_out = Gate(image_input=image)
    is_number_plate_out, cap_out_img = gate_out.plate_regconition()
    if is_number_plate_out:
        license_text_out = cleanup_text(get_license_plate_text(cap_out_img))
        current_time_out = get_current_time()
        if license_text_out is not None:
            if check_data_is_correct(license_text_out, 'MtrNvOp49W7I'):
                time_in = get_time_in(license_text_out)
                print('remove data')
                remove_data(license_text_out)
            else:
                print('Data Wrong')
    cv.waitKey(0)


def read_data():
    read_data_from_csv()


if __name__ == "__main__":
    # gateIn()
    gateOut()
    # read_data()
