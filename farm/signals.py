from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    Animal, VeterinaryLog, Field, Storage, CropRotation,
    Species, WorkLog, Purchase, SaleOrder, VetPlan
)
from .log_utils import log_action


def _get_user(sender, instance, **kwargs):
    if hasattr(instance, 'responsible_person') and instance.responsible_person:
        return instance.responsible_person
    if hasattr(instance, 'created_by') and instance.created_by:
        return instance.created_by
    if hasattr(instance, 'user') and instance.user:
        return instance.user
    return None


TRACKED_MODELS = {
    Animal: 'Animal',
    VeterinaryLog: 'VeterinaryLog',
    Field: 'Field',
    Storage: 'Storage',
    CropRotation: 'CropRotation',
    Species: 'Species',
    WorkLog: 'WorkLog',
    Purchase: 'Purchase',
    SaleOrder: 'SaleOrder',
    VetPlan: 'VetPlan',
}


@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    model_name = TRACKED_MODELS.get(sender)
    if not model_name:
        return
    action = 'create' if created else 'update'
    user = _get_user(sender, instance)
    log_action(
        user=user,
        action=action,
        model_name=model_name,
        object_id=instance.pk,
        object_repr=str(instance),
    )


@receiver(post_delete)
def log_delete_action(sender, instance, **kwargs):
    model_name = TRACKED_MODELS.get(sender)
    if not model_name:
        return
    user = _get_user(sender, instance)
    log_action(
        user=user,
        action='delete',
        model_name=model_name,
        object_id=instance.pk,
        object_repr=str(instance),
    )
