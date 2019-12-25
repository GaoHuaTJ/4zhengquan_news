
import requests
#发请求
day_sum_url="http://finance.sina.com.cn/focus/zqbjh/"
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
response=requests.get(url=day_sum_url,headers=headers)
#将返回的结果进行储存
html_text=response.content.decode("utf-8")
#将文本转换成标准的html
from lxml import  etree
html=etree.HTML(html_text)
#解析网址
urls=html.xpath("//div/ul[@class=\"list_009\"]/li/a/@href")
#解析标题
titles=html.xpath("//div/ul[@class=\"list_009\"]/li/a/text()")
#解析发布日期
dates=html.xpath("//div/ul[@class=\"list_009\"]/li/span/text()")
##删除每一个字符元素中的前后空格
def delete_space(item):
    if len(item) > 2 and item.find("\u3000\u3000") == 0:
        item = item.replace("\u3000\u3000", "")
    return item
#对网址循环发请求，返回网址内容
for url in urls:
    content=requests.get(urls,headers=headers).content.decode("utf-8")
    #将内容转换成标准的html
    content_html=etree.HTML(content)
    #解析内容页的html
    ##解析报社列表
    papers=content_html.xpath("//*[@id=\"artibody\"]/p/strong/text()")
    ##解析报社内容列表
    news=content_html.xpath("//*[@id=\"artibody\"]/p/text()")
    #数据格式化
    news=list(map(delete_space,news))
    ##删除新闻中的无用字符
    for i in news:
        if (i.find("责任编辑")==0) or i in ['\xa0\xa0','\u3000\u3000']:
            news.remove(i)
        if i=="\u3000\u3000":#这里要删两边，不知道为什么一遍删不全
            news.remove(i)
    ##确定报纸的顺序
    real_paper= ["中国证券报","证券时报","上海证券报","证券日报"]
    final_paper=[paper for paper in papers if paper in real_paper]
    #新闻标题
    news_titles=[paper.replace('\u3000','') for paper in papers if paper not in real_paper]



