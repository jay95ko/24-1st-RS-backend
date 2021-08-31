from django.db import models


class Cart(models.Model):
    user     = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="cart")
    product  = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField()

    class Meta:
        db_table = "carts"

    def __str__(self):
        return self.user.name + "'s cart"