import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from telegram import Update
from telegram.ext import CallbackContext
from shop.models import Order
from .bot import telegram_bot

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def telegram_webhook(request):
    """Обработка webhook от Telegram бота"""
    try:
        data = json.loads(request.body)
        update = Update.de_json(data, telegram_bot.bot)
        
        # Обработка callback query (нажатия на кнопки)
        if update.callback_query:
            handle_callback_query(update.callback_query)
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return JsonResponse({'status': 'error'}, status=500)

def handle_callback_query(callback_query):
    """Обработка нажатий на inline кнопки"""
    try:
        data = callback_query.data
        chat_id = callback_query.message.chat.id
        
        if data.startswith('confirm_payment_'):
            order_id = data.split('_')[-1]
            confirm_order_payment(order_id, chat_id, callback_query)
            
        elif data.startswith('reject_payment_'):
            order_id = data.split('_')[-1]
            reject_order_payment(order_id, chat_id, callback_query)
            
    except Exception as e:
        logger.error(f"Ошибка обработки callback query: {e}")

# Для совместимости с polling
async def handle_callback_query_async(update, context):
    """Асинхронная обертка для polling"""
    await handle_callback_query(update.callback_query)

def confirm_order_payment(order_id, chat_id, callback_query):
    """Подтверждение оплаты заказа"""
    try:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.status = 'confirmed'
        order.save()
        
        # Отправляем уведомления клиенту
        try:
            from shop.notifications import NotificationService
            NotificationService.send_order_status_notification(order)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомлений клиенту: {e}")
        
        # Отправляем уведомление клиенту в Telegram (если есть)
        # telegram_bot.send_payment_confirmation(order)
        
        # Обновляем сообщение с кнопками
        callback_query.edit_message_text(
            text=f"✅ Оплата заказа #{order.id} подтверждена администратором.\n📧 Клиенту отправлено уведомление на email.",
            reply_markup=None
        )
        
        logger.info(f"Администратор подтвердил оплату заказа #{order_id}")
        
    except Order.DoesNotExist:
        callback_query.answer("Заказ не найден", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка подтверждения оплаты: {e}")
        callback_query.answer("Ошибка подтверждения оплаты", show_alert=True)

def reject_order_payment(order_id, chat_id, callback_query):
    """Отклонение оплаты заказа"""
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'cancelled'
        order.save()
        
        # Обновляем сообщение с кнопками
        callback_query.edit_message_text(
            text=f"❌ Оплата заказа #{order.id} отклонена администратором.",
            reply_markup=None
        )
        
        logger.info(f"Администратор отклонил оплату заказа #{order_id}")
        
    except Order.DoesNotExist:
        callback_query.answer("Заказ не найден", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка отклонения оплаты: {e}")
        callback_query.answer("Ошибка отклонения оплаты", show_alert=True)
