import qrcode
import random
import string
import os

dir_path = '/home/tran-duy-nghia/Desktop/CarParking/IMAGES/QRCODE'


class QRCode:
    def __init__(self, code_size=12) -> None:
        self.code_size = code_size
        self.__identifier = ''.join([random.choice(string.ascii_letters + string.digits)
                                     for i in range(self.code_size)])
        self.__qr = qrcode.QRCode(version=1, box_size=9, border=3)

    def get_identifier_code(self):
        return self.__identifier

    def generate_qr(self):
        data = self.get_identifier_code()
        self.__qr.add_data(data)
        self.__qr.make(fit=True)
        img = self.__qr.make_image(fill_color='black',
                                   back_color='white')
        qr_dir = os.path.join(dir_path, "QRCode.jpg")
        img.save(qr_dir)
        return qr_dir, data
