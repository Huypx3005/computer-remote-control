import sys
import time
import threading
import socket

from queue import Queue

from telegram_bot import *

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()


# ==========================================================================================================================
# Tạo socket và chấp nhận kết nối


# Tạo socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 3005
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding socket với port và host tương ứng, sau đó cho socket lắng nghe yêu cầu từ client
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Tiếp nhận kết nối từ nhiều clients và lưu vào list all_connections, all_address
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")

# ==========================================================================================================================
# Tạo 2 luồng:
    # 1 luồng tạo socket, lắng nghe và chấp nhận kết nối
    # 1 luồng thực thi telegrambot


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            run_telegrambot()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


if __name__ == "__main__":
    create_workers()
    create_jobs()
