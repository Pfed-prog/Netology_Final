
# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests
 
# Пакет для удобной работы с данными в формате json
import json
 
# Модуль для работы со значением времени
import time
 
import pandas as pd
import numpy as np
from tqdm import tqdm

class hh():
    def __init__(self):
        self.jsObj = []

    def getPage(self, text, page = 0):
        """
        Создаем метод для получения страницы со списком вакансий.
        Аргументы:
            text - Текст фильтра
            area - Индекс страны или города. Например, 113-rus
            page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
            per_page - Кол-во вакансий на 1 странице
        """
        
        # Справочник для параметров GET-запроса
        params = {
            'text': f'NAME:{text}',
            'area': 113,
            'page': page,
            'per_page': 100 
        }
        
        
        req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
        self.data = req.content.decode() # Декодируем ответ
        req.close()
 
    
    # Считываем первые number*100 вакансий
    def generate_pages(self, number=1):
        
        for page in tqdm(range(0, number)):
            # Преобразуем текст ответа запроса в справочник Python
            js = json.loads(self.data)
            self.jsObj.append(js)
            # Проверка на последнюю страницу, если вакансий меньше чем задано
            if (js['pages'] - page) <= 1:
                break
            
            # Необязательная задержка, чтобы не нагружать сервисы hh
            time.sleep(0.25)
            
        print('Страницы поиска собраны')


    def generate_vacancies(self, name ):
        # Создаем списки для столбцов таблицы vacancies
        IDs = [] # Список идентификаторов вакансий
        names = [] # Список наименований вакансий
        snippet = [] # Список описаний вакансий
        salary = [] # Список зарплат
        skills_name=[]
        # Заполняем списки для таблиц
        for i in range(len(self.jsObj)):
            for j in tqdm(range(len(self.jsObj[i]['items']))):

                IDs.append(self.jsObj[i]['items'][j]['id'])
                names.append(self.jsObj[i]['items'][j]['name'])
                snippet.append(self.jsObj[i]['items'][j]['snippet']['requirement'])

                skills=str()
                # Обращаемся к API и получаем детальную информацию по конкретной вакансии
                req=requests.get(self.jsObj[i]['items'][j]['url'])
                data = req.content.decode()
                req.close()
                jsVac = json.loads(data)
                
                for skl in jsVac['key_skills']:
                    skills = skills + skl['name']+','
                skills_name.append(skills[:-1])
                
                try:
                    salary.append(self.jsObj[i]['items'][j]['salary']['from'])
                except:
                    salary.append(np.nan)
                time.sleep(0.25)
        pd.DataFrame({'ids':IDs,'names':names,'skills':skills_name,'salary':salary},index=IDs).to_csv(f'{name}.csv', index=False)

b = hh()
b.getPage('c++')
b.generate_pages()
b.generate_vacancies('c++')
