from django.core.exceptions import ValidationError


class ChainLinkSerializerValidator:

    def __init__(self, data: dict):
        self.is_factory = data.get('is_factory')
        self.is_retail_network = data.get('is_retail_network')
        self.is_individual_entrepreneur = data.get('is_individual_entrepreneur')
        self.supplier = data.get('supplier')
        self.debt_to_the_supplier = data.get('debt_to_the_supplier')

    def __call__(self):
        if not self.is_factory and not self.is_retail_network and not self.is_individual_entrepreneur:
            raise ValidationError('Должен быть указан тип занятости')

        if self.is_factory:
            if self.supplier or self.debt_to_the_supplier:
                raise ValidationError('У завода не может быть поставщиков электроники и задолженности перед ними')
