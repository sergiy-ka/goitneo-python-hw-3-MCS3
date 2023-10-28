# Homework-3 >>> CLI-bot
import address_book as ab
import user_exceptions as ue


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Wrong format! Correct format in the help."
        except KeyError:
            return "Name not found."
        except IndexError:
            pass
        except ue.NameNotFoundError:
            return "Name not found in the Address book."
        except ue.BirthdayNotFoundError:
            return "Birthday not found."
        except ue.PhoneNotFoundError:
            return "Phone not found."
        except ue.NameExistsError:
            return "Name already exists."
        except ue.PhoneExistsError:
            return "Phone already exists."
        except ue.EmptyAddressBookError:
            return "Address book is empty."
        except ue.PhoneFormatError:
            return "Phone number must be 10 digits."
        except ue.BirthdayFormatError:
            return "Date of birth must exist and be in the format DD.MM.YYYY"
        except ue.BirthdayInFutureError:
            return "Birthday can't be in the future."
        except Exception:
            return "Something went wrong, but we are already working on fixing it."
    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    if book.find(name) is None:
        record = ab.Record(name)
        record.add_phone(phone)
        book.add_record(record)
    else:
        for p in book[name].phones:
            if p.value == phone:
                raise ue.PhoneExistsError
        book[name].add_phone(phone)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    if book.find(name) is None:
        raise ue.NameNotFoundError
    elif book[name].find_phone(old_phone) is None:
        raise ue.PhoneNotFoundError
    else:
        book[name].edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def show_phone(args, book):
    name, = args
    if book.find(name) is None:
        raise ue.NameNotFoundError
    return book.find(name)


@input_error
def show_all(book):
    contact_list = []
    if len(book) == 0:
        raise ue.EmptyAddressBookError
    else:
        for name, record in book.items():
            contact_list.append(str(record))
    return ("\n").join(contact_list)


@input_error
def add_birthday(args, book):
    name, birthday = args
    if book.find(name) is None:
        record = ab.Record(name)
        record.add_birthday(birthday)
        book.add_record(record)
    else:
        book[name].add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name, = args
    if book.find(name) is None:
        raise ue.NameNotFoundError
    elif book.find(name).birthday is None:
        raise ue.BirthdayNotFoundError
    else:
        birthday = book.find(name).birthday.value
    return birthday


@input_error
def show_birthdays_per_week(book):
    if len(book) == 0:
        raise ue.EmptyAddressBookError
    return book.get_birthdays_per_week()


@input_error
def remove_contact(args, book):
    name, phone = args
    if len(book) == 0:
        raise ue.EmptyAddressBookError
    elif book.find(name) is None:
        raise ue.NameNotFoundError
    elif book[name].find_phone(phone) is None:
        raise ue.PhoneNotFoundError
    else:
        book[name].remove_phone(phone)
    return "Contact removed."


@input_error
def delete_contact(args, book):
    name, = args
    if len(book) == 0:
        raise ue.EmptyAddressBookError
    elif book.find(name) is None:
        raise ue.NameNotFoundError
    else:
        book.delete(name)
    return "Contact deleted."


def show_all_commands():
    commands = {"hello": "hello",
                "add": "add [name] [phone]",
                "change": "change [name] [old_phone] [new_phone]",
                "phone": "phone [name]",
                "all": "all",
                "add-birthday": "add-birthday [name] [birthday]",
                "show-birthday": "show-birthday [name]",
                "birthdays": "birthdays",
                "remove": "remove [name] [phone]",
                "delete": "delete [name]",
                "help": "help",
                "exit": "exit"}
    command_list = []
    h_line_0 = "{:^15}{:^3}{:^25}".format("Command", "|", "Format")
    h_line_1 = "{:^15}{:^3}{:^25}".format("-" * 15, "|", "-" * 25)
    command_list.append(h_line_0)
    command_list.append(h_line_1)
    for cmd, format in commands.items():
        b_line = "{:<15}{:^3}{:<25}".format(cmd, "|", format)
        command_list.append(b_line)
    return ("\n").join(command_list)


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = ab.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in ["hello", "hi"]:
            print("How can I help you?")
        elif command == 'help':
            print(show_all_commands())
        elif command == "add":
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(show_birthdays_per_week(book))
        elif command == 'remove':
            print(remove_contact(args, book))
        elif command == 'delete':
            print(delete_contact(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
