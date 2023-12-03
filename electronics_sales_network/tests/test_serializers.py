from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from electronics_sales_network.models import Contact, Product
from electronics_sales_network.serializers import ChainLinkSerializer


class ChainLinkSerializerTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='testuser@email.com', is_staff=True, is_active=True)
        self.client.force_authenticate(user=self.user)

        self.contact = Contact.objects.create(
            email='contact1@example.com',
            country='Country1',
            city='City1',
            street='Street1',
            house_number=1,
        )
        self.product = Product.objects.create(
            name='Test Product',
            model='Test Model',
            release_date='2023-01-01',
        )
        self.chain_link_data = {
            'name': 'Test ChainLink',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': True,
            'is_retail_network': False,
            'is_individual_entrepreneur': False,
        }

    def test_valid_chain_link_serializer(self) -> None:
        """
        Тест на работу сериализатора с валидными данными
        :return: None
        """
        serializer = ChainLinkSerializer(data=self.chain_link_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_invalid_chain_link_serializer(self) -> None:
        """
        Нельзя указывать одновременно несколько типов занятости
        :return: None
        """
        # Тест на создание объекта ChainLink с неудовлетворяющим валидатору состоянием
        invalid_data: dict = {
            'name': 'Invalid ChainLink',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': True,
            'is_retail_network': True,  # Несоответствие условиям валидатора
            'is_individual_entrepreneur': True,  # Несоответствие условиям валидатора
        }

        serializer = ChainLinkSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_chain_link_serializer_with_debt_to_supplier(self) -> None:
        """
        Создание объекта с флагом is_factory = True и указанием долга перед поставщиком запрещено
        :return: None
        """
        data_with_debt: dict = {
            'name': 'ChainLink with Debt',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': True,
            'is_retail_network': False,
            'is_individual_entrepreneur': False,
            'debt_to_the_supplier': 1.01,
        }

        serializer = ChainLinkSerializer(data=data_with_debt)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_the_type_of_employment_is_not_specified(self) -> None:
        """
        Тест проверяет указан ли тип занятости
        :return: None
        """
        invalid_data: dict = {
            'name': 'Invalid ChainLink',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': False,
            'is_retail_network': False,
            'is_individual_entrepreneur': False,
        }

        serializer = ChainLinkSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
