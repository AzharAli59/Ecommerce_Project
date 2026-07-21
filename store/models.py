from django.contrib.auth.models import User
from django.db import models


STATE_CHOICES = (
    ('Lahore', 'Lahore'),
    ('Karachi', 'Karachi'),
    ('Multan', 'Multan'),
    ('Yazman', 'Yazman'),
    ('Bahawalpur', 'Bahawalpur'),
    ('Islamabad', 'Islamabad'),
    ('Sialkot', 'Sialkot'),
    ('Faisalabad', 'Faisalabad'),
    ('Gujranwala', 'Gujranwala'),
    ('Khanewal', 'Khanewal'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    email = models.EmailField(default='azhar@gmail.com')
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=128)
    state = models.CharField(max_length=128, choices=STATE_CHOICES)

    def __str__(self):
        return self.name


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)


class Product(models.Model):
    title = models.CharField(max_length=128)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def item_cost(self):
        return self.quantity * self.product.discounted_price

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_cart_user_product',
            ),
        ]


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Accepted')

    @property
    def item_cost(self):
        return self.quantity * self.product.discounted_price
