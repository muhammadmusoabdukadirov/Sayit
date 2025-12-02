from django.db import models
from django.contrib.auth.models import User


# Gilam turlari modeli
class CarpetType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Gilam turi nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    price_per_m2 = models.IntegerField(verbose_name="1 m² narxi (so`m)")

    class Meta:
        verbose_name = "Gilam turi"
        verbose_name_plural = "Gilam turlari"

    def __str__(self):
        return self.name


# Buyurtmalar modeli
class Order(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism familiya")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    address = models.CharField(max_length=255, verbose_name="Manzil")
    carpet_type = models.ForeignKey(CarpetType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gilam turi")
    other_carpet_name = models.CharField( max_length=100, blank=True, verbose_name="Boshqa gilam nomi",
            help_text="Agar ro`yxatda bo`lmasa, o`zingiz gilam nomini kiriting")
    date = models.DateField(verbose_name="Buyurtma kuni")
    comment = models.TextField( blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.name} — {self.phone}"


class VisitorCount(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Sana")
    count = models.IntegerField(default=1, verbose_name="Kirishlar soni")

    class Meta:
        verbose_name = "Saytga kirishlar"
        verbose_name_plural = "Saytga kirishlar statistikasi"

    def __str__(self):
        return f"{self.date} — {self.count} ta kirish"


class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name="Foydalanuvchi ismi")
    message = models.TextField(verbose_name="Izoh matni")
    rating = models.IntegerField(
        choices=[(i, f"{i} Yulduz") for i in range(1, 5+1)],
        verbose_name="Reyting"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yozilgan sana")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"

    def __str__(self):
        return f"{self.name} — {self.rating} ⭐"
