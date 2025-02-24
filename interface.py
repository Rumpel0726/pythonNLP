# Импорт необходимых библиотек
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from parse import ParseObj  # Парсер новостей
from ai_test.toxic import NLPObj  # NLP модель для анализа текста
from transformers import pipeline

# Импорт библиотек для тематического моделирования
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Импорт библиотек для кластеризации
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class MainWindow(QMainWindow):
    """
    Главное окно приложения для анализа новостей
    """
    def __init__(self):
        super().__init__()
        # Настройка основного окна
        self.setWindowTitle("AI Чат-интерфейс")
        self.setGeometry(100, 100, 800, 600)
        self.keywords_list = [[]]
        self.topic_list = []
        
        # Инициализация NLP модели
        self.nlpobj = NLPObj()
        
        # Инициализация парсера
        self.parseobj = ParseObj()
        #self.parseobj.parse_main('https://www.yarnews.net/news/bymonth/2014/12/0/')

        # Создание и настройка интерфейса
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создание области для отображения новостей
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        layout.addWidget(self.content_area)
        
        # Настройка стилей для области контента
        self.content_area.setStyleSheet("""
            QTextEdit {
                font-size: 14pt;
                padding: 10px;
                background-color: #ffffff;
                border: 1px solid #cccccc;
            }
        """)

        self.ner_pipeline = pipeline("ner", 
                                   model="surdan/LaBSE_ner_nerel", 
                                   aggregation_strategy="simple")

        # Создание поля для анализа
        self.analysis_field = QTextEdit()
        self.analysis_field.setMaximumHeight(100)
        layout.addWidget(self.analysis_field)

        # Создание кнопок управления
        self.next_button = QPushButton("Вперед")
        self.next_button.clicked.connect(self.next_message)
        layout.addWidget(self.next_button)

        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.prev_message)
        layout.addWidget(self.prev_button)

        self.clusterize_button = QPushButton("Кластеризация")
        self.clusterize_button.clicked.connect(self.clusterize)
        layout.addWidget(self.clusterize_button)

        self.frequenncy_button = QPushButton("Частотность")
        self.frequenncy_button.clicked.connect(self.analyze_entities_frequency)
        layout.addWidget(self.frequenncy_button)


    def next_message(self):
        """
        Обработчик для отображения следующей новости и её анализа
        """
        self.content_area.clear()
        cur_new = str(self.parseobj.db.get_next_line()[3])

        self.content_area.append(cur_new)
        self.analysis_field.clear()

        entities = self.ner_pipeline(cur_new)
        entities = self.process_entities(entities)

        # Выводим результаты
        for entity in entities:
            self.analysis_field.append(f"Entity: {entity['word']}, Label: {entity['label']}\n")

    def prev_message(self):
        """
        Обработчик для отображения предыдущей новости и её анализа
        """
        self.content_area.clear()
        self.content_area.append(str(self.parseobj.db.get_prev_line()[3]))
        self.analysis_field.clear()
        self.analysis_field.append(str(self.nlpobj.get_ent(self.content_area.toPlainText())))
        
    def clusterize(self):
        """
        Метод для кластеризации новостей с использованием BERTopic
        """
        # Очистка области контента
        self.content_area.clear()
        
        # Получение всех новостей из базы данных
        documents = [self.parseobj.db.records[i][3] for i in range(len(self.parseobj.db.records))]
        
        # Фильтрация коротких новостей (менее 10 слов)
        documents = [doc for doc in documents if len(doc.split()) > 10]

        # Инициализация модели для создания эмбеддингов
        sentence_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

        # Настройка и создание модели BERTopic
        topic_model = BERTopic(
            embedding_model=sentence_model,
            nr_topics=10,  # Количество тем для кластеризации
            language="russian",
            min_topic_size=5,  # Минимальный размер темы
            verbose=True
        )

        # Применение модели к документам
        topics, _ = topic_model.fit_transform(documents)

        # Вывод результатов кластеризации
        for i, topic in enumerate(topics):
            print(f"Новость {i} относится к теме {topic}")

        # Получение и вывод информации о темах
        topic_info = topic_model.get_topic_info()
        print(topic_info)

        # Создание визуализаций
        fig = topic_model.visualize_barchart()
        fig.write_html("barchart.html")

        fig = topic_model.visualize_hierarchy()
        fig.write_html("hierarchy.html")

        fig = topic_model.visualize_heatmap()
        fig.write_html("heatmap.html")

        # Детальный анализ каждой темы
        print("visualize_keywords()")
        print()
        for topic_id in topic_info["Topic"]:
            if topic_id != -1:  # Пропуск выбросов
                keywords = topic_info[topic_info["Topic"] == topic_id]["Representation"].values[0]
                self.keywords_list.append(keywords)
                self.topic_list.append(topic_id)
                print(f"Тема {topic_id}:")
                print(f"Ключевые слова: {', '.join(keywords[:5])}")
                print(f"Пример документа: {topic_model.get_representative_docs(topic_id)[0]}")
                print()
                        
        

    def process_entities(self, ner_results):
        processed_entities = []
        current_word = ""
        current_label = None
        current_score = 0.0
        
        for entity in ner_results:
            word = entity['word']
            label = entity['entity_group']
            score = entity['score']
            
            # Если слово начинается с ##, это продолжение предыдущего токена
            if word.startswith('##'):
                current_word += word[2:]
                current_score = max(current_score, score)  # берем максимальную оценку
            else:
                # Если есть накопленное слово, добавляем его в результат
                if current_word and current_label:
                    processed_entities.append({
                        'word': current_word,
                        'label': current_label,
                        'score': current_score
                    })
                current_word = word
                current_label = label
                current_score = score
        
        # Добавляем последнее слово
        if current_word and current_label:
            processed_entities.append({
                'word': current_word,
                'label': current_label,
                'score': current_score
            })
            
        return processed_entities

    def get_entities(self, text):
        results = self.ner_pipeline(text)
        return self.process_entities(results)

    def analyze_entities_frequency(self):
        """
        Анализ частотности появления именованных сущностей с фильтрацией
        """
        # Список стоп-слов для фильтрации
        stop_entities = {
            'Ярославль', 'Ярославля', 'Ярославле', 'Ярньюс',
            'Ярославской области', 'Ярославской'
        }
        
        # Словарь для хранения частот по категориям
        entity_by_type = {}
        
        for record in self.parseobj.db.records:
            text = record[3]
            entities = self.get_entities(text)
            
            for entity in entities:
                word, label = entity['word'], entity['label']
                
                # Пропускаем стоп-сущности
                if word in stop_entities:
                    continue
                    
                # Пропускаем короткие слова и цифры
                if len(word) <= 1 or word.isdigit():
                    continue
                
                # Создаем словарь для типа сущности, если его еще нет
                if label not in entity_by_type:
                    entity_by_type[label] = {}
                
                # Увеличиваем счетчик для сущности
                entity_by_type[label][word] = entity_by_type[label].get(word, 0) + 1
        
        # Вывод результатов
        self.content_area.clear()
        self.content_area.append("Анализ именованных сущностей по категориям:\n")
        
        for label, entities in entity_by_type.items():
            # Сортируем сущности внутри каждой категории по частоте
            sorted_entities = sorted(entities.items(), key=lambda x: x[1], reverse=True)
            
            # Выводим топ-5 сущностей для каждой категории
            if sorted_entities:
                self.content_area.append(f"\n{label}:")
                for word, freq in sorted_entities[:5]:
                    self.content_area.append(f"  {word}: {freq} раз")

        

        
        





