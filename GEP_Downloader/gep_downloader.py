import streamlit as st
import json
from GEP_Downloader.download_base import Base, ToomanyNotFound, ToomanyImages, PyAutoGuiForGEP
import time
from datetime import timedelta

class view():
    def __init__(self):
        st.title('GEP Downloader')

        total_data = {'aoi':'', 'date':'', 'geog':{'max_lng':'', 'min_lng':'', 'max_lat':'', 'min_lat':''}}
        title = st.text_input('Area Name')
        total_data['aoi'] = title

        txt_widget = st.empty()
        date_time = txt_widget.date_input( "DateTime")
        date = Base.datetime_to_time(date_time)
        total_data['date'] = date

        def calc_area():
            st.session_state['area'] = st.session_state['side']
            st.session_state['slider_side'] = st.session_state['side'] 

        def calc_side():
            st.session_state['side'] = st.session_state['area']
            st.session_state['slider_side'] = st.session_state['side']

        def slider_input():
            st.session_state['side'] = st.session_state['slider_side']
            st.session_state['area'] = st.session_state['slider_side']
            
        def show_error(str):
            st.error(str)

        percent_404 = st.number_input("Select a percent of the 404 not found:", key='side', on_change = calc_area)
        st.slider('Select a percent of the 404 not found :', key='slider_side', on_change = slider_input)

        uploaded_file = st.file_uploader("Choose a kml file")
        if uploaded_file is not None:

            max_lng, min_lng, max_lat, min_lat = Base.kml_to_lat_lng(uploaded_file)
            total_data['geog']['max_lng'] = max_lng
            total_data['geog']['min_lng'] = min_lng
            total_data['geog']['max_lat'] = max_lat
            total_data['geog']['min_lat'] = min_lat

            json_path = f"C:\\Users\\SIA\\GEP_DOWNLOADER\\json\\{total_data['aoi']}_{total_data['date']}.json"
            with open(json_path,'w') as f:
                json.dump(total_data, f, ensure_ascii=False, indent=4)
            st.write(total_data)


            if total_data['aoi'] and total_data['date'] \
                and total_data['geog']['max_lng'] and total_data['geog']['min_lng'] \
                and total_data['geog']['max_lat'] and total_data['geog']['min_lat']:

                if st.button('Download'):

                    pag = PyAutoGuiForGEP(json_path)
                    try:
                        basetime = time.time()
                        pag.make_dir(pag.save_path)
                        pag.scene_name_time_define(pag.aoi_date, pag.save_path)
                        pag.auto_input_gep()
                        processingtime = pag.check_download_log(int(percent_404))
                        pag.auto_combine()
                        pag.check_combined_log()
                        st.success(f'complete {pag.aoi_date}_{pag.aoi}')
                        st.success(f'processing time    {processingtime.split(".")[0]}')
                        tm = time.time() - basetime
                        timestr = str(timedelta(seconds=tm))
                        st.success(f'Total time    {timestr.split(".")[0]}')
                        pag.exit_gep()
                    except ToomanyNotFound:
                        show_error("Too many 404 Not Found... ")
                    except ToomanyImages:
                        show_error("Too many Images... ")
                    except:
                        show_error('Download Failed... Please Check Terminal')
                        pag.exit_gep()
                else:
                    pass