# Download_Manager

## Introduce
Google Earth Pro, Capella open-data-set의 영상 데이터 다운로드를 자동화하는 프로젝트 입니다. Streamlit으로 UI를 시각화 했습니다.

<br/>

## Software development environment

|항목|내용|비고|
|:---:|:---:|:---:|
|OS|Windows 11 21H2,  WSL2 Ubuntu-20.04||
|Visual Studio | 1.70.2| |
|Python|3.8.10||
|Anaconda Navigator| 2.2.0||

## Python Package

|항목|내용|비고|
|:---:|:---:|:---:|
|awscli|1.25.39||
|boto3|1.24.54||
|botocore|1.27.54||
|capella-console-client|0.8.3||
|geopandas|0.11.0||
|file-read-backwards|2.0.0||
|streamlit|1.12.0|||
|streamlit_option_menu|0.3.2||
|pyautogui|0.9.53||
|datetime|4.5||

<br/>

### Precautions
- you must run this prgram after all jobs done.
- In GEP Downloader Page, you need to asure that DateTime is valid. if DateTime not valid, maybe this program will download wrong file that has DateTime.
- if Capella CronJob page show error message something like "download failed...", you must check ./Capella_Cron/aws_s3_log.txt first. then execute ./ShellScripts/cron.sh manually.

## How to Run?

> you need to run this program at specific local computer

1. Execute ananconda

2. Environments -> GEP -> Open terminal

3. Run command in terminal
```
 cd C:\Users\SIA\DOWNLOAD_MANAGER
``` 
```
 streamlit run home.py
```

```

# Directory 구조
    .
    └── home.py
    └── Capella_Cron
        ├── Capella_Cron.py
        └── servers.json # For Setting
    └── GEP_Downloader
        ├── download_base.py
        └── gep_downloader.py
    └── ShellScripts
        └── cron.sh
```
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/54494793/186603080-92ff8d4a-0a00-4d1b-a48a-18a519c04ca9.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/54494793/186603447-02d5276f-f805-4606-9865-c2656edd3f79.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/54494793/186603459-e7b7d19b-7805-45e2-babd-5b77e9cf6e45.png" /></td>
  <tr>
</table>

- We Select 4 polygon point, Although data has random polygon

<table>
  <tr>
<td><img alt="" src="https://user-images.githubusercontent.com/54494793/186603459-e7b7d19b-7805-45e2-babd-5b77e9cf6e45.png" /></td>
  <tr>
</table>


<br/>

## How to Use?

### How to run to cron?

1. Run command in terminal

```
 crontab -e
```

2. wrtie cron expression

input [pwd] that is your home path


```
 30 0 * * 6 (time aws s3 sync --no-sign-request s3://capella-open-data/data/2020 ./capelladata/2020 --exclude 'tiledb/*') > [pwd]/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log_$(date +'%Y-%m-%d').txt 2>&1 && cp [pwd]/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log_$(date +'%Y-%m-%d').txt [pwd]/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log.txt
```


| Parameter          | Format                          |
|----------------------|--------------------------------------------------------|
| cron expression       | * * * * *                 |
| DIRECTORY             | /write/your/path          |
