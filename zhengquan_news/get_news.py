

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
    if len(item)>2 and item.find("\u3000\u3000")==0:
        item=item.replace("\u3000\u3000","")
    return item

headers={
'Cache-Control': 'max-age=0',
'If-None-Match': '"5e03f6a0-14988"V=17300DDB'


}

for url in urls:
    # url="https://finance.sina.com.cn/stock/y/2019-12-26/doc-iihnzahk0015581.shtml"

#对网址循环发请求，返回网址内容
    content=requests.get(url,headers=headers).content.decode("utf-8")



    #将内容转换成标准的html
    content_html=etree.HTML(content)



    #解析内容页的html
    ##解析报社列表
    papers=content_html.xpath("//*[@id=\"artibody\"]/p/strong/text()")
    ##解析报社内容列表
    # %%
    news = content_html.xpath("(//*[@id=\"artibody\"]/p/text())")

#注意：这部分是在正常的情况下（白天，新闻里面有股价信息，打乱了标签，需要处理）
#--------------------------------------------------------------------------------------------------------------------
    # news = content_html.xpath("(//*[@id=\"artibody\"]/p/text()) | (//*[@id=\"artibody\"]/p/span/a/text())")
    # index_bug = []
    # # 找到有bug的新闻
    # for index, new in enumerate(news[:-2]):
    #     if (new not in ["\u3000\u3000", '\xa0']) and (news[index + 1] != "\u3000\u3000"):
    #         index_bug.append(index)
    #         index_bug = list(set(index_bug))
    #         index_bug.append(index + 1)
    # remember = 0  # 动态的删除元素，需要记录
    # news_bug = ""
    # for index, new in enumerate(news):
    #     if index in index_bug:
    #         news_bug += news[index - remember]
    #         del news[index - remember]
    #         remember += 1
    # try:
    #     news.insert(min(index_bug), news_bug)
    # except:
    #     pass

#--------------------------------------------------------------------------------------------------------------------

    #数据格式化
    news=list(map(delete_space,news))

    ##删除新闻中的无用字符
    real_news=[]
    for i in news:
        if (i.find("责任编辑") != 0) and (i not in ['\xa0\xa0', '\u3000\u3000']):
            real_news.append(i)



    ##确定报纸的顺序
    real_paper= ["中国证券报","证券时报","上海证券报","证券日报"]
    final_paper=[paper for paper in papers if paper in real_paper]
    #新闻标题
    news_titles=[paper.replace('\u3000','') for paper in papers if paper not in real_paper]
    print(len(real_news),url)




