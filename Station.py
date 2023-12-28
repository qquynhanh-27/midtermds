import math


class Station:
    '''
    Lớp mô tả trạm đo lượng mưa gồm các thông tin:
    name: tên trạm
    sid: mã trạm
    lat: vĩ độ
    lon: kinh độ
    rain: từ điển về lượng mưa có khóa là ngày là một chuỗi dạng (năm-tháng-ngày),
    VD: 1980-6-22 và giá trị lượng mưa được đo trong ngày đó
    '''

    # Hàm dựng
    def __init__(self, name, sid, lat, lon):
        self.name = name
        self.sid = sid
        self.lat = lat
        self.lon = lon
        self.rain = dict()

    # Hàm tính gán giá trị cho thuộc tính rain
    def set_rain_infor(self, rain_dict):
        self.rain = rain_dict

    # Hàm tạo chuỗi đại diện cho đối tượng
    def __str__(self):
        return '{name:%s, id:%s, lat:%.3f, lon:%.3f}'%(self.name, self.sid, self.lat, self.lon)

    # Hàm tính khoảng cách Euclid từ trạm hiện tại đến trạm station
    def get_distance(self, station):
        return math.sqrt((self.lat - station.lat) ** 2 + (self.lon - station.lon) ** 2)

    # Hàm lấy ra giá trị mưa theo ngày
    def get_rain_value(self, date):
        '''
        Cần hoàn thiện hàm.
        Nếu date có trong từ điển mưa thì trả lại giá trị là lượng mưa của ngày đó
        Ngược lại trả giá trị 0
        '''
        return self.rain.get(date, 0)

