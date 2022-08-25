# Download_Manager

## Introduce
Google Earth Pro, Capella open-data-set의 영상 데이터 다운로드를 자동화하는 프로젝트 입니다. Streamlit으로 UI를 시각화 했습니다.

<br/>

## Software development environment

|항목|내용|비고|
|:---:|:---:|:---:|
|OS|Windows 11 21H2 ||
|OS|WSL2 Ubuntu-20.04||
|Python|3.8.10||
|awscli|1.25.39||
|boto3|1.24.54||
|botocore|1.27.54||
|capella-console-client|0.8.3||
|geopandas|0.11.0||
|file-read-backwards|2.0.0||

<br/>

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

사진 붙이기

<br/>

## How to Use?

### How to run to cron?
| Parameter          | Format                          |
|----------------------|--------------------------------------------------------|
| cron expression       | * * * * *                 |
| DIRECTORY             | /write/your/path          |