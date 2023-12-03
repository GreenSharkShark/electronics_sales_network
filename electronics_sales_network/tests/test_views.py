from rest_framework import status
from rest_framework.test import APITestCase
from electronics_sales_network.models import Contact, Product
from users.models import User


class ChainLinkViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.contact_data = {
            'email': 'contact1@example.com',
            'country': 'Country1',
            'city': 'City1',
            'street': 'Street1',
            'house_number': 1,
        }
        self.product_data = {
            'name': 'Test Product',
            'model': 'Test Model',
            'release_date': '2023-01-01',
        }
        self.contact = Contact.objects.create(**self.contact_data)
        self.product = Product.objects.create(**self.product_data)
        self.chain_link_data = {
            'name': 'Test ChainLink',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': True,
            'is_retail_network': False,
            'is_individual_entrepreneur': False,
        }
        self.user = User.objects.create(email='testuser@email.com', is_staff=True, is_active=True)
        self.client.force_authenticate(user=self.user)

    def test_create_chain(self) -> None:
        """
        Проверка создания объекта
        """
        response = self.client.post('/chains/', data=self.chain_link_data)

        expected_response_data = {
            'id': response.data.get('id'),
            'name': 'Test ChainLink',
            'debt_to_the_supplier': None,
            'date_of_creation': response.data.get('date_of_creation'),
            'is_factory': True,
            'is_retail_network': False,
            'is_individual_entrepreneur': False,
            'contacts': response.data.get('contacts'),
            'products': response.data.get('products'),
            'supplier': None
        }

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_response_data, response.data)

    def test_get_chains_list(self) -> None:
        """
        Проверка получения списка объектов
        """
        self.client.post('/chains/', data=self.chain_link_data)
        self.client.post('/chains/', data=self.chain_link_data)
        response = self.client.get('/chains/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_chain_retrieve(self) -> None:
        """
        Проверка получения объекта по id
        """
        chain = self.client.post('/chains/', data=self.chain_link_data)
        response = self.client.get(f'/chains/{chain.data.get("id")}/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_chain_delete(self) -> None:
        """
        Проверка удаления объекта
        """
        chain = self.client.post('/chains/', data=self.chain_link_data)
        response = self.client.delete(f'/chains/{chain.data.get("id")}/')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_chain_update(self) -> None:
        """
        Проверка обновления объекта
        """
        chain = self.client.post('/chains/', data=self.chain_link_data)
        updated_data = {'name': 'Not Test ChainLink',
                        'is_factory': True,
                        'is_retail_network': False,
                        'is_individual_entrepreneur': False,
                        'contacts': self.contact.pk,
                        'products': self.product.pk
                        }
        response = self.client.put(f'/chains/{chain.data.get("id")}/', data=updated_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data.get('name'), updated_data['name'])

    def test_chain_update_debt_to_the_supplier_is_forbidden(self) -> None:
        """
        Проверка запрета на обновление задолженности перед поставщиком
        """
        data = {
            'name': 'Test ChainLink',
            'contacts': self.contact.pk,
            'products': self.product.pk,
            'is_factory': False,
            'is_retail_network': True,
            'is_individual_entrepreneur': False,
            'debt_to_the_supplier': 1.01
        }
        chain = self.client.post('/chains/', data=data)
        data['debt_to_the_supplier'] = 1.02
        response = self.client.put(f'/chains/{chain.data.get("id")}/', data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
