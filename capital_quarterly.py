import pandas as pd
from .my_class import MyClass

class CapitalQuarterly(MyClass):
    def __init__(self):
        super().__init__()
        self._members = []

    def add_member(self, base_date, capital, cta, pre_tax_income, share_buy_back):
        member = CapitalQuarterlyMember(base_date, capital, cta, pre_tax_income, share_buy_back)
        self._members.append(member)
        data = {
            'base_date': member.base_date,
            'capital': member.capital,
            'cta': member.cta,
            'pre_tax_income': member.pre_tax_income,
            'share_buy_back': member.share_buy_back
        }
        self.add_data(**data)


class CapitalQuarterlyMember:
    def __init__(self, base_date, capital, cta, pre_tax_income, share_buy_back):
        self.base_date = base_date
        self.capital = capital
        self.cta = cta
        self.pre_tax_income = pre_tax_income
        self.share_buy_back = share_buy_back

    @property
    def base_date(self):
        return self._base_date

    @base_date.setter
    def base_date(self, value):
        if not self._is_valid_date(value):
            raise ValueError("The date must be a valid quarter-end date.")
        self._base_date = value

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, value):
        if value < 0:
            raise ValueError("Capital should be a positive value.")
        self._capital = value

    @property
    def share_buy_back(self):
        return self._share_buy_back

    @share_buy_back.setter
    def share_buy_back(self, value):
        if value < 0:
            raise ValueError("Share buy back should be a positive value.")
        self._share_buy_back = value

    @staticmethod
    def _is_valid_date(date):
        return date.month in [3, 6, 9, 12] and date.day == pd.Timestamp(date).days_in_month





