from django.db import models


class Product(models.Model):
    name             = models.CharField(max_length=45)
    tiny_description = models.CharField(max_length=100, null=True)
    dgree            = models.DecimalField(max_digits=3, decimal_places=1)
    ml               = models.IntegerField()
    awards           = models.CharField(max_length=45)
    price            = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    expire_date      = models.CharField(max_length=45)
    keep             = models.CharField(max_length=100)
    grade            = models.DecimalField(max_digits=2, decimal_places=1)
    category         = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    brewery          = models.ForeignKey("Brewery", on_delete=models.CASCADE, related_name="products")
    sidedish         = models.ManyToManyField("Sidedish", related_name="products", blank=True)
    tag              = models.ManyToManyField("Tag", related_name="products", blank=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image_url = models.URLField(max_length=1000)
    product   = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")

    class Meta:
        db_table = "product_imgs"

    def __str__(self):
        return self.product.name + "'s imgs"

class Category(models.Model):
    name        = models.CharField(max_length=45)
    description = models.CharField(max_length=200)
    image_url   = models.URLField(max_length=1000)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name

class Brewery(models.Model):
    name    = models.CharField(max_length=45)
    img_url = models.URLField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "breweries"

    def __str__(self):
        return self.name

class Description(models.Model):
    product      = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="descriptions")
    point_flavor = models.CharField(max_length=200)
    point_side   = models.CharField(max_length=200)
    point_story  = models.CharField(max_length=200)

    class Meta:
        db_table = "descriptions"

    def __str__(self):
        return self.product.name + "'s description"

class Sidedish(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(null=True)

    class Meta:
        db_table = "sidedishes"

    def __str__(self):
        return self.name

class Tag(models.Model):
    caption = models.CharField(max_length=100)

    class Meta:
        db_table = "tags"

class Flavor(models.Model):
    flavor_name = models.CharField(max_length=45)

    class Meta:
        db_table = "flavors"

    def __str__(self):
        return self.flavor_name

class ProductFlavor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="flavor_relation")
    flavor  = models.ForeignKey("Flavor", on_delete=models.CASCADE, related_name="product_relation")
    point   = models.IntegerField()

    class Meta:
        db_table = "products_flavors"

    def __str__(self):
        return self.product.name + self.flavor.flavor_name + "= " + self.point

class OrderItem(models.Model):
    product  = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="order_items")
    order    = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return self.product.name + self.quantity +"orders"

class Order(models.Model):
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.user.name + "'s order"

class Shipment(models.Model):
    order         = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="shipments")
    shipmented_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shipments"
