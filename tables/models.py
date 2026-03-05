from django.db import models


class Table(models.Model):
    """A restaurant table with a corresponding QR code URL."""
    table_number = models.PositiveIntegerField(unique=True)
    qr_code = models.CharField(
        max_length=200,
        blank=True,
        help_text='QR code URL, e.g. /table/5',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['table_number']

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = f'/table/{self.table_number}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Table {self.table_number}'
