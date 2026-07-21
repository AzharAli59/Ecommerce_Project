from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cart, Customer, OrderPlaced, Product


class CartFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='azhar',
            email='azhar@example.com',
            password='pass12345',
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass12345',
        )
        self.product = Product.objects.create(
            title='Test Mobile',
            selling_price=Decimal('1500.00'),
            discounted_price=Decimal('1200.00'),
            description='A test product',
            brand='Samsung',
            category='M',
            product_image='productimg/test.png',
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name='Azhar',
            email='azhar@example.com',
            phone='1234567890',
            state='Lahore',
            address='Street 1',
        )
        self.other_customer = Customer.objects.create(
            user=self.other_user,
            name='Other',
            email='other@example.com',
            phone='0987654321',
            state='Karachi',
            address='Street 2',
        )

    def test_cart_page_requires_login(self):
        response = self.client.get(reverse('showcart'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_add_to_cart_reuses_existing_row_and_increments_quantity(self):
        self.client.force_login(self.user)

        self.client.get(reverse('add-to-cart'), {'prod_id': self.product.id})
        self.client.get(reverse('add-to-cart'), {'prod_id': self.product.id})

        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)

    def test_buy_now_adds_product_and_redirects_to_checkout(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('add-to-cart'), {
            'prod_id': self.product.id,
            'next': reverse('checkout'),
        })

        self.assertRedirects(response, reverse('checkout'))
        self.assertTrue(Cart.objects.filter(user=self.user, product=self.product).exists())

    def test_checkout_renders_user_address_state(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=1)

        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lahore')
        self.assertNotContains(response, 'Karachi')

    def test_minus_cart_does_not_reduce_quantity_below_one(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=1)

        response = self.client.get(reverse('minuscart'), {'prod_id': self.product.id})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['quantity'], 1)
        self.assertEqual(Cart.objects.get(user=self.user, product=self.product).quantity, 1)

    def test_profile_always_assigns_logged_in_user(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('profile'), {
            'user': self.other_user.id,
            'name': 'My Address',
            'email': 'mine@example.com',
            'phone': '1234567890',
            'state': 'Lahore',
            'address': 'Street 3',
        })

        self.assertEqual(response.status_code, 200)
        customer = Customer.objects.get(name='My Address')
        self.assertEqual(customer.user, self.user)

    def test_payment_uses_only_logged_in_users_address(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=2)

        response = self.client.post(reverse('paymentdone'), {
            'custid': self.other_customer.id,
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(OrderPlaced.objects.count(), 0)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)

    def test_payment_creates_orders_and_clears_cart(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=2)

        response = self.client.post(reverse('paymentdone'), {
            'custid': self.customer.id,
        })

        self.assertRedirects(response, reverse('orders'))
        order = OrderPlaced.objects.get(user=self.user)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
