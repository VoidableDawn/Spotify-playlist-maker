import requests
from bs4 import BeautifulSoup

url = ""


def get_user_input():
    global url, user_input
    user_input = input("Which year do you want to travel to? Enter the year in this format YYYY-MM-DD:\n")
    year = user_input.split("-")[0]
    print(user_input)
    url = f"https://www.billboard.com/charts/hot-100/{user_input}/"
    return user_input


def get_soup():
    response = requests.get(url = url).text
    soup = BeautifulSoup(response, "html.parser")
    return soup


# Using bs4 to scrap the top 100 songs data from the billboard site
def get_top_songs(soup):
    artists = soup.find_all(name = "span",
                            class_ = "c-label a-no-trucate a-font-primary-s lrv-u-font-size"
                                     "-14@mobile-max u-line-height-normal@mobile-max u-letter"
                                     "-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line"
                                     " u-max-width-330 u-max-width-230@tablet-only")
    song_artists = [name.get_text().split("\n\t\n\t")[1].split("\n")[0] for name in artists if name is not None]
    titles = soup.find_all(name = "h3",
                           class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing"
                                    "-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height"
                                    "-125 u-line-height-normal@mobile-max a-truncate-ellipsis "
                                    "u-max-width-330 u-max-width-230@tablet-only")
    song_titles = [title.get_text().split("\t")[9] for title in titles if title is not None]
    return song_artists, song_titles


# Saving the gotten songs to a local text file
def save_top_songs(song_artists, song_titles, date):
    with open(file = f"songs_lists/top_songs{date}", mode = "w", encoding = "utf-8") as file:
        try:
            for idx in range(0, 99):
                file.write(f"{song_titles[idx]} by {song_artists[idx]}\n")
        except IndexError:
            print("There was an Index Error out of range")
