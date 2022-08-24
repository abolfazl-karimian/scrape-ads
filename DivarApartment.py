from ScrapeAdvertisement import ScrapeAds
from bs4 import BeautifulSoup
import re


class DivarApartmentAds(ScrapeAds):

    def extract_ads_url(self, text):
        ads_link = []
        web_text = BeautifulSoup(text, self.get_parser())
        # print(web_text)
        ads = web_text.find_all("div", attrs={'class': 'waf972 wbee95 we9d46'})
        for ad in ads:
            link = "https://divar.ir" + ad.find("a", href=True)['href']
            # print(link)
            ads_link.append(link)

        backup_and_dirty_way_ads = web_text.find_all("a", attrs={'class': ''})
        for ad in backup_and_dirty_way_ads:
            if 'href="/v/' in str(ad):
                link = "https://divar.ir" + ad['href']
                if link not in ads_link:
                    print(link)
                    ads_link.append(link)

        return ads_link

    def get_full_ads(self, links):
        for link in links:
            self.add_to_list(self.extract_divar_ad_info(link))
        # print(len(self._ADS))

    def extract_divar_ad_info(self, link):
        item = {}
        print(link)
        web_text = self.make_request(link).text
        ad = BeautifulSoup(web_text, self.get_parser())

        # index 0 =>
        self.extract_title(ad, item)
        # print(item)

        # index 1 =>
        self.extract_location(ad, item)

        # index 2 => Size
        # index 3 => Year
        # index 4 => Rooms
        self.extract_specs(ad, item)

        # index 5 => Credit
        # index 6 => Rent
        self.extract_price(ad, item)

        # index 7 => Floor
        self.extract_floor(ad, item)

        # index 8 => Elevator
        # index 9 => Parking
        self.extract_utility(ad, item)

        # index 10 => Desc
        self.extract_description(ad, item)

        # index 11 => Link
        item['link'] = link

        return item

    def add_to_list(self, item):
        if "پردیس" in item['title']: return

        if item['floor'] <= 2:
            self.ADS.append(item)
        elif item['floor'] > 2 and item['elevator'] is True:
            self.ADS.append(item)

        # if self._ADS[-1]['location']=='پیروزی': print(self._ADS[-1])

    def extract_title(self, ad, item):
        title = ad.find("div", attrs={'class': 'kt-page-title__title kt-page-title__title--responsive-sized'})
        item['title'] = title.text

    def extract_utility(self, ad, item):
        elevator = ad.find_all("span", attrs={'class': 'kt-group-row-item__value kt-body kt-body--stable'})[0].text
        if elevator == "آسانسور":
            item['elevator'] = True
        else:
            item['elevator'] = False
        parking = ad.find_all("span", attrs={'class': 'kt-group-row-item__value kt-body kt-body--stable'})[1].text
        if parking == "پارکینگ":
            item['parking'] = True
        else:
            item['elevator'] = False

    def extract_floor(self, ad, item):
        try:
            floor = \
                ad.find_all("div", attrs={'class': 'kt-base-row__end kt-unexpandable-row__value-box'})[-1].text.split(
                    " ")[
                    0]
            item['floor'] = int(floor)
        except ValueError:
            item['floor'] = 0

    def extract_price(self, ad, item):
        count = len(
            ad.find_all("div", attrs={'class': 'kt-base-row kt-base-row--large kt-base-row--has-icon kt-feature-row'}))
        if count < 1:
            credit = \
                ad.find_all("div", attrs={'class': 'kt-base-row__end kt-unexpandable-row__value-box'})[0].text.split(
                    " ")[
                    0].replace("٬", "")
            item['credit'] = int(credit)

            rent = \
                ad.find_all("div", attrs={'class': 'kt-base-row__end kt-unexpandable-row__value-box'})[1].text.split(
                    " ")[
                    0].replace("٬", "")
            item['rent'] = int(rent)

    def extract_specs(self, ad, item):
        specs = ad.find_all("div", attrs={'class': 'kt-group-row-item kt-group-row-item--info-row'})
        item['size'] = int(specs[0].find("span", attrs={'class': 'kt-group-row-item__value'}).text)
        item['year'] = int(specs[1].find("span", attrs={'class': 'kt-group-row-item__value'}).text)
        item['rooms'] = int(specs[2].find("span", attrs={'class': 'kt-group-row-item__value'}).text)
        if len(specs) > 3:
            item['credit'] = int(float(
                specs[3].find("span", attrs={'class': 'kt-group-row-item__value'}).text.replace(" ", "").replace(
                    "میلیون", ""))*1000000)

            item['rent'] = int(float(
                specs[4].find("span", attrs={'class': 'kt-group-row-item__value'}).text.replace(" ", "").replace(
                    "میلیون", "")) * 1000000)

    def extract_location(self, ad, item):
        location = ad.find("div", attrs={'class': 'kt-page-title__subtitle kt-page-title__subtitle--responsive-sized'})
        location = re.findall("(?<=\،)(.*?)(?=\|)", location.text)[0].strip()
        item['location'] = location

    def extract_description(self, ad, item):
        Desc = ad.find("p", attrs={'class': 'kt-description-row__text kt-description-row__text--primary'})
        item['description'] = Desc.text
