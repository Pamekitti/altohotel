from bs4 import BeautifulSoup
import requests
import pandas as pd


def inspect(val):
    print(val)
    print(type(val))


new_requests = False
html_directory = 'html/hotel_test.html'
if new_requests:
    html = requests.get('https://www.booking.com/hotel/th/rikka-inn.en-gb.html?aid=898409;label=affnetawin-index_pub-214459_site-_pname-Honey%20Science%20Corporation_plc-ext_ts-g7956987871295198328-a8716124745074117859_clkid-6776_1662468861_71ce27f335bf47cb9ba9e6a9608cf572;sid=cd42be046d7fb2183d44382c763a4716;all_sr_blocks=17655204_350772997_2_0_0;checkin=2022-09-06;checkout=2022-09-07;dcs_click=1;dest_id=-3414440;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=17655204_350772997_2_0_0;hpos=1;matching_block_id=17655204_350772997_2_0_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=17655204_350772997_2_0_0__108900;srepoch=1662468867;srpvid=e9af5ac09c830480;type=total;ucfs=1&#hotelTmpl')
    with open(html_directory, 'wb+') as f:
        f.write(html.content)
    soup = BeautifulSoup(html.content, 'lxml')
else:
    with open(html_directory, 'rb') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

title = soup.find('h2', class_='pp-header__title').text.strip()
inspect(title)

