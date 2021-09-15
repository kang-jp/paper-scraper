import requests
from bs4 import BeautifulSoup

# search_word = input("enter words for seaching : ")
search_word = "well-being"

"""
q         : 検索ワード
range     : 検索方法？(本文含む, 著者検索など)
count     : 表示量 (上限200ぽい)
sortorder : 表示順番 (2: 出版年が古い順)
type      : ブラウザのUIの種類 
"""
response = requests.get("https://ci.nii.ac.jp/search?q=%s&range=0&count=200&sortorder=2&type=0" % (search_word))
soup = BeautifulSoup(response.text,"html.parser")

result_list = soup.find(attrs={"id":"resultlist"})

seach_result_papers_number = result_list.div.h1.text
papers_number = int(seach_result_papers_number.strip("\n検索結果\n\t\n\t").split("件")[0])
print("見つかった論文数 : ",papers_number)


for start in range(0,papers_number,200):
    response = requests.get("https://ci.nii.ac.jp/search?q=%s&range=0&count=200&sortorder=2&type=0&start=%s" % (search_word,start+1))
    each_soup = BeautifulSoup(response.text,"html.parser")
    each_result_paper_list = each_soup.find(attrs={"id":"itemlistbox"}).ul.find_all("li")
    for item in each_result_paper_list:
        try:
            title = item.div.dl.dt.a.text.replace("\n","").replace("\t","")
            print("title : ",title)
            authors = item.div.dl.dd.p.text.replace("\n","").replace("\t","")
            print("authors : ",authors.split(","))
        except:
            print("error")
