import csv
import datetime
from itertools import tee

import requests
import email

from place import parse_place


def format_dict(d):
    return ' '.join([f'{k}:{v}' for k,v in d.items()])


headers = '''Host: www.airbnb.ru
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://www.airbnb.ru/s/%D0%AD%D1%81%D1%82%D0%BE~%D0%A1%D0%B0%D0%B4%D0%BE%D0%BA--%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D1%80%D0%B0%D0%B9/homes?adults=1&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&gps_lat=43.6701285&gps_lng=40.2610513&tab_id=home_tab&place_id=ChIJG7tVEL119kARoolZ6QfnDrI&federated_search_session_id=7565e76e-1e9f-420a-b3cd-45deba985924&map_toggle=false&items_offset=20&section_offset=3
content-type: application/json
X-Airbnb-GraphQL-Platform: web
X-Airbnb-GraphQL-Platform-Client: apollo-niobe
X-CSRF-Token: V4$.airbnb.ru$vNJwZHT6B5E$9-b0Gf0vD0ZX7uxtO3OqSIgt72xiPGdr4AOVYw93ceY=
X-Airbnb-API-Key: d306zoyjsyarp7ifhu67rjxn52tv0t20
X-CSRF-Without-Token: 1
Connection: keep-alive
Cookie: bev=1601283992_NjhkZjdjZWE1ZmI2; cdn_exp_f699727e78669251b=control; tzo=180; frmfctr=wide; OptanonConsent=landingPath=https%3A%2F%2Fwww.airbnb.ru%2Frooms%2F45087683%3Fsource_impression_id%3Dp3_1600693700_YdyIut7wxZFNuvRd%26guests%3D4%26adults%3D4%26check_in%3D2020-10-02%26check_out%3D2020-10-10&datestamp=Mon+Sep+28+2020+12%3A06%3A42+GMT%2B0300+(Moscow+Standard+Time)&version=4.6.0&groups=0_179751%3A1%2C1%3A1%2C2%3A1%2C0_183217%3A1%2C3%3A1%2C0_183345%3A1%2C0_183219%3A1%2C4%3A1%2C0_183240%3A1%2C0_179739%3A1%2C0_179743%3A1%2C0_185813%3A1%2C0_183096%3A1%2C0_179755%3A1%2C0_183215%3A1%2C0_185808%3A1%2C0_179747%3A1%2C0_179740%3A1%2C0_179744%3A1%2C0_185810%3A1%2C0_185814%3A1%2C0_183097%3A1%2C0_179756%3A1%2C0_183216%3A1%2C0_183344%3A1%2C0_185809%3A1%2C0_179748%3A1%2C0_179752%3A1%2C0_183241%3A1%2C0_179741%3A1%2C0_183098%3A1%2C0_179745%3A1%2C0_183346%3A1%2C0_185811%3A1%2C0_179737%3A1%2C0_185815%3A1%2C0_179757%3A1%2C0_179749%3A1%2C0_179753%3A1%2C0_185831%3A1%2C0_183099%3A1%2C0_179738%3A1%2C0_179742%3A1%2C0_183095%3A1%2C0_185816%3A1%2C0_183243%3A1%2C0_179754%3A1%2C0_183214%3A1%2C0_179750%3A1; cfrmfctr=DESKTOP; cbkp=4; OptanonAlertBoxClosed=2020-09-28T09:06:42.978Z; _airbed_session_id=b693486d7af95a36b7b909e1849bbf17; cdn_exp_e437bcda7f41486a6=extend_one_three_five_days; cdn_exp_14332663b5ca816ee=control; cdn_exp_b1b38777d5c7a308a=runtime_initializers; cdn_exp_b76569944fd3a6caf=extend_one_three_seven_days; sdid=; _user_attributes=%7B%22curr%22%3A%22RUB%22%2C%22guest_exchange%22%3A76.75032%2C%22device_profiling_session_id%22%3A%221602659137--04f5ace973032ed897a9569f%22%2C%22giftcard_profiling_session_id%22%3A%221603909572-7725978-fa92dd84b39a386e37c7d510%22%2C%22reservation_profiling_session_id%22%3A%221603909572-7725978-257ae2d8c9f65b740419144d%22%2C%22id%22%3A7725978%2C%22hash_user_id%22%3A%2206396acefb7d3e63e11a4b0c3c799a5413bb8704%22%2C%22eid%22%3A%22DXh6undPcFJDtDDli1Ee4g%3D%3D%22%2C%22num_msg%22%3A1%2C%22num_notif%22%3A0%2C%22num_alert%22%3A0%2C%22num_h%22%3A0%2C%22num_trip_notif%22%3A0%2C%22name%22%3A%22Alexey%22%2C%22num_action%22%3A0%2C%22is_admin%22%3Afalse%2C%22can_access_photography%22%3Afalse%2C%22travel_credit_status%22%3Anull%2C%22referrals_info%22%3A%7B%22receiver_max_savings%22%3Anull%2C%22receiver_savings_percent%22%3Anull%2C%22receiver_signup%22%3Anull%2C%22referrer_guest%22%3A%221%C2%A0100%E2%82%BD%22%2C%22terms_and_conditions_link%22%3A%22%2Fhelp%2Farticle%2F2269%22%2C%22wechat_link%22%3Anull%2C%22offer_discount_type%22%3Anull%7D%7D; _ga=GA1.2.1368901649.1603313680; __ssid=b7712b5193628cb3845c826f88cebb5; _gcl_au=1.1.295923240.1603313700; _uetvid=b255480013df11ebaeab41b2a31101cb; jitney_client_session_id=8dfae4eb-40d8-4881-a391-90e419a5856e; jitney_client_session_created_at=1603905918; jitney_client_session_updated_at=1603913053; _rmt=2--Wzc3MjU5NzgsIjE2fDF8TUxkaXNyTGtERnYxNkN2ciIsIldSemhJcVhZSGN6bGV5Z2NmNWVYd0ZkRjdRbTEtTDRzUVhHMVBXb19vVG8iXQ%3D%3D--c7f9dbe9e1a82377fe764e418d214a26238ba356; _pt=1--WyIwNjM5NmFjZWZiN2QzZTYzZTExYTRiMGMzYzc5OWE1NDEzYmI4NzA0Il0%3D--abaa35e01f086bce54c0f8f654e93a13cdc04f03; _aat=0%7CWGP58ReQru8AqRfNAmyE4H36RNlbetY1hI33SKQyVAupZ0WFwgRPP5LTIKrFqxG%2F; abb_fa2=%7B%22user_id%22%3A%2244%7C1%7CkGlzOmsf2zph4A%2FqeMCp%2BIoKNr6HRo%2FcYeBfglori3BK0nQF1BN%2F%22%7D; rclu=%7B%227725978%22%3D%3E%22bxr3fMfZoLiiZRNFplRGO7DGqyCY4sHQYkW4dD312EM%3D%22%7D; rclmd=%7B%227725978%22%3D%3E%22email%22%7D; cdn_exp_24332663b5ca816ee=control; har=1; previousTab=%7B%22id%22%3A%226186477d-e9d7-4481-8799-9185a9bed306%22%2C%22url%22%3A%22https%3A%2F%2Fwww.airbnb.ru%2Finbox%2F876793147%3Fref%3Dredirect-from-messaging-app%26ttype%3Dhome_booking%22%7D; flags=8448; _csrf_token=V4%24.airbnb.ru%24vNJwZHT6B5E%249-b0Gf0vD0ZX7uxtO3OqSIgt72xiPGdr4AOVYw93ceY%3D; auth_jitney_session_id=9111187b-1f52-4cf4-ae36-88a493174f0a; li=1; roles=0; hli=1; __svt=258; cdn_exp_140d70271b981c913=treatment; cdn_exp_283a19eb11edcad71=control
Pragma: no-cache
Cache-Control: no-cache
TE: Trailers'''

def get_places(place_id: str):
    variables = '''{"request":{"metadataOnly":false,"version":"1.7.9","itemsPerGrid":55,"adults":1,"refinementPaths":["/homes"],"source":"structured_search_input_header",
"searchType":"pagination","tabId":"home_tab","placeId":"%(placeId)s",
"federatedSearchSessionId":"7565e76e-1e9f-420a-b3cd-45deba985924","mapToggle":false,"itemsOffset":20,"sectionOffset":3,
"query":"Эсто-Садок, Краснодарский край","cdnCacheSafe":false,"simpleSearchTreatment":"simple_search_only",
"treatmentFlags":["simple_search_1_1","simple_search_desktop_v3_full_bleed","flexible_dates_options_extend_one_three_five_days"],"screenSize":"large"}}''' % dict(placeId=place_id)

    extensions = '{"persistedQuery":{"version":1,"sha256Hash":"aa7c5e53ca607108c7e8cf6052853bfd8ecec3edf21c6578ee2256e8ed108432"}}'
    uri = f'https://www.airbnb.ru/api/v3/ExploreSearch?operationName=ExploreSearch&locale=ru&currency=RUB&_cb=164980x1wh7384&variables={variables}&extensions={extensions}'
    r = requests.get(uri, headers=email.message_from_string(headers))
    r.raise_for_status()
    with open(f'search.json', 'w') as fp:
        fp.write(r.text)

    items = r.json()['data']['dora']['exploreV3']['sections'][0]['items']
    print(f'found {len(items)} places')
    for item in items[:3]:
        id = item['listing']['id']
        url = f'https://www.airbnb.ru/rooms/{id}'
        print(url, item['listing']['name'])
        yield id

        items = parse_place(id=id)
        prices = ' '.join([f'{item["localPriceFormatted"]}' for item in items])
        print(prices)


def get_prices(places):
    for place in places:
        yield parse_place(place)


def dates(days):
    base = datetime.date.today()
    dates = [base + datetime.timedelta(days=x) for x in range(days)]
    return list(map(str, dates))


def dump(places, prices):
    with open('data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['url'] + dates(30), extrasaction='ignore')
        writer.writeheader()
        for id, pr in zip(places, prices):
            data = dict(url=f'https://www.airbnb.ru/rooms/{id}')
            data.update({item["calendarDate"]: item["localPriceFormatted"] for item in pr})
            writer.writerow(data)


if __name__ == '__main__':
    # placeId = 'ChIJ7WVKx4w3lkYR_46Eqz9nx20'  # спб
    # placeId = 'ChIJXSFYKsZbs0YRSO_CVGuYeyA'  # пересалвль залесский
    places = get_places(place_id='ChIJ7WVKx4w3lkYR_46Eqz9nx20')
    places1, places2 = tee(places)
    prices = get_prices(places=places1)
    dump(places2, prices)