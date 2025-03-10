import requests
from bs4 import BeautifulSoup
import feedparser
import json
RSS_FEEDS={"BBC":"http://feeds.bbci.co.uk/news/rss.xml","CNN":"http://rss.cnn.com/rss/edition.rss","Al Jazeera":"https://www.aljazeera.com/xml/rss/all.xml","TechCrunch":"https://feeds.feedburner.com/TechCrunch/","The Verge":"https://www.theverge.com/rss/index.xml"}
def scrape_rss():
    a=[]
    for b,c in RSS_FEEDS.items():
        d=feedparser.parse(c)
        for e in d.entries[:10]:
            a.append({"source":b,"title":e.title,"url":e.link,"summary":e.get("summary","No summary available")})
    return a
def scrape_quora(topic="technology"):
    f=f"https://www.quora.com/topic/{topic}"
    g={"User-Agent":"Mozilla/5.0"}
    h=requests.get(f,headers=g)
    i=BeautifulSoup(h.text,"html.parser")
    j=[]
    for k in i.select("a.q-box.qu-cursor--pointer")[:10]:
        j.append({"question":k.text.strip(),"url":"https://www.quora.com"+k["href"]})
    return j
def scrape_stackoverflow(tag="python"):
    l=f"https://stackoverflow.com/questions/tagged/{tag}?sort=votes"
    m={"User-Agent":"Mozilla/5.0"}
    n=requests.get(l,headers=m)
    o=BeautifulSoup(n.text,"html.parser")
    p=[]
    for q in o.select(".s-post-summary--content-title a")[:10]:
        p.append({"question":q.text.strip(),"url":"https://stackoverflow.com"+q["href"]})
    return p
def scrape_producthunt():
    r="https://www.producthunt.com/"
    s={"User-Agent":"Mozilla/5.0"}
    t=requests.get(r,headers=s)
    u=BeautifulSoup(t.text,"html.parser")
    v=[]
    for w in u.select("h3[data-test='post-name']")[:10]:
        v.append({"product":w.text.strip(),"url":"https://www.producthunt.com"})
    return v
def main():
    x=scrape_quora()
    y=scrape_stackoverflow()
    z=scrape_producthunt()
    aa=scrape_rss()
    ab={"quora":x,"stackoverflow":y,"producthunt":z,"news":aa}
    with open("data/scraped_data.json","w",encoding="utf-8") as ac:
        json.dump(ab,ac,indent=4,ensure_ascii=False)
if __name__=="__main__":
    main()