from django.db import models


class Cart(models.Model):
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="carts")
    product    = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="carts")
    quantity   = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carts"

    def __str__(self):
        return self.user.name + "'s cart"