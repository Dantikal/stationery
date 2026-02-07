from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Product
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    """Запускает collectstatic при сохранении товара с изображением"""
    try:
        # Проверяем есть ли изображение
        if instance.image:
            logger.info(f"Товар {instance.name} сохранен с изображением, запускаем collectstatic...")
            # Запускаем collectstatic
            call_command('collectstatic', '--noinput', verbosity=0)
            logger.info("collectstatic успешно выполнен")
    except Exception as e:
        logger.error(f"Ошибка при выполнении collectstatic: {e}")
