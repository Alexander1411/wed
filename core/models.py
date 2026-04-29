from django.db import models


class RSVPResponse(models.Model):
    ATTENDANCE_COMING = "coming"
    ATTENDANCE_NOT_COMING = "not_coming"
    ATTENDANCE_PLUS_ONE = "plus_one"
    ATTENDANCE_CHOICES = [
        (ATTENDANCE_COMING, "Я приду / Мы придем"),
        (ATTENDANCE_NOT_COMING, "Прийти не получится"),
        (ATTENDANCE_PLUS_ONE, "Буду +1"),
    ]

    DRINK_RED_WINE = "red_wine"
    DRINK_WHITE_WINE = "white_wine"
    DRINK_WHISKY = "whisky"
    DRINK_VODKA = "vodka"
    DRINK_CHAMPAGNE = "champagne"
    DRINK_SOFT = "soft"
    DRINK_CHOICES = [
        (DRINK_RED_WINE, "Вино красное"),
        (DRINK_WHITE_WINE, "Вино белое"),
        (DRINK_WHISKY, "Виски"),
        (DRINK_VODKA, "Водка"),
        (DRINK_CHAMPAGNE, "Шампанское"),
        (DRINK_SOFT, "Что-нибудь безалкогольное"),
    ]

    attendance = models.CharField(max_length=20, choices=ATTENDANCE_CHOICES)
    full_name = models.CharField(max_length=255)
    drinks = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.get_attendance_display()})"
