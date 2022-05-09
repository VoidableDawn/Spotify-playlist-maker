import requests
from bs4 import BeautifulSoup

user_input = input("Which year do you want to travel to? Enter the year in this format YYYY-MM-DD:\n")

print(user_input)

url = f"https://www.billboard.com/charts/hot-100/{user_input}/"

response = requests.get(url = url).text
soup = BeautifulSoup(response, "html.parser")

# sse = soup.find_all(name = "li", class_ = "lrv-u-width-100p")
# print(sse)

artists = soup.find_all(name = "span",
                        class_ = "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
song_artists = [name.get_text().split("\n\t\n\t")[1].split("\n")[0] for name in artists if name is not None]

titles = soup.find_all(name = "h3",
                       class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
song_titles = [title.get_text().split("\t")[9] for title in titles if title is not None]

with open(file = "top_songs.txt", mode = "w", encoding = "utf-8") as file:
    try:
        for i in range(0, 99):
            file.write(f"{i + 1}. {song_titles[i]} by {song_artists[i]}\n")
    except IndexError:
        print("There was an Index Error out of range")
