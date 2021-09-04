import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brewery, Sidedish, Tag, ProductImage, Description, Flavor, ProductFlavor

CSV_PATH_PRODUCT = "./backdata.csv"

with open(CSV_PATH_PRODUCT) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if not Category.objects.filter(name = row[6]):
            Category.objects.create(name = row[6], description = row[7], image_url = row[37])
            print("Create category " + row[22])

        if not Brewery.objects.filter(name = row[22]):
            Brewery.objects.create(name = row[22], img_url = row[23])
            print("Create brewery " + row[22])

        for num in range(0,3):
            if not Sidedish.objects.filter(name = row[16+num]):
                Sidedish.objects.create(name = row[16+num], image_url = row[19+num])
                print("Create sidedish " + row[16+num])

        for num in range(0,2):
            if not Tag.objects.filter(caption = row[2+num]):
                Tag.objects.create(caption = row[2+num])
                print("create tag " + row[2+num])

        if not Product.objects.filter(name = row[0]):
            category = Category.objects.get(name = row[6])
            brewery = Brewery.objects.get(name = row[22])
            Product.objects.create(
                name             = row[0],
                dgree            = row[8],
                ml               = row[9],
                awards           = row[5],
                expire_date      = row[11],
                keep             = row[12],
                grade            = row[4],
                price            = row[10],
                tiny_description = row[1]
                category         = category,
                brewery          = brewery,
            )
            print("create product " + row[0])

        for num in range(0,3):
            if not ProductImage.objects.filter(image_url = row[24+num]):
                product = Product.objects.get(name = row[0])
                ProductImage.objects.create(image_url = row[24+num], product=product)
                print("create" + row[0]+"'s image")
        
        if not Description.objects.filter(product = Product.objects.get(name = row[0])):
            Description.objects.create(
                product      = Product.objects.get(name = row[0]),
                point_flavor = row[13],
                point_side   = row[14],
                point_story  = row[15],
            )
            print("create" + row[0]+"'s description")

        for num in range(0,5):
            if not Flavor.objects.filter(flavor_name = row[27+num]):
                Flavor.objects.create(flavor_name = row[27+num])
                print("create flavor " + row[27+num])

            if not ProductFlavor.objects.filter(flavor = Flavor.objects.get(flavor_name = row[27+num]), product = Product.objects.get(name = row[0])):
                ProductFlavor.objects.create(
                    flavor  = Flavor.objects.get(flavor_name = row[27+num]),
                    product = Product.objects.get(name = row[0]),
                    point   = row[32+num],
                )
                print("create" + row[0]+"'s flavor relation " + row[27+num])

        product = Product.objects.get(name = row[0])
        for num in range(0,3):
            sidedish = Sidedish.objects.get(name = row[16+num])
            product.sidedish.add(sidedish)
            print("create" + row[0] + "'s sidedish" + row[16+num])
        
        for num in range(0,2):
            tag = Tag.objects.get(caption = row[2+num])
            product.tag.add(tag)
            print("create" + row[0] + "'s tag" + row[2+num])