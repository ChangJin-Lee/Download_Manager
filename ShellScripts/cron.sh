DIRECTORY="/mnt/d/Capella_data"

(time aws s3 sync --no-sign-request s3://capella-open-data/data/ $DIRECTORY --exclude 'tiledb/*') > /mnt/c/Users/SIA/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log_$(date +'%Y-%m-%d').txt 2>&1 && cp /mnt/c/Users/SIA/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log_$(date +'%Y-%m-%d').txt /mnt/c/Users/SIA/DOWNLOAD_MANAGER/Capella_Cron/aws_s3_log.txt