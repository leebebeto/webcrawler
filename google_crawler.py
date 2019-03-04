from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd
import os 
import csv
import pickle
#direct your workspace 
os.chdir("C:/Users/SAMSUNG/for_git/")

stay_together = pd.read_csv("google_crawler/Sample_data.csv")
driver = webdriver.Chrome('chromedriver.exe') #direct your chromedriver path here
driver.get("https://www.google.com")
result = []

def search(title, artist , index):
	song_lyric = []
	try:
		search= driver.find_element_by_name('q')
		search.send_keys(title+' lyrics')
		search.send_keys(Keys.RETURN) 
		html = driver.page_source
		driver.implicitly_wait(3)
		soup = BeautifulSoup(html,'html.parser')    
		lyric_upper_tag = soup.find_all('span', {'jsname':'YS01Ge'})
		for words in lyric_upper_tag:
		    song_lyric.append(words.get_text())
		driver.find_element_by_name('q').clear()

	except:
	    print(str(index)+" "+title+" "+artist+" uncompleted Try again!")
	print('%.4f' % (index/stay_together.shape[0]) +" completed")   
	return {
		"index" : index+1,
		"title" : title,
		"artist" : artist,
		"song_lyric" : song_lyric
	}

for i in range(stay_together.shape[0]):
	# Made this condition in order to avoid robot-asking problem
	if (i%15==0 and i>1):
		driver.quit()
		driver = webdriver.Chrome('chromedriver.exe') #direct your chromedriver path here
		driver.get("https://www.google.com")
	song = stay_together['title'].iloc[i]
	artist = stay_together['artist'].iloc[i]
	result.append(search(song, artist, i))
keys = result[0].keys()
driver.quit()
stay_together_with_lyrics_df = pd.DataFrame(columns = ("index", "title", "artist", "song_lyric"))
for i in range(len(result)):
	stay_together_with_lyrics_df.loc[i] = result[i]

#save as csv
with open('data_with_lyrics.csv', 'w', encoding="utf-8") as f: #store the data as a txt file.
    dict_writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)

#save as pickle    
with open('data_with_lyrics.pickle', 'wb') as pkl:
   pickle.dump(stay_together_with_lyrics_df,pkl)