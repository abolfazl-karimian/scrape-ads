from DivarApartment import DivarApartmentAds
from HistoryHandler import HandleHistory
from Telegram import TelegramApi
from _datetime import datetime
from datetime import timedelta
from BColor import BColors


def get_url(min_credit=0, max_credit=500000000, min_rent=0, max_rent=500000000, min_size=0, max_size=200, min_age=0,
            max_age=40, parking='', rooms=1):
    URL = f"""https://divar.ir/s/tehran/rent-apartment/azerbaijan?
    districts=1001%2C1024%2C1025%2C1028%2C1035%2C106%2C115%2C116%2C117%2C118%2C119%2C120%2C125%2C126%2C127%2C128%2C130%2C131%2C132%2C133%2C138%2C139%2C143%2C145%2C146%2C147%2C148%2C152%2C155%2C157%2C158%2C172%2C173%2C174%2C197%2C200%2C201%2C202%2C203%2C204%2C205%2C206%2C208%2C209%2C210%2C211%2C283%2C284%2C286%2C292%2C297%2C298%2C299%2C300%2C301%2C302%2C315%2C360%2C399%2C64%2C656%2C658%2C67%2C68%2C70%2C71%2C72%2C74%2C78%2C81%2C82%2C84%2C86%2C87%2C88%2C90%2C91%2C920%2C926%2C927%2C928%2C929%2C932%2C933%2C934%2C935%2C936%2C937%2C938%2C939%2C94%2C940%2C941%2C943%2C944%2C945%2C949%2C95%2C950%2C954%2C955%2C956%2C957%2C958%2C959%2C96%2C960%2C971%2C99&
    credit={min_credit}-{max_credit}&
    rent={min_rent}-{max_rent}&
    size={min_size}-{max_size}&
    rooms={rooms}&
    building-age={min_age}-{max_age}&
    parking={parking}"""
    print(URL.replace("\n", "").replace(" ", ""))
    return URL.replace("\n", "").replace(" ", "")


if __name__ == '__main__':
    # U = """https://divar.ir/s/tehran/rent-apartment/azerbaijan?districts=1001%2C1024%2C1025%2C1028%2C1035%2C106%2C115%2C116%2C117%2C118%2C119%2C120%2C125%2C126%2C127%2C128%2C130%2C131%2C132%2C133%2C138%2C139%2C143%2C145%2C146%2C147%2C148%2C152%2C155%2C157%2C158%2C172%2C173%2C174%2C197%2C200%2C201%2C202%2C203%2C204%2C205%2C206%2C208%2C209%2C210%2C211%2C283%2C284%2C286%2C292%2C297%2C298%2C299%2C300%2C301%2C302%2C315%2C360%2C399%2C64%2C656%2C658%2C67%2C68%2C70%2C71%2C72%2C74%2C78%2C81%2C82%2C84%2C86%2C87%2C88%2C90%2C91%2C920%2C926%2C927%2C928%2C929%2C932%2C933%2C934%2C935%2C936%2C937%2C938%2C939%2C94%2C940%2C941%2C943%2C944%2C945%2C949%2C95%2C950%2C954%2C955%2C956%2C957%2C958%2C959%2C96%2C960%2C971%2C99&credit=0-150000000&rent=0-5800000&size=55-200&building-age=0-20&parking=true"""
    # print(get_url(max_credit=150000000, max_rent=5800000, min_size=55, max_age=20, parking='true'))
    divar = DivarApartmentAds(
        get_url(max_credit=150000000, min_rent=1200000, max_rent=5800000, min_size=55, max_age=20, parking='true',
                rooms=2))
    advertisements = divar.get_ads()

    divar_1_bedroom_but_good_enough = DivarApartmentAds(
        get_url(max_credit=150000000, min_rent=1200000, max_rent=5800000, min_size=55, max_age=20, parking='true',
                rooms=1))

    advertisements.append(divar_1_bedroom_but_good_enough.get_ads())

    print(f"{len(advertisements)}" + " Ad(s) found from divar with your preferred parameters.")

    history = HandleHistory()
    new_items = history.save_new_items(advertisements)
    print(f"{len(new_items)}" + " Ad(s) was/were new & was/were saved.")

    api = TelegramApi()
    sent_items = api.send_messages(new_items)
    print(f"{sent_items}" + " New ad(s) has/have been sent to Telegram.\n")

    if len(new_items) > sent_items:
        print(f"{BColors.FAIL}ERROR : Could not send some new items to telegram{BColors.ENDC}")

    now = datetime.now() + timedelta(minutes=270)
    now = now.strftime("%Y/%m/%d %H:%M:%S")
    print(f"{BColors.OKGREEN}********************   Finished At {now}   ********************.{BColors.ENDC}\n\n\n\n")

    exit()
