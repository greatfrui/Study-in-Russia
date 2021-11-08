import requests
import fake_useragent
import csv
from bs4 import BeautifulSoup
import os
try:
    os.mkdir("date")#создаем папку в которой буду храниться файлы с которыми мы будем работать
except:
    pass

headers = {
    'user-agent' : fake_useragent.UserAgent().random
}
page = 1
#важная часть кода,при добавлении дополнительных страниц на сайт следуют увеличить число в скобках
for q in range (182):
    headers = {
        'user-agent' : fake_useragent.UserAgent().random
    }
    link = f"https://studyinrussia.ru/study-in-russia/programs/type-is-main/apply/?PAGEN_1={page}"
    responce = requests.get(link,headers = headers).text
    #скачиваем все страницы в папку
    with open(f'date/study{page}.html', 'w', encoding='utf-8') as file:
        file.write(responce)
    print(f'страница {page} успешно записана')
    page += 1



#Создаю excel таблицу с необходимыми столбцами
speciality = "Специальность"#1
university = 'Ввуз'#2
city = 'Город'#3
direction = 'Направление'#4
level = 'Уровень'#5
language = 'Язык обучения'#6
duration = 'Продолжительность'#7
education = 'Форма обучения'#8
free_educat = 'Возможность бесплатного обучения'#9
cost = 'Стоимость обучения'#10
city_educat = 'Где проходит обучение'#11
link_information = 'Ссылка на общую информацию'#12
name_univer = 'Полное название университета'#13
link_descrip = 'Ссылка на описание программы'#14
link_speciality = 'Ссылка на специализацию'#15
subject = 'Предмет'#16
code = 'Код'#17
degree = 'Документ об образовании, степень или квалификация'#18
page_programm_univer = 'Страница программы на сайте вуза'#19
curator = 'Куратор программы'#20
number = 'Телефон'#21
e_mail = 'E-mail'#22
link_logo = 'Ссылка на лого вуза'#23
adress_univer = 'Адрес вуза'#24
link_page_univer = 'Ссылка на сайт университета'#25
text_descrip = 'Текст из поля описания программы'#26
text_speciality = 'Текст из поля специализации '#27
with open('table.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter = ";")
    writer.writerow(
        (
            speciality,
            university,
            city,
            direction,
            level,
            language,
            duration,
            free_educat,
            cost,
            city_educat,
            link_information,
            name_univer,
            link_descrip,
            link_speciality,
            subject,
            code,
            degree,
            page_programm_univer,
            curator,
            number,
            e_mail,
            link_logo,
            adress_univer,
            link_page_univer,
            text_descrip,
            text_speciality
        )
    )
#если нужно парсить с какой-то опредленной страницы меняем значение page на начальную страницу
page = 1
#важная часть программы-основной цикл,при добавлении дополнительных страниц на сайт следуют увеличить число в скобках
for i in range(182):

    headers = {
        'user-agent': fake_useragent.UserAgent().random
    }
    #открываем файл нужной страницы
    with open(f'date/study{page}.html', encoding='utf-8') as file:
        src2 = file.read()

    # считываю нужные фрагменты и заношу их в список для обработки
    soup2 = BeautifulSoup(src2, 'lxml')
    # заносим все карточки страницы в один массив
    content_page = soup2.find_all(class_="program-item")
    # рассматриваем все карточки страницы
    helper=0
    for item in content_page:
        # собираем данные с верхней части карточки
        top_part = item.find('div', class_='top')
        speciality = top_part.find('h3', class_="h3-basic").text  # 1 столбец
        university_inf = top_part.find('div', class_='university').find_all('a')
        university = university_inf[0].text  # 2 столбец
        city = university_inf[1].text  # 3 столбец
        #рассматриваем колонки по бокам карты программы
        column_part = item.find('div', class_='columns columns-2').find_all('div', class_='column')
        # проверка левого столбца на остутствие и наличие нужных элементов

        direction = 'Направление'  # 4
        level = 'Уровень'  # 5
        language = 'Язык обучения'  # 6
        duration = 'Продолжительность'  # 7
        slovar_left = {
            'Направление': 0,
            'Уровень': 0,
            'Язык обучения': 0,
            'Продолжительность': 0
        }
        list_left = ['Направление', 'Уровень', 'Язык обучения', 'Продолжительность']

        left = column_part[0].find_all('strong')
        for i in left:
            slovar_left[i.text] += 1
        for j in list_left:
            if slovar_left[j] == 0:
                if j == 'Направление':
                    direction = ''
                if j == 'Уровень':
                    level = ''
                if j == 'Язык обучения':
                    language = ''
                if j == 'Продолжительность':
                    duration = ''
        stroka_left = str(column_part[0].text)
        razbiv_left = stroka_left.split(':')
        list = []
        for y in razbiv_left:
            final_razbiv = y.split('\n')
            list.append(final_razbiv[0])
        try:
            if direction == '':
                if level == '':

                    language = list[1]
                    duration = list[2]
                elif language == '':
                    level = list[1]
                    duration = list[2]

                elif duration == '':
                    level = list[1]
                    language = list[2]
                else:
                    level = list[1]
                    language = list[2]
                    duration = list[3]
            elif level == '':
                if language == '':
                    direction = list[1]
                    duration = list[2]
                elif duration == '':
                    direction = list[1]
                    level = list[2]
                else:
                    direction = list[1]
                    level = list[2]
                    duration = list[3]
            elif language == '':
                if duration == '':
                    direction = list[1]
                    level = list[2]
                else:
                    direction = list[1]
                    level = list[2]
                    duration = list[3]
            elif duration == '':
                direction = list[1]
                level = list[2]
                language = list[3]
            else:
                direction = list[1]
                level = list[2]
                language = list[3]
                duration = list[4]
            list = []
        except:
            direction=''
            duration=''
            language=''
            pass

        # проверка правого столбца на остутствие и наличие нужных элементов
        education = 'Форма обучения'  # 8
        free_educat = 'Возможность бесплатного обучения'  # 9
        cost = 'Стоимость обучения'  # 10
        city_educat = 'Где проходит обучение'  # 11
        slovar_right = {

            'Форма обучения': 0,
            'Возможность бесплатного обучения': 0,
            'Стоимость обучения': 0,
            'Где проходит обучение': 0
        }
        list_right = ['Форма обучения', 'Возможность бесплатного обучения', 'Стоимость обучения', 'Где проходит обучение']
        right = column_part[1].find_all('strong')
        for i in right:
            slovar_right[i.text] += 1
        for j in list_right:
            if slovar_right[j] == 0:
                if j == 'Форма обучения':
                    education = ''
                if j == 'Возможность бесплатного обучения':
                    free_educat = ''
                if j == 'Стоимость обучения':
                    cost = ''
                if j == 'Где проходит обучение':
                    city_educat = ''
        stroka_right = str(column_part[1].text)
        razbiv_right = stroka_right.split(':')
        list = []
        for y in razbiv_right:
            final_razbiv = y.split('\n')
            list.append(final_razbiv[0])
        if education == '':
            if free_educat == '':
                cost = list[1]
            elif cost == '':
                free_educat = list[1]
            else:
                level = list[1]
                language = list[2]
                duration = list[3]
        elif free_educat == '':
            if cost == '':
                education = list[1]
            else:
                education = list[1]
                cost = list[2]
        elif cost == '':
            education = list[1]
            free_educat = list[2]
        else:
            education = list[1]
            free_educat = list[2]
            cost = list[3]
        try:
            city_educat = column_part[1].find('a').text  # 11
        except:
            city_educat=''
            pass
        list = []
        #12-15
        half_link = item.find('div', class_='actions')
        half_link_inf = half_link.find('a').get('href')
        link_information = f'https://studyinrussia.ru{half_link_inf}'  # 12
        responce = requests.get(link_information, headers=headers).text
        with open(f'date/{helper}_link.html', 'w', encoding='utf-8') as file:
            file.write(responce)
        # считываем страницы карточек
        with open(f'date/{helper}_link.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        # находим полное название вуза
        main_block = soup.find('main')
        try:
            name_univer = main_block.find('a', class_='university-link').text  # 13
        except:
            name_univer=''
            pass

        # ищем ссылки
        ul_link = main_block.find('ul', class_='tags-nav tags-nav_green')
        link_list = ul_link.find_all('a')

        # проверка ссылок
        slovar_link = {
            "Общая информация": 0,
            "Описание программы": 0,
            "Специализация": 0
        }
        name_link_list = []

        for link_il in link_list:
            half_link_il = link_il.get('href')
            name_link_list.append(f'https://studyinrussia.ru{half_link_il}')
            slovar_link[link_il.text] += 1
        if slovar_link["Описание программы"] == 1 and slovar_link["Специализация"] == 1:
            link_descrip = name_link_list[1]
            link_speciality = name_link_list[2]
        elif slovar_link["Описание программы"] == 0 and slovar_link["Специализация"] == 1:
            link_descrip = ''
            link_speciality = name_link_list[1]
        elif slovar_link["Специализация"] == 0 and slovar_link["Описание программы"] == 1:
            link_speciality = ''
            link_descrip = name_link_list[1]
        elif slovar_link["Специализация"] == 0 and slovar_link["Описание программы"] == 0:
            link_speciality = ''
            link_descrip = ''
        #16-19
        with open(f'date/{helper}_link.html', encoding='utf-8') as file:
            src = file.read()
        # получаем код предмет и степень
        soup = BeautifulSoup(src, 'lxml')
        block_section = soup.find('section', class_='main-content')
        all_p = block_section.find_all('p')
        p_16 = all_p[0].text
        total_list_inf = p_16.split(':')
        date = []
        for i in total_list_inf:
            b = i.split('\n')
            date.append(b[0])
        try:
            subject = date[-3]  # 16
            code = date[-2]  # 17
            degree = date[-1]# 18
        except:
            subject = ''  # 16
            code = ''  # 17
            degree = ''  # 18

        # старница программы на сайте ввуза
        try:
            page_programm_univer = all_p[-1].find('a').get('href')
        except:
            page_programm_univer=''
            pass

        #20-22
        with open(f'date/{helper}_link.html', encoding='utf-8') as file:
            src = file.read()
        # получаем mail.curatora,number
        soup = BeautifulSoup(src, 'lxml')
        block_section = soup.find('section', class_='main-content')
        #пробуем получить почту
        try:
            inviz_content = block_section.find('div', class_="info-text")
            try:
                e_mail = inviz_content.find('a').text  # 22
            except:
                e_mail = ''
                pass
            try:
                number_cur = inviz_content.text
                number_cur_list = number_cur.split(':')
                a = []
                for i in number_cur_list:
                    b = i.split('\n')
                    a.append(b[0])
                # проверка наличия куратора и номера
                number_cur_strong = inviz_content.find_all('strong')
                slovar_proverka = {
                    'Куратор программы': 0,
                    'Телефон': 0,
                    'E-mail': 0,
                }
                for i in number_cur_strong:
                    slovar_proverka[i.text] += 1
                if slovar_proverka['Куратор программы'] == 1 and slovar_proverka['Телефон'] == 1:
                    curator = a[1]
                    number = a[2]
                    if len(a) == 5:
                        number = a[3]
                elif slovar_proverka['Куратор программы'] == 1 and slovar_proverka['Телефон'] == 0:
                    curator = a[1]
                    number = ''
                elif slovar_proverka['Куратор программы'] == 0 and slovar_proverka['Телефон'] == 1:
                    curator = ''
                    number = a[2]
                elif slovar_proverka['Куратор программы'] == 0 and slovar_proverka['Телефон'] == 0:
                    curator = ''
                    number = ''
            except:
                number = ''
                curator = ''
        except:
            pass
        #23-25
        with open(f'date/{helper}_link.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        aside_block = soup.find('aside', class_="sidebar sidebar_right")#забираем сайд бар страницы
        block_link_logo = aside_block.find('div', class_='logo')
        half_link_logo = block_link_logo.find('img').get('src')
        link_logo = f'https://studyinrussia.ru/{half_link_logo}'  # 23 находим ссылку на лого
        adress_univer = aside_block.find('span', itemprop="streetAddress").text  # 24
        stroka_adress_univer = str(adress_univer).replace('&nbsp', '')# 24 считываем адрес
        link_page_univer = aside_block.find('a', itemprop="url").get('href')  # 25 забираем ссылку сайта ввуза
        #26 и 27
        if link_descrip != '':#проверяем есть ли ссылка на страницу с дданным текстом если есть то берем текст если нет оставляем пустую ячейку
            responce = requests.get(link_descrip, headers=headers).text
            soup = BeautifulSoup(responce, 'lxml')
            try:
                block_section = soup.find('section', class_='main-content')
                all_div = block_section.find_all('div')
                text_descrip = all_div[1].text
            except:
                text_descrip=''
                pass
        else:
            text_descrip=''
        if link_speciality != '':#проверяем есть ли ссылка на страницу с дданным текстом если есть то берем текст если нет оставляем пустую ячейку
            responce = requests.get(link_speciality, headers=headers).text
            soup = BeautifulSoup(responce, 'lxml')
            block_section = soup.find('section', class_='main-content')
            all_div = block_section.find('ul')
            text_speciality = all_div.text.strip()
        else:
            text_speciality=''
        helper += 1

        with open('table.csv', 'a', encoding='utf-8-sig',newline='') as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(
                (
                    speciality,
                    university,
                    city,
                    direction,
                    level,
                    language,
                    duration,
                    free_educat,
                    cost,
                    city_educat,
                    link_information,
                    name_univer,
                    link_descrip,
                    link_speciality,
                    subject,
                    code,
                    degree,
                    page_programm_univer,
                    curator,
                    number,
                    e_mail,
                    link_logo,
                    adress_univer,
                    link_page_univer,
                    text_descrip,
                    text_speciality
                )
            )
    print(f'данные с {page} страницы успешно записаны в таблицу')
    page += 1