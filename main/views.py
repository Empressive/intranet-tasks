from django.views.generic import TemplateView, View
from django.http.response import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse

from .models import Term, ToDo

from .constants import CATEGORIES_CHOICES, PRIORITY_CHOICES


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


class ApiView(View):
    response = []

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        self.response = []

        params = request.GET.copy()
        query = {}

        todo = ToDo.objects

        if not params:
            for row in todo.all().values():
                self.response.append(row)

            return JsonResponse(self.response, safe=False)

        for key in params:
            if key not in ['name', 'description', 'is_done', 'priority', 'parent']:
                return HttpResponseBadRequest(
                    'Parameter "{}" is not allowed for this method'.format(key)
                )

            if not params[key]:
                continue

            if key == 'name':
                query[key] = params[key]

            if key == 'description':
                query['{}__icontains'.format(key)] = params[key]

            if key == 'is_done':
                if params[key] in ['True', 'true', '1']:
                    query[key] = 1
                elif params[key] in ['False', 'false', '0']:
                    query[key] = 0
                else:
                    return HttpResponseBadRequest(
                        'Value "{}" is not allowed for "{}" field'.format(params[key], key)
                    )

            if key == 'priority':
                if (params[key], params[key]) not in PRIORITY_CHOICES:
                    return HttpResponseBadRequest(
                        'Value "{}" is not allowed for "{}" field'.format(params[key], key)
                    )

                query['priority'] = params[key]

            if key == 'parent':
                query['parent__name__icontains'] = params[key]

        todo = todo.filter(**query).values()

        for row in todo:
            self.response.append(row)

        return JsonResponse(self.response, safe=False)

    def post(self, request):
        return HttpResponseNotAllowed('GET')
