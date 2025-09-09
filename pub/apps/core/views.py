from django.views.generic import TemplateView

from apps.catalog.models import Offering


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offerings"] = Offering.objects.filter(is_active=True)
        return context
