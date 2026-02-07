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
            logger.info(f"Товар {instance.name} сохранен с изображением: {instance.image.name}")
            logger.info(f"Путь к изображению: {instance.image.path}")
            logger.info(f"URL изображения: {instance.image.url}")
            
            # Запускаем collectstatic только в продакшене
            from django.conf import settings
            if not settings.DEBUG:
                logger.info("Запускаем collectstatic для сохранения media файлов...")
                call_command('collectstatic', '--noinput', verbosity=0)
                logger.info("collectstatic успешно выполнен")
        else:
            logger.info(f"Товар {instance.name} сохранен без изображения")
    except Exception as e:
        logger.error(f"Ошибка при обработке товара: {e}")
