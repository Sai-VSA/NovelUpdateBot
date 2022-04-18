from bs4 import BeautifulSoup
from database import return_recent, add_recent
import discord, os
from discord.ext import commands, tasks
import requests

def return_chap(chap_num, url, id):
    recent = return_recent(id)
    html_text = requests.get(url).text
#html script from website
    soup = BeautifulSoup(html_text, 'lxml')
#text reader
    chapter_list = soup.find_all('li', class_ = "listing-item")
    content = soup.find("div", class_ = "site-content")
    nn = content.find("h2")
    novel_name = nn.contents[0]

    for cnum, chap in enumerate(reversed(chapter_list)):
        chapter_name = chap.find('a', class_ = "title") #code
        chapter_name1 = chapter_name.text
        if str(chap_num) in chapter_name1:
            chapter_link = chapter_name['href']
          #  if int(chap_num) > int(recent):
            #  add_recent(id, chapter_list)
            if(chap_num >  recent):
              add_recent(id, chap_num)
            return discord.Embed(title = novel_name + " " + str(chap_num), url = chapter_link, color = discord.Color.blue())
        else: 
            num = int(cnum + 1);
            

    ##edit later to return recent chap based on save
    ##chapterPage = requests.get(chapter_link).text
    ##subSoup = BeautifulSoup(chapterPage, 'lxml')
    ##story = subSoup.find('div', class_ = "entry-content").text
    add_recent(id, num)
    return -1



