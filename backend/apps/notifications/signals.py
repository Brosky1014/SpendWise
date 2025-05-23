from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from django.contrib.auth import get_user_model
from .models import Notification
from apps.users.models import Profile
from decimal import Decimal

User = get_user_model()

@receiver(post_save, sender=Transaction)
def create_transaction_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            notification_type='TRANSACTION',
            title=f"New {instance.category.get_type_display()}",
            message=f"{instance.name} of ₦{instance.amount} was recorded",
            related_url="/history/"
        )

@receiver(post_save, sender=Budget)
def create_budget_notification(sender, instance, created, **kwargs):
    if not created and instance.spent_amount() > instance.amount * Decimal('0.8'):
        Notification.objects.create(
            user=instance.user,
            notification_type='BUDGET_ALERT',
            title=f"Budget Alert: {instance.name}",
            message=f"You've spent {instance.spent_amount()/instance.amount*100:.0f}% of your budget",
            related_url="/budgets/"
        )
        
@receiver(post_save, sender=User)
def user_notifications(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance,
            title="Welcome!",
            message="Thanks for joining SpendWise. We hope you enjoy your experience.",
            related_url="/dashboard/"
        )
    
        
@receiver(pre_save, sender=Profile)
def check_balance_change(sender, instance, **kwargs):
    if instance.pk: 
        try:
            old = Profile.objects.get(pk=instance.pk)
            if old.starting_balance != instance.starting_balance:
                Notification.objects.create(
                    user=instance.user,
                    title="Balance Updated",
                    message=f"Your starting balance was updated to ₦{instance.starting_balance}",
                    related_url="/dashboard/"
                )
        except Profile.DoesNotExist:
            pass