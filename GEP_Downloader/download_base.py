import geopandas as gpd
import re
import time
import os
import json
from datetime import datetime, timedelta

import pyautogui


class ToomanyNotFound(BaseException):
    def __init__(self):
        pyautogui.click(1422, 227)
        super().__init__('Too many 404 Not Found...')

class ToomanyImages(Exception):
    def __init__(self):
        pyautogui.click(1422, 227)
        super().__init__('Too many Images...')

class Base:
    def __init__(self, json_path) -> None:
        yyyy_mm_dd, self.yymmdd = self.now_date()
        self.aoi, \
        self.aoi_date, \
        self.right_lng, \
        self.left_lng, \
        self.top_lat, \
        self.bottom_lat = self.read_json(json_path)
        self.save_path = f'C:\\downloads\\{yyyy_mm_dd}_{self.aoi}'

    def now_date(self):
        current_time = datetime.now()
        yyyy_mm_dd = datetime.strftime(current_time, '%Y-%m-%d')
        yymmdd = datetime.strftime(current_time, '%y%m%d')
        return yyyy_mm_dd, yymmdd

    def make_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            print('directory already exists')

    def read_json(self, json_path):
        with open(json_path,'r') as f:
            data =json.load(f)
            aoi = data['aoi']
            aoi_date = data['date']
            max_lng = data['geog']['max_lng']
            min_lng = data['geog']['min_lng']
            max_lat = data['geog']['max_lat']
            min_lat = data['geog']['min_lat']
        return aoi, aoi_date, max_lng, min_lng, max_lat, min_lat

    def scene_name_time_define(self, date, save_path):
        self.scene_name = f'GEP_{date}_{self.yymmdd}'
        self.combine_path = f'{save_path}\\{self.scene_name}.geid'
        self.imagery_date = f'{date[:4]}-{date[4:6]}-{date[6:]}'
        dir_path = f'{save_path}\\{self.scene_name}'
        # assert os.path.exists(dir_path) == False
        return dir_path

    @staticmethod
    def kml_to_lat_lng(kml_path):
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        df = gpd.read_file(kml_path, driver='KML')
        aoi_poly = str(df['geometry'][0])
        aoi_poly = aoi_poly.replace('Z','')
        aoi_poly = re.sub(' 0', '', aoi_poly)
        aoi_poly = aoi_poly.replace('POLYGON', '')
        aoi_poly = aoi_poly.replace('((', '')
        aoi_poly = aoi_poly.replace('))', '')
        aoi_poly = aoi_poly.replace('LINESTRING ', '')
        aoi_poly = aoi_poly.replace(')', '')
        aoi_poly = aoi_poly.replace('(', '')
        aoi_poly = aoi_poly.strip()
        aoi_split = aoi_poly.split(', ')

        lng_list = []
        lat_list = []
        for aoi_item in aoi_split:
            aoi_split = aoi_item.split(' ')
            lng_list.append(aoi_split[0])
            lat_list.append(aoi_split[1])
        max_lng, min_lng = max(map(float, lng_list)), min(map(float, lng_list)) 
        max_lat, min_lat = max(map(float, lat_list)), min(map(float, lat_list)) 
        return str(max_lng), str(min_lng), str(max_lat), str(min_lat)
            
    @staticmethod
    def datetime_to_time(date_time):
        date_time = str(date_time)
        st = date_time.replace('-','')
        return st


class PyAutoGuiForGEP(Base):
    def __init__(self, json_path) -> None:
        super().__init__(json_path)
 
    def auto_input_gep(self) -> None:
        pyautogui.click(400, 1054)
        time.sleep(1)
        pyautogui.moveTo(740, 300)
        pyautogui.doubleClick()
        pyautogui.press('Backspace')
        pyautogui.write(self.scene_name)
        pyautogui.click(746, 346)
        pyautogui.click(709, 400)
        pyautogui.click(875, 400)
        pyautogui.write(self.imagery_date)

        # 20 고정
        for _ in range(11):
            pyautogui.click(676, 469)
        for _ in range(8):
            pyautogui.click(951, 469)

        pyautogui.click(663, 583)
        pyautogui.write(self.left_lng)
        pyautogui.press('Tab')
        pyautogui.write(self.right_lng)
        pyautogui.press('Tab')
        pyautogui.write(self.top_lat)
        pyautogui.press('Tab')
        pyautogui.write(self.bottom_lat)
        pyautogui.doubleClick(711, 711)
        pyautogui.press('Backspace')
        pyautogui.press('Backspace')
        pyautogui.press('Backspace')
        pyautogui.write(self.save_path)
        pyautogui.click(896, 798)

    def check_download_log(self, percent_404):
        self.log_path = f'{self.save_path}\\{self.scene_name}_log.txt'
        count_not_found = 0
        ctrl_lock = False
        basetime = time.time()

        time.sleep(10)
        # ================ Count Of Images =========================
        pyautogui.click(896, 798)
        time.sleep(5)
        pyautogui.press('Enter')
        f = open(self.log_path, 'r')
        lines = f.readlines()
        for line in lines:
            if 'Total count of images' in line:
                images = int(line.split()[-1])
                if images > 35000:
                    raise ToomanyImages()
        f.close()
        print("choosen count of 404",int(images * percent_404 / 100))
        time.sleep(1)
        pyautogui.click(896, 798)
        time.sleep(10)
        # ==================== 404 Not Found ========================
        while True:
            if ctrl_lock == True:
                print(ctrl_lock)
                break
            pyautogui.click(896, 798)
            time.sleep(4.5)
            pyautogui.click(965, 573)
            f = open(self.log_path, 'r')
            lines = f.readlines()
            f.close()
            for line in lines:
                if '404 Not Found' in line:
                    count_not_found += 1

            if count_not_found > int(images * percent_404 / 100):
                raise ToomanyNotFound()

            def finished():
                print("call finished()")
                f = open(self.log_path, 'r')
                lines = f.readlines()
                f.close()
                if lines[-5].strip() == 'Task finished!':
                    print('Task finished!')
                    pyautogui.press('Enter')
                    pyautogui.click(1425, 228)
                    return True

            pyautogui.click(896, 798)

            for _ in range(200):
                if ctrl_lock == True:
                    tm = time.time() - basetime
                    timestr = str(timedelta(seconds=tm))
                    fa = open(self.log_path, 'a')
                    lines = fa.write("processing time : " + timestr)
                    fa.close()
                    return timestr
                else:
                    ctrl_lock = finished()
                time.sleep(3)
    
    def check_combined_log(self):

        self.log_path = f'{self.save_path}\\{self.scene_name}_combined\\{self.scene_name}_zoom_20_combine_log.txt'
        while True:
            if os.path.exists(self.log_path):
                f = open(self.log_path, 'r')
                lines = f.readlines()
                f.close()
                if lines[-2].strip() == 'All operations finished!':
                    print('All operations finished!')
                    pyautogui.press('Enter')
                    pyautogui.click(1420, 272)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(2)

    def auto_combine(self):
        pyautogui.click(459, 1049)
        time.sleep(2)
        pyautogui.click(913, 338)
        time.sleep(1)
        pyautogui.write(self.combine_path)
        pyautogui.press('Enter')
        pyautogui.click(749, 775)
        time.sleep(3)


    def exit_gep(self):
        pyautogui.click(400, 1054)
        time.sleep(1)
        pyautogui.click(1425, 228)

        pyautogui.click(459, 1049)
        time.sleep(1)
        pyautogui.click(1420, 272)