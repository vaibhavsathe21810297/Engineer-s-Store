from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka	', 'Karnataka	'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False


CATEGORY_CHOICES = (
    ('cr', 'cricket'),
    ('ba', 'badminton'),
    ('cy', 'cycling'),
    ('fo', 'football'),
    ('sw', 'swimming'),
    ('vb', 'volleyball'),
    ('bb', 'basketball'),
    ('tt', 'tabletennis'),
    ('m','mobile'),
    ('tv', 'television'),
    ('l','laptop'),
    ('c','camera'),
    ('hp','Headphone'),
    ('s', 'speaker'),
    ('sm','smartwatch'),
    ('p', 'printer'),
    ('b','beds'),
    ('so','sofas'),
    ('ch','chairs'),
    ('t','tables'),
    ('wr','wardrobes'),
    ('sh','shelves'),
    ('ca','cabinet'),
    ('ma','mattress'),
    ('me','mens'),
    ('wo','women'),
    ('ki','kids'),
    ('s','shoes'),
    ('je', 'jewellery'),
    ('wa','watches'),
    ('ha','handbags'),
    ('sc','school'),
    ('ex','exam'),
    ('un','university'),
    ('cm','comics'),
    ('cd','children'),
    ('ac','air'),
    ('r','refrigerator'),
    ('w','washing'),
    ('cl','cooler'),
    ('f','fan'),
    ('v','vitamins'),
    ('p','personal'),
    ('fv','fruitvegetable'),
    ('be', 'beverages'),
    ('fg', 'foodgrains'),
    ('co','cookies'),
    ('no','noodles'),
    ('ol','oil'),
    ('sn', 'snacks'),
    ('de', 'deo'),
    ('qa', 'puma'),

)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    @staticmethod
    def get_orders_by_customer(customer_id):
        return OrderPlaced.objects.filter(customer=customer_id).order_by('-date')


class Feedback(models.Model):
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)