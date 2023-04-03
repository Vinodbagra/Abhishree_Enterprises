import requests
from bs4 import BeautifulSoup
import csv
import sqlite3

urlhome = "https://www.theverge.com/"

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

res = requests.get(urlhome)
html_c = res.content

s= BeautifulSoup(html_c, "html.parser")

a_tags_title = s.find_all('a', class_='group-hover:shadow-underline-franklin')
a_tags_autohors = s.find_all('a',class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8')
span_tags_dates = s.find_all('span',class_='text-gray-63 dark:text-gray-94')
a_tags_urls = s.find_all('a',class_='block h-full w-full')
titles = []
authors = []
dates = []
urls = []

for a_tag_title in a_tags_title:
    title = a_tag_title.text
    titles.append(title)
for a_tag_author in a_tags_autohors:
    author = a_tag_author.text
    authors.append(author)

for span_tag_date in span_tags_dates:
    date = span_tag_date.text
    dates.append(date)
for a_tag_url in a_tags_urls:
    url = urlhome + a_tag_url['href']
    urls.append(url)









filename = "articles_details.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['title','url','author','date'])
    for i in range(len(titles)):
        writer.writerow([titles[i],urls[i],authors[i],dates[i]])

cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                (id INTEGER PRIMARY KEY, title TEXT, url TEXT, author TEXT, date TEXT)''')

# Insert the data into the table
for i in range(len(titles)):
    title = titles[i]
    url = urls[i]
    author = authors[i]
    date = dates[i]

    cursor.execute("SELECT * FROM my_table WHERE title = ? AND url = ? AND author = ? AND date = ?", (title, url, author, date))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO my_table (title, url, author, date) VALUES (?, ?, ?, ?)", (title, url, author, date))

# Commit the changes and close the connection
conn.commit()
conn.close()