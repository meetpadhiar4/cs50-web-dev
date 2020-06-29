from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Regular_pizza(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=64, default="Regular Pizza")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class Sicilian_pizza(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=64, default="Sicilian Pizza")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class Toppings(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64, default="Toppings")

    def __str__(self):
        return f"{self.name}"


class Subs(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    large = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=64, default="Subs")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2, default="0.00")
    category = models.CharField(max_length=64, default="Pasta")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class Salads(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2, default="0.00")
    category = models.CharField(max_length=64, default="Salads")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class Dinner_platters(models.Model):
    name = models.CharField(max_length=64)
    small = models.DecimalField(max_digits=4, decimal_places=2)
    large = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.CharField(max_length=64, default="Dinner Platter")

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Order(models.Model):
    status_choices = (
        ("Pending", "Pending"),
        ("Complete", "Complete"),
        ("Initiated", "Initiated")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_toppings = models.IntegerField(default=0)
    status = models.CharField(max_length=64, choices=status_choices, default="Pending")

    def __str__(self):
        return f"{self.user} - {self.status}"
