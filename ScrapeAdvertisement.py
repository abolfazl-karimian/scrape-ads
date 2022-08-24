import requests


class ScrapeAds:
    __default_page = 'https://googles.org'
    __parser = 'html.parser'
    ADS = []

    def __init__(self, URL=__default_page):
        result = self.make_request(URL)
        # print(self._result.status_code)
        links = self.extract_ads_url(text=result.text)
        # print(links)

        self.get_full_ads(links)

    def set_parser(self, x):
        self.__parser = x

    def get_parser(self):
        return self.__parser

    def get_ads(self):
        return self.ADS

    def make_request(self, URL):
        try:
            result = requests.get(URL)
            if result.status_code != 200:
                message = f"There Is A Problem.\nError Code:{result.status_code}"
                self.throw_error(message)
            return result

        except requests.exceptions.ConnectionError:
            message = "Could Not Reach To server."
            self.throw_error(message)

    def throw_error(self, message):
        print(message)
        exit()

    def extract_ads_url(self, text):
        pass

    def get_full_ads(self, links):
        pass

    def add_to_list(self, item):
        pass

    def notify(self):
        pass
