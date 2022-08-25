import streamlit as st
import boto3
from botocore.handlers import disable_signing
import os
from file_read_backwards import FileReadBackwards
from datetime import datetime

class view():
    def __init__(self):
        logsize = 0
        st.title('Capella CronJob')

        option = st.selectbox(
        'Select year',
        ('All', '2020', '2021', '2022'))

        contents, totalsize, cnt = self.capella_size(option)
        st.subheader("summarize")
        st.write( "year :  " + str(option))
        st.write( "count : " + str(cnt))
        st.write( "totalsize : " + str(totalsize))
        st.subheader("samples")

        with st.container():
            for content in contents:
                st.code(os.path.basename(content[0]) + "  " + str(content[1]))

        today = datetime.today().date()
        date = datetime(year=today.year, month=today.month, day=1).date()
        with FileReadBackwards(r"C:\Users\SIA\DOWNLOAD_MANAGER\Capella_Cron\aws_s3_log_" + str(date) +".txt", encoding="utf-8") as frb:
            completed_chk = False
            for l in frb:
                if l.split("	")[0] == "real":
                    st.success("sync success! ... last cronjob process time : " + str(l.split("	")[1]))
                elif l != "" and l.split()[0] == "Completed":
                    if l.split("/")[0].split(' ')[2] == l.split("/")[1].split(' ')[1]\
                    and l.split("/")[0].split(' ')[1] == l.split("/")[1].split(' ')[0]:
                        logsize = l.split("/")[0].split(' ')[2]
                        completed_chk = True
                        break
            if completed_chk == False:
                st.error("Something's wrong...... check 'aws_s3_log.txt' ")
            if option == 'All' and logsize < totalsize:
                st.error("new data updated in aws s3... plaese download manualy")

    def capella_size(self,option):
        sizes, cnt, objcontents = 0, 0, []
        
        if option == "All":
            option = ""

        def sizeof_fmt(num, suffix="B"):
            for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
                if abs(num) < 1024.0:
                    return f"{num:3.1f} {unit}{suffix}"
                num /= 1024.0
            return f"{num:.1f}Yi {suffix}"

        resource = boto3.resource('s3')
        resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        bucket = resource.Bucket('capella-open-data')

        for obj in bucket.objects.filter(Prefix='data/'+option):
            if 'tiledb/' not in obj.key:
                if len(objcontents) < 5 and obj.key.split('.')[-1] == 'tif' and '_preview' not in obj.key and obj.key not in objcontents:
                    objcontents.append([obj.key, sizeof_fmt(obj.size)])
                sizes += obj.size
                cnt += 1

        return objcontents, sizeof_fmt(sizes), cnt