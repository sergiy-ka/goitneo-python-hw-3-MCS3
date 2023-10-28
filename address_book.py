# Homework-3 >>> AddressBook
import user_exceptions as ue
import calendar
from datetime import datetime
from collections import defaultdict, UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        self._value = value
        super().__init__(self.__value)

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value):
        # Номер телефону має складатись з 10 цифр
        if not value.isdigit() or len(value) != 10:
            raise ue.PhoneFormatError
        else:
            self.__value = value


class Birthday(Field):
    def __init__(self, value):
        self._value = value
        super().__init__(self.__value)

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value):
        # Дата народження має бути у форматі DD.MM.YYYY (DD та MM можуть бути без нуля спереду)
        current_date = datetime.today().date()
        try:
            b_date = datetime.strptime(value, "%d.%m.%Y").date()
        except:
            raise ue.BirthdayFormatError
        else:
            if b_date > current_date:
                raise ue.BirthdayInFutureError
            b_date_str = datetime.strftime(b_date, "%d.%m.%Y")
            self.__value = b_date_str


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        for idx, p in enumerate(self.phones):
            if p.value == phone:
                self.phones.pop(idx)

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def __str__(self):
        return f"Name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        birthdays_by_day = defaultdict(list)
        current_date = datetime.today().date()
        # current_weekday = current_date.weekday()
        # first_weekday_name = calendar.day_name[0]
        res_list = []
        res_str = ""
        for name, record in self.data.items():
            user_name = name
            if record.birthday is None:
                continue
            user_birthday = datetime.strptime(
                record.birthday.value, "%d.%m.%Y").date()
            # user_name = user["name"]
            # user_birthday = user["birthday"].date()
            birthday_this_year = user_birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday_this_year.replace(
                    year=birthday_this_year.year + 1)
            delta_days = (birthday_this_year - current_date).days
        # у розрізі дат, повертаємо іменинників, які мають дні народження у наступні 7 днів (включно з сьогоднішнім)
        # функціонал переносу відображення вихідних та відображення у розрізі назв днів тижня відключено
            if delta_days < 7:
                # birthday_weekday = birthday_this_year.weekday()
                # birthday_weekday_name = calendar.day_name[birthday_weekday]
                birthday_day = birthday_this_year
                birthdays_by_day[birthday_day].append(user_name)
                # # виклик у неділю:
                # if current_weekday == 6:
                #     if birthday_weekday == 6:       # іменинників поточної НД переносимо на ПН
                #         birthdays_by_weekday[first_weekday_name].append(
                #             user_name)
                #     elif birthday_weekday != 5:     # іменинники ПН-ПТ у свої дні, іменинників наступної СБ не виводимо у цей тиждень
                #         birthdays_by_weekday[birthday_weekday_name].append(
                #             user_name)
                # # виклик у понеділок:
                # elif current_weekday == 0:
                #     if birthday_weekday < 5:        # іменинники ПН-ПТ у свої дні, іменинників наступної СБ-НД не виводимо у цей тиждень
                #         birthdays_by_weekday[birthday_weekday_name].append(
                #             user_name)
                # # виклик у інші дні:
                # else:
                #     if birthday_weekday < 5:        # іменинники ПН-ПТ у свої дні
                #         birthdays_by_weekday[birthday_weekday_name].append(
                #             user_name)
                #     else:                           # іменинників СБ-НД переносимо на ПН
                #         birthdays_by_weekday[first_weekday_name].append(
                #             user_name)
        for day, user_names in birthdays_by_day.items():
            res_list.append(str(day) + ": " + (", ").join(user_names))
        res_list.sort()
        if len(res_list) > 0:
            res_str = ("\n").join(res_list)
        else:
            res_str = "No birthdays in the next 7 days."
        return res_str
