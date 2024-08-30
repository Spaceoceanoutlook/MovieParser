import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def create_driver():
    # Создаем объект для открытия закрытия браузера
    service = Service(executable_path=ChromeDriverManager().install())
    # Создаем объект обращения к браузеру
    return webdriver.Chrome(service=service)


def check_capcha():
    """
    Прохождение capcha
    """
    if 'https://www.kinopoisk.ru/showcaptcha' in driver.current_url:
        try:
            checkbox = driver.find_element('class name', 'CheckboxCaptcha-Button')
            checkbox.click()
        except Exception as e:
            print(f'Ошибка: {e}')
    time.sleep(2)


def get_information_about_the_movie(url: str):
    driver.get(url)
    check_capcha()
    countries_genres = driver.find_elements('xpath', "//div[@data-tid='d5ff4cc']")
    platform = driver.find_elements('xpath', "//div[@data-tid='7cda04a5']")
    if platform[1].text[:9] in ['Платформа', 'Аудиодоро']:
        countries = countries_genres[1].text.replace(',', '').split()
        genres = countries_genres[2].text.replace(',', '').split()
    else:
        countries = countries_genres[0].text.replace(',', '').split()
        genres = countries_genres[1].text.replace(',', '').split()
    description = driver.find_element('xpath', "//p[@data-tid='bbb11238']").text
    rating = driver.find_element('xpath', "//span[@data-tid='939058a8']").text
    title_and_year = driver.find_element('xpath',"//h1[@data-tid='f22e0093']").text
    list_title_and_year = title_and_year.split('(')
    if 'series' in url:
        url = url.replace('series', 'film')
        title = list_title_and_year[0].title().strip() + " (Сериал)"
    else:
        title = list_title_and_year[0].title().strip()
    year = list_title_and_year[1].lstrip("сериал ")[:4]

    driver.get(url + 'posters')
    check_capcha()

    div_elements = driver.find_elements(
        'xpath',
        "//div[@data-tid='b22ff31f']")

    div_element = div_elements[0]
    img_element = div_element.find_element('tag name', 'a')
    img = img_element.get_attribute('href')

    return {'title': title,
            'year': year,
            'countries': countries,
            'genres': genres,
            'description': description,
            'rating': rating,
            'img': img
            }


driver = create_driver()
