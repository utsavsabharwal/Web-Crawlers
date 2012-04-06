#!/bin/bash
echo "This is pycURL v2 crawler only for crawling 1M + urls. For better performance on smaller files use fecther machine."
phase=$( date | tr -d ' ' )
k=$phase
phase=/mnt1/$phase
mkdir $phase 
echo Created directory $phase
echo "Fetching urls"
echo "Enter where clause. Press Enter for none."
cd $phase
read clause
mysql -uroot -h10.241.31.96 spider -e "select distinct rdomain, uid, url, product_id from url_queue ${clause}" >> urls
echo "Starting URL Scheduling"
cd /home/curl/
python scheduler.py $phase
echo "Starting Crawler"
mv /mnt/$phase/url /mnt/phase/urls
python crawler.py $phase
echo "Creating db queries"
python query.py $phase
echo "Updating db"
mysql -uroot -h10.241.31.96 spider < query
echo "Scheduling Upload"
python upload.py $phase
echo "Starting Uplaoding. Please check processor is on."
cd /home/spider/production/veetwo
paster job_runner --configuration-file machine/ec2/spider/ini/spider.ini --job-name=fetcher:Starter $phase
echo "Completed. Thankyou for your patience."


