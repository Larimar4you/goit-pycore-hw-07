from collections import UserDict
from datetime import datetime, timedelta


# ==== Класи полів =====
class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


# ===== Клас Record =====
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None  # не обов'язкове поле

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Old phone not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        bday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"
        return f"{self.name.value}: {phones} | Birthday: {bday}"


# ==== Клас AddressBook =====
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        result = {}

        for record in self.data.values():
            if not record.birthday:
                continue
            bday_this_year = record.birthday.value.replace(year=today.year)
            if today <= bday_this_year <= next_week:
                weekday = bday_this_year.strftime("%A")
                result.setdefault(weekday, []).append(record.name.value)

        return result
