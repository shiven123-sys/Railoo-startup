from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import RestroomRating


@receiver(post_save, sender=RestroomRating)
@receiver(post_delete, sender=RestroomRating)
def refresh_restroom_rating(sender, instance, **kwargs):
    instance.restroom.recalculate_rating()
