class Lesson(object): #класс для хранения записи о паре
    name = ""
    room = ""
    number = ""

    def __init__(self, name, room, number):
        self.name = name
        self.room = room
        self.number = number