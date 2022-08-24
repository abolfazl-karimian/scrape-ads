import requests
from _datetime import datetime
from datetime import timedelta
from BColor import BColors


class TelegramApi:
    __message = 'None'
    __chatId = '@find_my_new_home'
    __token = '5482919534:AAF0YUzdqKtw10mpJNYmklKFM650OfHLHIw'
    __api = 'https://api.telegram.org/bot'
    sent = 0

    def send_messages(self, items):
        for item in items:
            self.send_message_to_channel(self.format_msg(item))
        return self.sent

    def send_message_to_channel(self, msg):
        prepared_request = self.__api + self.__token + "/sendMessage?chat_id=" + self.__chatId + "&parse_mode=html" + "&text=" + msg
        # print(prepared_request)
        try:
            result = requests.post(prepared_request)
            # print("Sending to telegram response = ", result)
            if result.status_code == 200:
                self.sent += 1
            return 1
        except requests.exceptions.ConnectionError:
            message = f"{BColors.WARNING}Could Not Reach To Telegram Server.{BColors.ENDC}"
            self.throw_error(message)

    def throw_error(self, message):
        print(message)

    def format_msg(self, item):
        now = datetime.now() + timedelta(minutes=270)
        now = now.strftime("%H:%M:%S")
        time = f"""🔆🔆🔆            <pre>{now}</pre>         🔆🔆🔆\n\n"""

        title = f"""🏠<a href="{item['link']}">{item['title']}</a>\n\n"""
        size = f"♦️<strong>متراژ: </strong><u><em>{item['size']}</em></u>\n"
        floor = f"♦️<strong>طبقه: </strong><u><em>{item['floor']}</em></u>\n"
        rooms = f"♦️<strong>تعداد اتاق: </strong><u><em>{item['rooms']}</em></u>\n\n"
        rent = f"""🔷اجاره: <pre>{("{:,}".format(item['rent']))}</pre>\n"""
        credits = f"""🔷ودیعه: <pre>{("{:,}".format(item['credit']))}</pre>\n\n"""
        year = f"""⚪️<strong>سال ساخت: </strong><u>{item['year']}</u>\n"""
        location = f"""⚪️<strong>منطقه: {item['location']}</strong>\n\n"""
        if item['parking']:
            parking = f"""◼️پارکینگ: ✅\n"""
        else:
            parking = f"""◼️پارکینگ: ❌\n"""

        if item['elevator']:
            elevator = f"""◼️آسانسور: ✅\n"""
        else:
            elevator = f"""◼️آسانسور: ❌\n"""

        text = time + title + size + floor + rooms + rent + credits + year + location + parking + elevator
        return text

    def set_message(self, msg):
        self.__message = msg

    def get_message(self):
        return self.__message

    def set_chat_id(self, chatId):
        self.__chatId = chatId

    def get_chat_id(self):
        return self.__chatId

    def set_token(self, token):
        self.__token = token

    def get_token(self):
        return self.__token