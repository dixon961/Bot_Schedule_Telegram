# -*- coding: utf-8 -*-
import requests
import lxml.html as html
import lxml
import datetime


def menu(site):
    ret = 'Время прибытия автобуса на остановку:\n'
    username = 'trnguest'
    password = 'trnguest'
    url = site
    r = requests.get(url, auth=(username, password))
    page = lxml.html.etree.HTML(r.text)
    if len(page.getchildren()[1].getchildren()[2].getchildren()) != 0:
        table_row = page.getchildren()[1].getchildren()[2].getchildren()[0].findall('tr')
    else:
        return 'Ошибка, автобусов на данной станции не придвидиться'
    for tr in table_row:
        columns = tr.findall('td')
        if len(columns) > 0:
            ret += 'Автобус '
            if str(html.tostring(columns[0])).find('&#') > 0:
                temp_bus = str(html.tostring(columns[0]))[
                           str(html.tostring(columns[0])).find('&#'):str(html.tostring(columns[0])).find('&#') + 7]
                if temp_bus == '&#1053;':
                    temp_bus = 'Н' + str(html.tostring(columns[0]))[str(html.tostring(columns[0])).find('</a>') - 1:str(
                        html.tostring(columns[0])).find('</a>')]
                elif temp_bus == '&#1069;':
                    temp_bus = str(html.tostring(columns[0]))[
                               str(html.tostring(columns[0])).find('&#') - 3:str(html.tostring(columns[0])).find('&#')] + 'Э'

                ret += temp_bus
            else:
                i = str(html.tostring(columns[0])).find('</a>') - 1
                temp_bus = ''
                while str(html.tostring(columns[0]))[i] != '>':
                    temp_bus += str(html.tostring(columns[0]))[i]
                    i -= 1
                ret += temp_bus[::-1]
            ret += ' : '
            time_pos = str(html.tostring(columns[2])).find(str(datetime.datetime.now().hour) + ':')
            if time_pos == -1:
                time_pos = str(html.tostring(columns[2])).find(str(datetime.datetime.now().hour + 1) + ':')
            if time_pos == -1:
                time_pos = str(html.tostring(columns[2])).find(str(datetime.datetime.now().hour + 2) + ':')
            ret += str(html.tostring(columns[2]))[time_pos:time_pos + 5]
            if ret[-1] == '<':
                ret = ret[0:len(ret) - 1]
        ret += '\n'
    return ret
