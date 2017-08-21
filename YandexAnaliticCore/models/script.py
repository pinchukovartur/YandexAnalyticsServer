# модель скрипт, которыми оперирует контролер
class Script:
    def __init__(self, name, type, username, text):
        self.name = name
        self.type = type
        self.username = username
        self.text = text
