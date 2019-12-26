# 2019.12.26 高华，完结
import pandas as pd
import requests,sys,datetime
from lxml import etree

# 发请求
day_sum_url = "http://finance.sina.com.cn/focus/zqbjh/"  # 总览页的地址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
response = requests.get(url=day_sum_url, headers=headers)  # 获得总览页的返回值
html_text = response.content.decode("utf-8")  # 将返回的结果进行转码并储存
html = etree.HTML(html_text)  # 将文本转换成标准的html
urls = html.xpath("//div/ul[@class=\"list_009\"]/li/a/@href")  # 解析网址
titles = html.xpath("//div/ul[@class=\"list_009\"]/li/a/text()")  # 解析标题
dates = html.xpath("//div/ul[@class=\"list_009\"]/li/span/text()")  # 解析发布日期
df = pd.DataFrame(columns=["时间", "报刊", "标题", "新闻内容"])
# 对网址循环发请求，返回网址内容


for index, url in enumerate(urls):
    sys.stdout.flush()
    sys.stdout.write(f"\r第{index+1}/{len(urls)}次请求")
    content = requests.get(url, headers=headers).content.decode("utf-8")
    content_html = etree.HTML(content)  # 将内容转换成标准的html
    news = []
    nodes = content_html.xpath("//*[@id=\"artibody\"]/p")
    for node in nodes:
        news.append(node.xpath("string(.)"))
    news = [new.strip() for new in news if new.find("责任编辑") == -1]
    real_paper = ["中国证券报", "证券时报", "上海证券报", "证券日报"]
    final_paper = []  # 存储最后的正确顺序的报纸
    news_titles = []  # 存储新闻标题
    news_contents = []  # 存储新闻内容
    for new in news:
        if new in real_paper:
            final_paper = final_paper + [new] * 4
            for i in range(1, 9):
                if i % 2 != 0:
                    news_titles.append(news[news.index(new) + i])
                else:
                    news_contents.append(news[news.index(new) + i])

    # 定义时间列表
    date = [
        datetime.datetime.strptime(
            dates[index].replace(
                "(",
                "").replace(
                ")",
                ""),
            '%Y-%m-%d %H:%M:%S').date()] * len(news_titles)
    df_temp = pd.DataFrame(
        {'时间': date, '报刊': final_paper, '标题': news_titles, '新闻内容': news_contents})
    df = df.append(df_temp)


df=df.sort_values(by='时间')  # 按照时间先后排序
df.to_excel(r"四大证券报.xlsx", encoding='gb2312', index=0)  # 输出到excel

print("\n运行结束")