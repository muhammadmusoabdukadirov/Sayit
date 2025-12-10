from django.db import models
from django.core.validators import RegexValidator
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

phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',  # +998 bilan boshlanib, 9 ta raqam
    message="Telefon raqam quyidagi formatda bo'lishi kerak: +998901234567"
)

# Buyurtmalar modeli
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('processing', 'Jarayonda'),
        ('completed', 'Tugatilgan'),
    ]

    name = models.CharField(max_length=100, verbose_name="Ism familiya")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Telefon raqam")
    address = models.CharField(max_length=255, verbose_name="Manzil")
    carpet_type = models.ForeignKey(
        CarpetType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gilam turi"
    )
    other_carpet_name = models.CharField(
        max_length=100, blank=True, verbose_name="Boshqa gilam nomi",
        help_text="Agar ro`yxatda bo`lmasa, o`zingiz gilam nomini kiriting"
    )
    date = models.DateField(verbose_name="Buyurtma kuni")
    comment = models.TextField(blank=True, verbose_name="Izoh")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.name} — {self.phone}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class VisitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} - {self.timestamp}"