from django.db import models

class AnalyticsReport(models.Model):
    generated_date = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50)  # 'breed_stats', 'milk_stats', etc.
    data = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['generated_date', 'report_type']),
        ]
        get_latest_by = 'generated_date'