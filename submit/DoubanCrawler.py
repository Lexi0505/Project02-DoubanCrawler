import requests
import bs4
import expanddouban as e
import csv
import codecs

url = None



def getMovieUrl(category, location):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category,location)

    return url

class Movie:
    def __init__(self,name,rate,location,category,info_link,cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

def getLocations():
    html = e.getHtml('https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    temp = soup.find(id = 'content').find(class_ = 'category').next_sibling.next_sibling
    movie_location = []
    for element in temp:
        if element.string!= '全部地区':
            movie_location.append(element.string)
    return movie_location


def getMovies(category, location):
    movie_list = []
    html = e.getHtml(getMovieUrl(category,location),True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    target_div = soup.find(id = 'content').find(class_ = 'list-wp')
    for child in target_div:
        name = child.find(class_ = 'title').string
        rate = child.find(class_ = 'rate').string
        info_link = child.get('href')
        cover_link = child.find('img').get('src')
        movie_list.append([name,rate,location,category,info_link,cover_link])
    return movie_list



data = []
temp_list = []
movie_category = input('pls inupt three ur favorate types, seperate with English verison comma:').split(',')

location_list = getLocations()

for m_category in movie_category:
    for loc in location_list:
        data.append(getMovies(m_category,loc))

with codecs.open('movies.csv','w','utf_8_sig') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerows(row)


with codecs.open('movies.csv','r','utf_8_sig') as f:
    reader = csv.reader(f)
    movie_items = list(reader)

result_dict = {}
for m_type in movie_category:
    total_num = 0
    analysis_dict = {}
    for m_loc in location_list:
        count = 0
        for item in movie_items:
            if item[3] == m_type and item[2] == m_loc:
                count +=1
                analysis_dict[item[2]] = count
        total_num = total_num + count
    result_dict = sorted(analysis_dict.items(), key = lambda x: x[1], reverse = True)


    if len(result_dict) >=3:
        temp_list.append('{}类型的电影,排名前三的分别为{},占比{}%,{}，占比{}%,{},占比{}%.'.format(m_type,result_dict[0][0],round((result_dict[0][1]/total_num*100),2),result_dict[1][0],round((result_dict[1][1]/total_num*100),2),result_dict[2][0],round((result_dict[2][1]/total_num*100),2)))
    if len(result_dict) == 2:
        temp_list.append('{}类型的电影,排名前三的分别为{},占比{}%,{},占比{}%,未找到符合条件的第三个地区.'.format(m_type,result_dict[0][0],round((result_dict[0][1]/total_num*100),2),result_dict[1][0],round((result_dict[1][1]/total_num*100),2)))
    if len(result_dict) == 1:
        temp_list.append('{}类型的电影,排名前三的分别为{},占比{}%,该类型符合条件的地区仅有一个.'.format(m_type,result_dict[0][0],round((result_dict[0][1]/total_num*100),2)))

output = codecs.open('output.txt','w','utf_8_sig')
for line in temp_list:
    print(line,file = output)
output.close()
