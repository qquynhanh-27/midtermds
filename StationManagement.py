from Station import Station


def read_station_fromfile(station_file):
    '''
    Hàm thực hiện đọc dữ liệu từ file statipn_file, đây là 1 file định dạng .csv
    Mỗi dữ liệu được phân cách bởi dấu ,
    dòng đầu tiên là tên các thuộc tính của trạm, các dòng tiếp theo, mỗi dòng gồm 4 thông tin ứng với các thuộc tính của trạm

    Hướng dẫn:
        Đọc dòng đầu tiên để biết được thứ tự các thuộc tính (có thể bỏ qua)
        Với mỗi dòng tiếp theo, đọc dòng đó, phân tách theo dấu , lưu các giá trị vào các biến
        Tạo đối tượng Station với các thuộc tính đã đọc ở trên, rồi đưa đối tượng vào danh sách kết quả.
    '''
    station_list = []
    file = open(station_file, 'rt', encoding='utf-8')
    head = file.readline()
    for line in file:
        tokens = line.strip().split(',')
        name, idx, lon, lat = tokens[0], tokens[1], float(tokens[2]), float(tokens[3])
        s = Station(name, idx, lon, lat)
        station_list.append(s)
    file.close()


def read_rain_fromfile(rain_file, station_list):
    '''
    Đọc file rain.csv
    Dòng đầu tiên là nhãn time và tên của các trạm (146 trạm)
    Mỗi dòng tiếp theo gồm 147 giá trị, giá trị đầu tiên 1 chuỗi (str) chỉ thời gian định dạng năm-tháng-ngày
    và 146 giá trị tiếp theo là lượng mưa từng trạm

    Hướng dẫn:
        - Đọc dòng đầu tiên để biết được thứ tự của các trạm dựa vào tên trạm
        - Có thể lưu các tên trạm vào 1 danh sách, hoặc 1 cách biểu diễn nào đó để biết được thứ tự của trạm theo tên trạm
        - Tạo 1 danh sách, trong đó mỗi phần tử là 1 từ điển, thứ tự của phần tử nên trùng với thự tự tên trạm

    Với mỗi dòng tiếp theo, đọc dòng đó, phân tách các giá trị theo dấu ,
        - giá trị đầu tiên là chuỗi thời gian sẽ là khoá
        - 146 giá trị tiếp theo sẽ là các giá trị ứng với khoá trên
        - thêm lần lượt các cặp khoá-giá trị vào các từ điển trong danh sách theo thứ tự

    Sau khi đọc hết tệp, cập nhật thông tin của các trạm trong station_list bằng cách gọi đến hàm set_rain_infor của mỗi trạm, với các từ điển tương ứng tạo ở bước trước
    '''
    file = open(rain_file, 'rt', encoding='utf-8')
    head = file.readline()
    stations = head.strip().split(',')[1:]
    rain_dict_list = [dict() for s in stations]
    for line in file:
        tks = line.strip().split(',')
        date = tks[0]
        for i in range(len(rain_dict_list)):
            rain_dict_list[i][date] = float(tks[i + 1])

    for s in station_list:
        for i in range(len(stations)):
            if s.name == stations[i]:
                s.set_rain_infor(rain_dict_list[i])
                break
    file.close()


def count_dry_day(s):
    '''
    input s là 1 station
    Thực hện tìm v trả về số ngày không mưa của trạm s
    '''
    return sum([1 for r in s.rain.values() if r == 0])


def get_station_dry_frequent(station_list):
    '''
    input: station_list là 1 danh sách các station
    Hàm thực hiện tìm và trả về 1 danh sách k tên trạm trong station_list có số ngày không mưa nhiều nhất
    (có thể có 1 trạm hoặc nhiều hơn 1 trạm có cùng số ngày không mưa)
    Danh sách kết quả được sắp xếp tăng dần theo tên trạm
    '''
    max_frequent = max([count_dry_day(s) for s in station_list])
    result = []
    for s in station_list:
        if count_dry_day(s) == max_frequent:
            result.append(s.name)
    result.sort()
    return result


def find_station_rain_above_avg(station_list):
    '''
    input: station_list là một danh sách các station
    Hàm thực hiện tìm và trả về 1 danh sách k tên trạm trong station_list có tổng lượng mưa cao hơn
    tổng lượng mưa trung bình của tất cả các trạm trong station_list
    Danh sách kết quả được sắp xếp tăng dần theo tên trạm
    '''
    total = sum([sum(s.rain.values()) for s in station_list])
    avg = total / len(station_list)
    result = [s.name for s in station_list if sum(s.rain.values()) > avg]
    result.sort()
    return result


def find_top_k_rain(date, station_list, k=5):
    '''
    input: station_list là 1 danh sách các station

    Hàm thực hiện tìm và trả về 1 danh sách k bộ (tên trạm, lượng mưa) trong station_list của ngày date,
    kết quả chỉ tính đến k trạm có lượng mưa lớn nhất và lớn hơn 0 trong ngày date

    (Chú ý kết quả chỉ xét các trạm có lượng mưa > 0, nên đôi khi có thể danh sách kết quả không cần đủ k trạm)
    Danh sách kết quả được sắp xếp giảm dần theo lượng mưa
    '''
    tk = [(s.name, s.rain.get(date, 0)) for s in station_list]
    tk.sort(key=lambda x: (x[1], x[0]), reverse=True)
    tk = tk[:k]
    tk = [t for t in tk if t[1] > 0]
    return tk


def find_lowest_rain_station(station_list):
    '''
    input: station_list là 1 danh sách các station

    Hàm thực hiện tìm và trả về 1 danh sách các tên trạm có tổng lượng mưa nhỏ nhất (có thể có nhiều hơn 1 trạm)
    Danh sách kết quả được sắp xếp tăng dần theo tên trạm
    '''
    min_rain = min([sum(s.rain.values()) for s in station_list])
    result = []
    for s in station_list:
        if sum(s.rain.values()) == min_rain:
            result.append(s)
    result.sort()
    return result
