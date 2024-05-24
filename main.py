import json
import readline
from tabulate import tabulate
from datetime import datetime, timedelta


def add_contact():
    print("Feature coming soon")


def add_phone_to_contact():
    print("Feature coming soon")


def change_contact():
    print("Feature coming soon")


def search_by_phone():
    print("Feature coming soon")


def all_contact():
    print("Feature coming soon")


def delete_contact():
    print("Feature coming soon")



class User:
    def __init__(self, id, name, birthday=None):
        self.id = id
        self.name = name
        self.birthday = birthday  # День народження користувача у форматі DD-MM-YYYY


class UsersDatabase:
    def __init__(self):
        self.users = []
        self.next_id = 1
        self.load_users()  # Завантаження користувачів з файлу при створенні об'єкта

    # Функція для перевірки коректності дати народження
    def validate_date(self, birthday_str):
        try:
            birthday = datetime.strptime(birthday_str, "%d-%m-%Y")
            today = datetime.now().date()
            # Перевірка, чи дата не є у майбутньому
            if birthday.date() > today:
                print("Дата народження не може бути у майбутньому.")
                return False
            # Перевірка, чи дата не більше за 120 років у минулому
            if today - birthday.date() > timedelta(days=365 * 120):
                print("Дата народження не може бути більше за 120 років у минулому.")
                return False
            return True
        except ValueError:
            print(
                "Некоректний формат дати народження. Будь ласка, введіть у форматі 'DD-MM-YYYY'."
            )
            return False

    # Метод для додавання контакту
    def add_birthday(self, user_id, new_birthday):
        while not self.validate_date(new_birthday):
            new_birthday = input(
                "Введіть новий день народження у форматі 'DD-MM-YYYY': "
            )
        for user in self.users:
            if user.id == user_id:
                user.birthday = new_birthday
                self.save_users()
                print("День народження оновлено.")
                return True
        print("Користувача з вказаним ID не знайдено.")
        return False

    def save_users(self):
        with open("users.json", "w") as file:
            json_users = [
                {"id": user.id, "name": user.name, "birthday": user.birthday}
                for user in self.users
            ]
            json.dump(
                json_users, file, indent=4
            )  # Використовуйте indent для форматування JSON

    # Метод для завантаження користувачів з файлу
    def load_users(self):
        try:
            with open("users.json", "r") as file:
                json_users = json.load(file)
                self.users = [
                    User(user["id"], user["name"], user["birthday"])
                    for user in json_users
                ]
                self.next_id = (
                    max(self.users, key=lambda user: user.id).id + 1
                    if self.users
                    else 1
                )
        except FileNotFoundError:
            pass

    # Метод для видалення дня народження користувача
    def delete_birthday(self, user_id):
        for user in self.users:
            if user.id == user_id:
                user.birthday = None  # Встановлюємо день народження користувача як None
                self.save_users()
                print("День народження користувача видалено.")
                return True
        print("Користувача з вказаним ID не знайдено.")
        return False

    # Метод для показу дня народження користувача
    def show_birthday(self, user_id):
        for user in self.users:
            if user.id == user_id:
                if user.birthday:
                    # return str(user)  # Повертаємо користувача у вигляді рядка
                    return user  # Повертаємо об'єкт користувача
                else:
                    return "День народження не встановлено для цього користувача."
        return "Користувача з вказаним ID не знайдено."

    # Метод для показу всіх днів народження
    def show_all_birthdays(self):
        birthdays = []
        for user in self.users:
            if user.birthday:
                birthdays.append(
                    f"ID: {user.id}, Name: {user.name}, Birthday: {user.birthday}"
                )
            else:
                birthdays.append(
                    f"ID: {user.id}, Name: {user.name}, Birthday: не встановлено"
                )
        return birthdays

    # Метод для пошуку контактів за датою народження в заданому проміжку
    def search_by_date_birthday(self, days):
        today = datetime.now().date()
        target_date = today + timedelta(days=days)
        matching_users = []

        for user in self.users:
            if user.birthday:
                # Перетворіть рядок з датою народження у об'єкт datetime.date
                user_birthday = datetime.strptime(user.birthday, "%d-%m-%Y").date()
                # Змініть рік дати народження на поточний
                user_birthday_this_year = user_birthday.replace(year=today.year)
                # Перевірте, чи дата народження відповідає заданому проміжку
                if today <= user_birthday_this_year <= target_date:
                    matching_users.append(user)

        return matching_users


# Клас для представлення нотатки з ідентифікатором, текстом та тегами
class Note:
    def __init__(self, id, text, tags):
        self.id = id
        self.text = text
        self.tags = tags


# Клас для управління базами даних нотаток
class NotesDatabase:
    def __init__(self):
        self.notes = []
        self.next_id = 1
        self.load_notes()  # Завантаження нотаток з файлу при створенні об'єкта

    # Метод для додавання нотатки
    def add_note(self, text, tags):
        note = Note(self.next_id, text, tags)
        self.notes.append(note)
        self.next_id += 1
        self.save_notes()  # Збереження нотаток після додавання

    # Метод для отримання всіх нотаток
    def get_all_notes(self):
        return self.notes

    # Метод для пошуку нотаток за тегами
    def search_notes_by_tags(self, tags):
        return [note for note in self.notes if any(tag in note.tags for tag in tags)]

    # Метод для сортування нотаток за тегами
    def sort_notes_by_tags(self, tags):
        sorted_notes = sorted(
            [note for note in self.notes if any(tag in note.tags for tag in tags)],
            key=lambda note: sum(tag in note.tags for tag in tags),
            reverse=True,
        )
        return sorted_notes

    # Метод для видалення нотатки за ідентифікатором
    def delete_note(self, id):
        self.notes = [note for note in self.notes if note.id != id]
        self.save_notes()  # Збереження нотаток після видалення
        return True

    # Метод для оновлення нотатки
    def update_note(self, id, text, tags):
        for note in self.notes:
            if note.id == id:
                note.text = text
                note.tags = tags
                self.save_notes()  # Збереження нотаток після оновлення
                return True
        return False

    # Метод для збереження нотаток у файл
    def save_notes(self):
        with open("notes.json", "w") as file:
            json_notes = [
                {"id": note.id, "text": note.text, "tags": note.tags}
                for note in self.notes
            ]
            json.dump(json_notes, file)

    # Метод для завантаження нотаток з файлу
    def load_notes(self):
        try:
            with open("notes.json", "r") as file:
                json_notes = json.load(file)
                self.notes = [
                    Note(note["id"], note["text"], note["tags"]) for note in json_notes
                ]
                self.next_id = (
                    max(self.notes, key=lambda note: note.id).id + 1
                    if self.notes
                    else 1
                )
        except FileNotFoundError:
            pass


# Словник команд та їх описи
commands = {
    "add_contact": "Додати контакт",
    "add_phone": "Додати телефон до контакту",
    "change_contact": "Змінити контакт",
    "search_by_phone": "Пошук за номером телефону",
    "all_contact": "Показати всі контакти",
    "delete_contact": "Видалити контакт",
    "add_birthday": "Додати день народження",
    "delete_birthday": "Видалити день народження",  # додати видалити день народження
    "show_birthday": "Показати день народження",
    "show_all_birthdays": "Показати всі дні народження",
    "search_by_date_birthday": "Пошук за датою народження",
    "add_note": "Додати нотатку",
    "all_note": "Показати всі нотатки",
    "search_note": "Пошук нотаток за тегами",
    "sorting_note_by_tags": "Сортування нотаток за тегами",
    "delete_note": "Видалити нотатку",
    "update_note": "Оновити нотатку",
    "hello": "Привіт",
    "exit": "Вийти",
    "close": "Вийти",
}


# Функція для друку нотаток у вигляді таблиці
def print_notes(notes):
    if not notes:
        print("Немає нотаток для виводу.")
    else:
        table = [[note.id, ", ".join(note.tags), note.text] for note in notes]
        print(tabulate(table, headers=["ID", "Tags", "Text"], tablefmt="grid"))


def say_hello():
    print("Hello!")


# Функція для автодоповнення команд
def completer(text, state):
    options = [cmd for cmd in commands.keys() if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


# Функція для отримання введеної команди з автодоповненням
def get_command_input():
    while True:
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")

        choice = input("Введіть команду: ").strip()

        matching_commands = [cmd for cmd in commands.keys() if cmd.startswith(choice)]

        if len(matching_commands) == 1:
            return matching_commands[0]
        elif len(matching_commands) > 1:
            print("Кілька команд відповідають введеній частині. Будь ласка, уточніть:")
            for cmd in matching_commands:
                print(f" - {cmd}")
        else:
            print("Команду не знайдено. Спробуйте ще раз.")


# Функція для друку команд у вигляді таблиці
def print_commands(commands):
    table = [[cmd, description] for cmd, description in commands.items()]
    print(tabulate(table, headers=["Command", "Description"], tablefmt="grid"))


# Головна функція програми
def main():
    db = NotesDatabase()
    users_db = UsersDatabase()

    print("\nAvailable commands:")
    print_commands(commands)

    while True:

        choice = get_command_input()

        # Обробка команд
        if choice == "hello":
            say_hello()

        # Обробка команди "add_contact"
        elif choice == "add_contact":
            add_contact()

        elif choice == "add_phone":
            add_phone_to_contact()

        elif choice == "change_contact":
            change_contact()

        elif choice == "search_by_phone":
            search_by_phone()

        elif choice == "all_contact":
            all_contact()

        elif choice == "delete_contact":
            delete_contact()

        # Обробка команди "update_birthday" з перевіркою
        elif choice == "add_birthday":
            user_id_input = input(
                "Введіть ID користувача, дату народження якого потрібно оновити: "
            )
            try:
                user_id = int(user_id_input)
                new_birthday = input(
                    "Введіть новий день народження у форматі 'DD-MM-YYYY': "
                )
                users_db.add_birthday(user_id, new_birthday)
            except ValueError:
                print("ID користувача повинно бути цілим числом.")

        # Обробка команди "delete_birthday"
        elif choice == "delete_birthday":
            while True:
                user_id_input = input(
                    "Введіть ID користувача, для якого потрібно видалити день народження: "
                )
                try:
                    user_id = int(user_id_input)
                    users_db.delete_birthday(user_id)
                    break  # Вихід з циклу, якщо введення коректне
                except ValueError:
                    print(
                        f"Неправильний ID користувача '{user_id_input}'. Будь ласка, введіть коректне ціле число."
                    )

        # Обробка команди "show_birthday"
        elif choice == "show_birthday":
            user_id_input = input(
                "Введіть ID користувача, для якого потрібно показати день народження: "
            )
            try:
                user_id = int(user_id_input)
                user = users_db.show_birthday(user_id)
                if user:
                    print(
                        f"ID: {user.id}, Name: {user.name}, Birthday: {user.birthday if user.birthday else 'не встановлено'}"
                    )
                else:
                    print("Користувача з вказаним ID не знайдено.")
            except ValueError:
                print(
                    f"Неправильний ID користувача '{user_id_input}'. Будь ласка, введіть коректне ціле число."
                )

        # Обробка команди "show_all_birthdays"
        elif choice == "show_all_birthdays":
            birthdays = users_db.show_all_birthdays()
            for birthday in birthdays:
                print(birthday)

        # Обробка команди "search_by_date_birthday"
        elif choice == "search_by_date_birthday":
            while True:
                days_input = input(
                    "Введіть кількість днів (максимум 365), на яку потрібно розширити проміжок для пошуку: "
                )
                try:
                    days = int(days_input)
                    if days > 365:
                        print(
                            "Кількість днів повинна бути не більше 365. Будь ласка, введіть коректне число."
                        )
                        continue  # Повернутись на початок циклу, щоб запитати введення знову
                    matching_users = users_db.search_by_date_birthday(days)
                    if matching_users:
                        print(
                            f"Контакти, у яких день народження відбувається в проміжку через {days} днів:"
                        )
                        for user in matching_users:
                            print(
                                f"ID: {user.id}, Name: {user.name}, Birthday: {user.birthday}"
                            )
                    else:
                        print(
                            f"Немає контактів, у яких день народження відбувається в проміжку через {days} днів."
                        )
                    break  # Вихід з циклу, якщо введення коректне
                except ValueError:
                    print("Неправильне значення днів. Будь ласка, введіть ціле число.")

        elif choice == "add_note":
            text = input("Enter note text: ")
            tags = input("Enter tags separated by comma: ").split(",")
            db.add_note(text, tags)
            print("Note added.")
            all_notes = (
                db.get_all_notes()
            )  # Оновлюємо all_notes після додавання нотатки
            print_notes(all_notes)

        elif choice == "all_note":
            all_notes = db.get_all_notes()
            print_notes(all_notes)

        elif choice == "search_note":
            search_tags = input("Enter tags to search separated by comma: ").split(",")
            found_notes = db.search_notes_by_tags(search_tags)
            print_notes(found_notes)

        elif choice == "sorting_note_by_tags":
            sort_tags = input("Enter tags to sort by separated by comma: ").split(",")
            sorted_notes = db.sort_notes_by_tags(sort_tags)
            print_notes(sorted_notes)

        elif choice == "delete_note":
            note_id_input = input("Enter note ID to delete: ")
            try:
                note_id = int(note_id_input)
                if db.delete_note(note_id):
                    print("Note deleted.")
                    all_notes = db.get_all_notes()
                    print_notes(all_notes)
                else:
                    print("Note with the given ID not found.")
            except ValueError:
                print(
                    f"Invalid note ID '{note_id_input}'. Please enter a valid integer ID."
                )

        elif choice == "update_note":
            note_id_input = input("Enter note ID to update: ")
            try:
                note_id = int(note_id_input)
                text = input("Enter new text for the note: ")
                tags = input("Enter new tags for the note separated by comma: ").split(
                    ","
                )
                if db.update_note(note_id, text, tags):
                    print("Note updated.")
                    all_notes = db.get_all_notes()
                    print_notes(all_notes)
                else:
                    print("Note with the given ID not found.")
            except ValueError:
                print(
                    f"Invalid note ID '{note_id_input}'. Please enter a valid integer ID."
                )

        elif choice in ("exit", "close"):
            print("Closing the program. Goodbye!")
            break


if __name__ == "__main__":
    main()
