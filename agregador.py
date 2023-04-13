import tkinter as tk
from tkinter import ttk
import requests
import webbrowser
import tkinter.font as font

# Define a classe, herdando do tkinter
class NewsAggregatorGUI(tk.Tk):
    API_KEY = 'b91d4545ff414645a1a35a5655e335af'
    URL = 'https://newsapi.org/v2/top-headlines?'

    # Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("News Aggregator")
        self.geometry("800x600")

        # Variáveis para inputs de categoria e consulta
        self.category_var = tk.StringVar()
        self.query_var = tk.StringVar()

        self.create_widgets()

    # Método para colocar os widgets na GUI
    def create_widgets(self):
        label_category = ttk.Label(self, text="Category:")
        label_category.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        entry_category = ttk.Entry(self, textvariable=self.category_var)
        entry_category.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        button_category = ttk.Button(self, text="Get Articles", command=self.get_articles_by_gui_category)
        button_category.grid(column=2, row=0, padx=10, pady=10)

        label_query = ttk.Label(self, text="Query:")
        label_query.grid(column=0, row=1, padx=10, pady=10, sticky="w")

        entry_query = ttk.Entry(self, textvariable=self.query_var)
        entry_query.grid(column=1, row=1, padx=10, pady=10, sticky="w")

        button_query = ttk.Button(self, text="Get Articles", command=self.get_articles_by_gui_query)
        button_query.grid(column=2, row=1, padx=10, pady=10)

        self.text = tk.Text(self, width=100, height=25, wrap=tk.WORD)
        self.text.grid(column=0, row=2, padx=10, pady=10, columnspan=3)

    # Método para pegar artigos por categoria e exibi-los
    def get_articles_by_gui_category(self):
        category = self.category_var.get()
        articles = self.get_articles_by_category(category)
        self.show_articles(articles)

    # " por query
    def get_articles_by_gui_query(self):
        query = self.query_var.get()
        articles = self.get_articles_by_query(query)
        self.show_articles(articles)

    # Método para mostrar artigos em texto
    def show_articles(self, articles):
        self.text.delete('1.0', tk.END)

        title_font = font.Font(weight='bold')

        # Faz um loop pelos artigos
        for article in articles:
            title = article["title"]
            url = article["url"]
            self.text.insert(tk.END, title + '\n', ('title',))
            self.text.insert(tk.END, url + '\n\n')
            self.text.tag_configure('title', font=title_font)
            self.text.tag_bind('title', '<Button-1>', lambda e, url=url: webbrowser.open_new(url))

    # Método para usar a API para encontrar os artigos por categorai
    def get_articles_by_category(self, category):
        query_parameters = {
            "category": category,
            "sortBy": "top",
            "country": "us",
            "apiKey": self.API_KEY
        }
        return self._get_articles(query_parameters)

    # " por query
    def get_articles_by_query(self, query):
        query_parameters = {
            "q": query,
            "sortBy": "top",
            "country": "gb",
            "apiKey": self.API_KEY
        }
        return self._get_articles(query_parameters)

    def _get_articles(self, params):
        response = requests.get(self.URL, params=params)

        articles = response.json()['articles']

        results = []

        for article in articles:
            results.append({"title": article["title"], "url": article["url"]})

        return results

    def get_sources_by_category(self, category):
        url = 'https://newsapi.org/v2/top-headlines/sources'
        query_parameters = {
            "category": category,
            "language": "en",
                        "apiKey": self.API_KEY
        }

        response = requests.get(url, params=query_parameters)

        sources = response.json()['sources']

        for source in sources:
            print(source['name'])
            print(source['url'])

# Instancia o aplicativo e executa
if __name__ == "__main__":
    app = NewsAggregatorGUI()
    app.mainloop()
