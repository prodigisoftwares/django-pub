from django.utils import timezone


def set_published_at(model, prev_instance=None):
    """
    Set published_at based on current and previous publication status.

    Args:
        prev_instance: Previous instance of the publishable
        model (None for new model)
    """
    if prev_instance:
        # Updating existing article
        if not prev_instance.is_published and model.is_published:
            # Publishing for the first time
            model.published_at = timezone.now()
        elif prev_instance.is_published and not model.is_published:
            # Unpublishing
            model.published_at = None
        # If both states are the same, published_at remains unchanged
    else:
        # New article
        if model.is_published and not model.published_at:
            model.published_at = timezone.now()
        elif not model.is_published:
            model.published_at = None
