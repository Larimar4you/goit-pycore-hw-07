from Task1 import AddressBook, Record


# Декоратор для обробки помилок ========


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Missing arguments."
        except KeyError:
            return "Error: Contact not found."

    return inner


# Функції-обробники =======


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.change_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return ", ".join(p.value for p in record.phones)
    return "Contact not found."


@input_error
def show_all(args, book):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(rec) for rec in book.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    elif record:
        return "No birthday set for this contact."
    return "Contact not found."


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{day}: {', '.join(names)}" for day, names in upcoming.items())


# Парсер команд =========
def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0].lower(), parts[1:]


# Основна функція main() =======
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
