class Book:
    def __init__(self, title, author, count_pages, path):
        self.title = title
        self.author = author
        self.count_pages = count_pages
        self.path = path

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_count_pages(self):
        return self.count_pages

    def get_path(self):
        return self.path

    # строка со всей информацией о книге
    def get_info(self):
        return f"Название: {self.title}\nАвтор: {self.author}\nКол-во страниц: {self.count_pages}\nОбложка:"
