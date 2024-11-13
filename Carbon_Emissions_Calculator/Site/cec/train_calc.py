from bs4 import BeautifulSoup
import requests
import datetime

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Thu, 05 Sep 2024 09:06:46 GMT',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"128.0.661.120"',
    'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.119", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.119"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.5.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
def encode(string):
    data =  {
        'input': string,
        'charset': 'CP936',
        'separator': 'lf',
    }
    response = requests.post('https://www.urlencoder.org/',headers=headers,data=data)
    soup = BeautifulSoup(response.text,'lxml')
    code = str(soup.find_all('textarea')[-1]).replace('</textarea>','')
    code = code[code.rfind(">")+1:]
    return code
def listify(string):
    array = string.split('</td>\n<td bgcolor="#F6F6F6" class="STYLE8">')
    return [array[0][array[0].find(">")+1:],int(array[-1].replace("km ",'')) if (array[-1] != '') else (0)]
def finddist(start,end,identification):
    url = "https://skb.gaotie.cn/checi.asp?checi="+identification
    text = requests.get(url,headers=headers).text
    soup = BeautifulSoup(text,"lxml")
    table_rows = soup.find_all('tr')
    station_rail = []
    for station in table_rows:
        if "https://skb.gaotie.cn/zhan.asp?zhan=" in str(station) and '<td class="STYLE5" colspan="2" height="20">' not in str(station):
            station_rail.append(listify(str(station).replace('<tr><td bgcolor="#F9F9F9" class="STYLE8" height="35"><a class="STYLE10" href="https://skb.gaotie.cn/zhan.asp?zhan=','').replace("</a>",'').replace("</td>\n</tr>","")))
    station_rail=dict(station_rail)
    distance = abs(station_rail.get(end)-station_rail.get(start))
    return distance
def calculator(start,end,identification):
    start = start.split(' ')[-1]
    end = end.split(' ')[-1]
    if identification != '':
        distance = finddist(start,end,identification)
        return round(distance * 0.03048,2)
    else:
        start = encode(start)
        end = encode(end)
        url = 'https://shike.gaotie.cn/mlieche.asp?from='+start+'&to='+end
        text = requests.get(url,headers=headers).text
        soup = BeautifulSoup(text,'lxml')
        table_data = soup.find_all("td")
        dists = []
        for data in table_data:
            if "km</td>" in str(data):
                dists.append(int(str(data)[str(data).find("距离")+2:-7]))
        distance = sum(dists)/len(dists)
        return round(distance * 0.03048,2)
print(calculator("Chang Shu 常熟","Cheng Du Dong 成都东",''))