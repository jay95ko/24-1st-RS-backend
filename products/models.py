from django.db import models


class Product(models.Model):
    name        = models.CharField(max_length=45)
    dgree       = models.DecimalField()
    ml          = models.IntegerField()
    awards      = models.CharField(max_length=45)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    expire_date = models.CharField(max_length=45)
    keep        = models.CharField(max_length=100)
    grade       = models.DecimalField()
    category    = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="product")
    brewery     = models.ForeignKey("Brewery", on_delete=models.CASCADE, related_name="product")
    sidedish    = models.ManyToManyField("Sidedish", on_delete=models.CASCADE, related_name="product", null=True)
    tag         = models.ManyToManyField("Tag", on_delete=models.CASCADE, related_name="product", null=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name

class Product_img(models.Model):
    img_url = models.URLField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="img")

    class Meta:
        db_table = "product_imgs"

    def __str__(self):
        return self.product.name + "'s imgs"

class Category(models.Model):
    name        = models.CharField(max_length=45)
    description = models.CharField(max_length=200)
    

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name

class Brewery(models.Model):
    name    = models.CharField(max_length=45)
    img_url = models.URLField(null=True)
    

    class Meta:
        db_table = "breweries"

    def __str__(self):
        return self.name

class Description(models.Model):
    product      = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="description")
    point_flavor = models.CharField(max_length=200)
    point_side   = models.CharField(max_length=200)
    point_story  = models.CharField(max_length=200)
    flavor       = models.CharField(max_length=400)
    side         = models.CharField(max_length=400)
    story        = models.CharField(max_length=400)

    class Meta:
        db_table = "descriptions"

    def __str__(self):
        return self.product.name + "'s description"

class Sidedish(models.Model):
    name    = models.CharField(max_length=45)
    img_url = models.URLField(null=True)

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

class Product_Flavor(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="flavor_relation")
    flavor  = models.ForeignKey("Flavor", on_delete=models.CASCADE, related_name="product_relation")
    point   = models.IntegerField()

    class Meta:
        db_table = "products_flavors"

    def __str__(self):
        return self.product.name + self.flavor.flavor_name + "= " + self.point

class Order_item(models.Model):
    product  = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="order_item")
    order    = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_item")
    quantity = models.IntegerField()

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return self.product.name + self.quantity +"orders"

class Order(models.Model):
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="order")
    ordered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.user.name + "'s order"

class Shipment(models.Model):
    order         = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="shipment")
    shipmented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shipments"
