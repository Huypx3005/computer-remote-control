# fa-5_11

fa-5_11 created by GitHub Classroom

## Điều khiển máy tính từ xa với Telegram Bot

- Server: lắng nghe, kết nối với client

- Client: nhận lệnh và thực hiện lệnh

- Telegram bot: gửi lệnh tới client thông qua server
- 
      * /start
      * /help
      * /list: show all clients have been connected
      * /select_{id}: select connection
      * ( --- cần chọn 1 kết nối trước khi gửi lệnh điều khiển ---)
      * /dir: show directory
      * /shutdown_{time}: shutdown in {time} s
      * /restart{time}: restart in {time} s
      * /close: close connection

##

Gõ lệnh: "python server.py" để chạy server
Gõ lệnh: "python client.py" để chạy client

## Notes:

Gõ lệnh "ipconfig" để tìm địa chỉ IP tương ứng của máy, thay địa chỉ đó vào biến "host" trong file client.py
