import socket
import re


def data_check(data_set):
    data_set = data_set.decode()
    match = re.fullmatch(r'\d{4} .. \d{2}:\d{2}:\d{2}\.\d{3} \d{2}', data_set)
    if match:
        sportsman_n, cut_off, sport_group, ar_time = data_processing(data_set)
        message = f'спортсмен, нагрудный номер {sportsman_n} прошёл отсечку {cut_off} в "{ar_time[0]}"'.encode()
        return [message, sport_group]
    else:
        return 'Неверный формат данных'


def data_processing(data_set):
    data_list = re.findall(r'\w+', data_set)
    sportsman_n = data_list[0]
    cut_off = data_list[1]
    group = data_list[6]
    ar_time = re.findall(r'\d{2}:\d{2}:\d{2}\.\d', data_set)
    return sportsman_n, cut_off, group, ar_time


HOST = 'localhost'
PORT = 51234

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind((HOST, PORT))
serv_sock.listen(1)
conn, addr = serv_sock.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break

    if data.decode() == 'q':
        conn.send('Соединение прервано'.encode())
    else:
        result = data_check(data)
        if type(result) == list:
            if result[1] == '00':
                conn.send(result[0])
                with open('log.txt', 'a+') as file:
                    file.write(f"{result[0].decode()}\n")
            else:
                with open('log.txt', 'a+') as file:
                    file.write(f"{result[0].decode()}\n")
        else:
            conn.send(result.encode())


conn.close()
