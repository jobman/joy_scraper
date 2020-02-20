import requests
from bs4 import BeautifulSoup
import time
import random

print('import ok')


def process_page(page):
    try:
        soup = BeautifulSoup(page)
        post_list = soup.find_all('div', {'class': 'postContainer'})
        for post in post_list:
            try:
                process_post(post)
            except Exception:
                print('Не могу обработать пост')
    except Exception:
        print('Не могу обработать страницу')


def process_post(post):
    try:
        content = post.find('div', {'class': 'post_content'})
        images_sources, images_extensions = process_content(content)
        rating = post.find('span', {'class': 'post_rating'}).text
        date = post.find('span', {'class': 'non-localized-time'}).get('data-time')
        filename = 'best_from_joy/' + date + ' ' + rating
        for image, id in zip(images_sources, range(len(images_sources))):
            name = filename + ' ' + str(id) + ' ' + images_extensions[id]
            save_image(image, name)
    except Exception:
        print('Не могу обработать пост')


def process_content(content):
    images = content.find_all('div', {'class': 'image'})
    images_sources = []
    images_extensions = []
    for image in images:
        try:
            image_src = image.find('img').get('src')
            file_type = image_src[image_src.rfind('.'):]
        except Exception:
            print('Не могу найти изображение в контенте')
            return None
        images_extensions.append(file_type)
        images_sources.append(image_src)
    return images_sources, images_extensions


def save_image(url, filename):
    try:
        img = requests.get(url)
        out = open(filename, 'wb')
        out.write(img.content)
        out.close()
    except Exception:
        print('Не могу сохранить изображение с url', url)


url = 'http://joyreactor.cc/best/'

number_of_pages = 8224
t = 5
for i in range(1, number_of_pages + 1):
    print('Старт обработки', i, 'страницы')
    current_url = url + str(i)
    print('Текущий адресс запроса:')
    print(current_url)
    start_time = time.time()
    r = requests.get(current_url)
    with open('temp.html', 'wb') as output_file:
        output_file.write(r.text.encode('utf-8'))
    with open('temp.html', 'r', encoding='utf-8') as file:
        text = file.read()
        process_page(text)
    print('Страница', i, 'обработана за %.3s секунды' % (time.time() - start_time))
    print('Временная задержка', t, 'секунд')
    print()
    t = random.randrange(3, 5, 1)
    time.sleep(t)
