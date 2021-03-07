import requests
from bs4 import BeautifulSoup
import csv
import re
def PhoneCheck(Telephone):
    pattern=re.compile(r'^(\(02|\(044)')
    if re.match(pattern,Telephone):
        return 1
    else:
        return 0
header = {
        'Host': 'www.autotrader.co.uk',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.autotrader.co.uk/',
        'Connection': 'close',
        'Cookie': '__cfduid=d7cf8cc2f0f145fdcecd6be0063afd6f31615016257; abtcid=16a0c5fa_8aec_496e_9ff0_552521f74cfc; bucket=desktop; sessVar=64480fa7-e994-4437-ba0e-cd397abfa940; userid=ID=85629498-3f76-45e4-a3b0-cd2725011cc7; user=STATUS=0&HASH=5a31ff484efb556910f8a61c2ba6bca9&PR=&ID=85629498-3f76-45e4-a3b0-cd2725011cc7; GeoLocation=Town=&Northing=&Latitude=51.556568272&Easting=&ACN=0&Postcode=E113LD&Longitude=0.0094344562; SearchData=postcode=E113LD; postcode=postcode=E113LD; searches=; cookiePolicy=seen.; LPCKEY-p-245=2cbbc690-09c8-4419-ba02-67a5d12e3941c-29778%7Cnull%7CindexedDB%7C120; CAOCID=c302f942-3352-4919-9b09-5757ea75db11f-73231; abTestGroups=FPAI-afvI-ahC-rxI-smT-ctI-fdC-gp3-hp0I-iosellT1-nhT-orI-faT-rlI-ssA-search0I-spI-ucI-um0-ut0-uhT-usrI-viI; ctmQuickQuotes=%7B%7D'
    }
url = 'https://www.autotrader.co.uk/car-search?advertClassification=standard&postcode=E113LD&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&is-quick-search=TRUE&include-delivery-option=on&page='
for page_number in range(1,50000):
    try:
        request = requests.get(url+str(page_number),headers=header)
        data = request.text
        soup = BeautifulSoup(data,features="html.parser")
        links = soup.find_all("a", class_="js-click-handler listing-fpa-link tracking-standard-link")
    except requests.exceptions.ConnectionError:
        print("Server is down or Check your internet")
        exit()
    car_links=open('car_links.txt','w+')
    for i in links:
        link = i.attrs['href']
        car_links.write("https://www.autotrader.co.uk"+link+"\n")


    headers2 = {
        'Host': 'www.autotrader.co.uk',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.autotrader.co.uk/',
        'Connection': 'close',
        'Cookie': '__cfduid=d7cf8cc2f0f145fdcecd6be0063afd6f31615016257; abtcid=16a0c5fa_8aec_496e_9ff0_552521f74cfc; userid=ID=85629498-3f76-45e4-a3b0-cd2725011cc7; user=STATUS=0&HASH=5a31ff484efb556910f8a61c2ba6bca9&PR=&ID=85629498-3f76-45e4-a3b0-cd2725011cc7; GeoLocation=Town=&Northing=&Latitude=51.556568272&Easting=&A'
    }
    car_links.close()
    try:
        car_link = open("car_links.txt",'r')
    except FileNotFoundError:
        print("File is not found!")
        exit()
    lines = car_link.readlines()
    fields = ["Number","isTradeSeller","Name"]
    csvfile = open("csvfile.csv",'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for line in lines:
        json_url = "https://www.autotrader.co.uk:443/json/fpa/initial/"
        carPage =  line[41:-1]
        req=requests.get(json_url+carPage,headers=headers2)
        json_req=req.json()
        Tel=json_req["seller"]["primaryContactNumber"]
        if PhoneCheck(Tel):
            Trace=json_req["seller"]["isTradeSeller"]
            Name=json_req["seller"]["name"]
            row = [Tel,Trace,Name]
            csvwriter.writerow(row)
car_links.close()
csvfile.close()


