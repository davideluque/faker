from typing import List, Optional, Union
from .. import Provider as BaseProvider
import datetime


class Provider(BaseProvider):
    """
    A Faker provider for the Danish SSN (cpr) numbers and VAT IDs
    """

    vat_id_formats = ("DK########",)

    def vat_id(self) -> str:
        """
        Returns a random generated Danish Tax ID
        """

        return self.bothify(self.random_element(self.vat_id_formats))

    def danish_control_digits(self, birthday: datetime.date) -> List[int]:
        year = birthday.year
        century = int(str(year)[:2])
        year_digits = int(str(year)[2:])

        if century == 18:
            if 58 <= year_digits <= 99:
                return [5, 6, 7, 8]
            else:
                raise ValueError(
                    f"Invalid birthday: {birthday}. Danish CPR numbers are only distributed to persons born between 1858 and 2057.")
        elif century == 19:
            if 0 <= year_digits <= 36:
                return [0, 1, 2, 3]
            else:  # 37 <= year_digits <= 99
                return [0, 1, 2, 3, 4, 9]
        else:  # century >= 20
            if 0 <= year_digits <= 36:
                return [4, 5, 6, 7, 8, 9]
            elif 37 <= year_digits <= 57:
                return [5, 6, 7, 8]
            else:
                raise ValueError(
                    f"Invalid birthday: {birthday}. Danish CPR numbers are only distributed to persons born between 1858 and 2057.")

    def cpr(self, formatted: bool = False, birthday: Optional[datetime.date] = None, gender: Optional[str] = None) -> str:
        """Generate a random Danish CPR number.

        Keyword Arguments:
        formatted {bool} -- Specifies if the number is formatted with dividers (default: {False})
        birthday {datetime.date} -- Specifies the birthday for the id number (default: {None})
        gender {str} -- Specifies the gender for the id number. Must be "male" or "female" if present (default: {None})
        """

        if birthday is None:
            birthday = self.generator.date_of_birth()

        valid_control_digits = self.danish_control_digits(birthday)
        control_digit = self.random_element(valid_control_digits)

        digits = list(range(0, 10))

        if gender is None:
            gender_digit = self.random_element(digits)
        elif gender.lower() == 'male':
            gender_digit = self.random_element([d for d in digits if d % 2 != 0])
        elif gender.lower() == 'female':
            gender_digit = self.random_element([d for d in digits if d % 2 == 0])
        else:
            raise ValueError("Invalid gender. Must be 'male', 'female', or None.")

        cpr_number = f"{birthday.strftime('%d%m%y')}" + (f"-" if formatted else "") + \
            f"{control_digit}" + f"{self.random_int(0, 99):02d}" + f"{gender_digit}"
        return cpr_number
