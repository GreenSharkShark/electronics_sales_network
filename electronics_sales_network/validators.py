from django.core.exceptions import ValidationError


class ChainLinkValidator:

    def __init__(self, data: dict):
        self.is_factory = bool(data.get('is_factory'))
        self.is_retail_network = bool(data.get('is_retail_network'))
        self.is_individual_entrepreneur = bool(data.get('is_individual_entrepreneur'))
        self.supplier = data.get('supplier')
        self.debt_to_the_supplier = data.get('debt_to_the_supplier')

    def __call__(self):
        if not self.is_factory and not self.is_retail_network and not self.is_individual_entrepreneur:
            raise ValidationError('Должен быть указан тип занятости')

        if self.is_factory:
            if self.supplier or self.debt_to_the_supplier:
                raise ValidationError('У завода не может быть поставщиков электроники и задолженности перед ними')

        if self.is_factory and self.is_retail_network and self.is_individual_entrepreneur:
            raise ValidationError('Нельзя выбирать несколько видов занятости одновременно')

        if not (self.is_factory ^ bool(self.is_retail_network) ^ self.is_individual_entrepreneur):
            raise ValidationError('Нельзя выбирать несколько видов занятости одновременно')
