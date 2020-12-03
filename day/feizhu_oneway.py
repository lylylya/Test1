from selenium import webdriver
from lxml import etree
import json
import time


def save_info(content, titles):
    with open('/Users/mjt/spider/fz_jsons/'+titles + ".json", 'a+', encoding='utf-8') as f:
        f.write(json.dumps(obj=content, ensure_ascii=False, indent=4))
        print(titles+"写入完成")


def select(driver, url):
    driver.get(url)
    driver.find_element_by_xpath('//i[@class="iconfont icon-qrcode"]').click()
    time.sleep(30)
    search = driver.find_element_by_xpath('//div[@class="sub-content"]/div/form/fieldset/div[last()]')
    search.click()
    current_window = driver.current_window_handle  # 获取当前窗口handle name
    all_window = driver.window_handles  # 返回当前会话中所有窗口的句柄。
    for window in all_window:  # 通过遍历判断要切换的窗口
        if window != current_window:
            driver.switch_to.window(window)  # 将定位焦点切换到指定的窗口，包含所有可切换焦点的选项
    return driver


def parse_html(result):
    html_etree = etree.HTML(text=result)
    list_info = html_etree.xpath(
        '//div[@class="flight-list-box"]/div[@class="flight-list-item clearfix J_FlightItem"]')
    data_list = list()
    for div in list_info:
        flight_item = dict()
        # 航班号
        airline = div.xpath('.//table/tbody/tr/td/div/p/span/text()')
        flight_item["airline"] = airline[0] if airline else ""
        # 起降时间
        dep_time = div.xpath('.//table/tbody/tr/td[2]/p[@class="flight-time-deptime"]/text()')
        flight_item["dep_time"] = dep_time[0] if dep_time else ""
        arr_time = div.xpath('.//table/tbody/tr/td[2]/p[2]/span/text()')
        flight_item["arr_time"] = arr_time[0] if arr_time else ""
        # 起抵机场名称
        port_dep = div.xpath('.//table/tbody/tr/td[3]/div/p[@class="port-dep"]/text()')
        flight_item["port-dep"] = port_dep[0] if port_dep else ""
        port_arr = div.xpath('.//table/tbody/tr/td[3]/div/p[@class="port-arr"]/text()')
        flight_item["dep_name"] = port_arr[0] if port_arr else ""
        # 价格
        price = div.xpath('.//table/tbody/tr/td[6]/span/span/text()')
        flight_item["price"] = price[0] if price else ""
        data_list.append(flight_item)
    return data_list


class QuNaErSpider:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def run(self):
        root_url = 'https://login.taobao.com/member/login.jhtml?spm=181.11358650.0.0.5193223e4HzpeU&f=top&redirectURL=https%3A%2F%2Fwww.fliggy.com%2F%3Fttid%3Dseo.000000574%26seoType%3Dorigin&ttid=seo.000000574'
        driver = select(driver=self.driver, url=root_url)
        print(driver.current_url)
        time.sleep(6)
        for i in range(1, 30):
            current_page_info_list = parse_html(driver.page_source)
            line = etree.HTML(driver.page_source)
            title = line.xpath('//div[@class="J_TripRoute"]/div/h3/span/text()')
            print(title)
            titles = title[0] + '-' + title[1] + title[2]
            save_info(current_page_info_list, titles)
            time.sleep(15)


if __name__ == "__main__":
    obj = QuNaErSpider()
    obj.run()
