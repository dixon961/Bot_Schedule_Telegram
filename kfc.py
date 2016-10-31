import lxml.html as html
import urllib.request as url


kfc_coupons_site = 'https://www.kfc.ru/promo/74'


def menu():
    kfc = url.urlopen(kfc_coupons_site)
    page = html.parse(kfc)

    e = page.getroot().find_class('coupon-list').pop()
    table = e.getchildren()
    imglist = []
    for li in table:
        imglist.append(li.getchildren()[0].get("src"))
    return imglist
