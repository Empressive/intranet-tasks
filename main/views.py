from django.views.generic import TemplateView

from .models import Term

from .constants import CATEGORIES_CHOICES


class Dinner(TemplateView):
    template_name = 'dinner.html'


class Vocabulary(TemplateView):
    template_name = 'vocabulary.html'

    def get_context_data(self, **kwargs):
        letters = set()
        terms = Term.objects.all().order_by('name')

        for term in terms:
            letters.add(term.name[0].upper())

        context = {
            'categories': CATEGORIES_CHOICES,
            'terms': terms,
            'letters': sorted(letters)
        }

        return context
