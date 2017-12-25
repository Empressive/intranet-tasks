from django.views.generic import TemplateView, View
from django.http.response import JsonResponse, HttpResponse

from .models import Term, ToDo

from .constants import CATEGORIES_CHOICES, PRIORITY_CHOICES


class BaseApiView(View):
    response = {'code': 400, 'data': []}

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        self.get_logic(request)

        if self.response['code'] != 200:
            return HttpResponse(self.response.get('message'), status=self.response['code'])

        return JsonResponse(self.response['data'], safe=False)

    def post(self, request):
        return HttpResponse(status=501)

    def get_logic(self, request):
        raise NotImplementedError


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


class ApiView(BaseApiView):
    def get_logic(self, request):
        self.response = {'code': 400, 'data': []}

        query = {}
        params = request.GET.copy()

        if not params:
            for row in ToDo.objects.all().values():
                self.response['data'].append(row)

            self.response['code'] = 200

            return

        for key in params:
            if key not in ['name', 'description', 'is_done', 'priority', 'parent']:
                self.response['code'] = 400
                self.response['message'] = 'Parameter "{}" is not allowed for this method'.format(key)

                return

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
                    self.response['code'] = 400
                    self.response['message'] = 'Value "{}" is not allowed for "{}" field'.format(params[key], key)

            if key == 'priority':
                if (params[key], params[key]) not in PRIORITY_CHOICES:
                    self.response['code'] = 400
                    self.response['message'] = 'Value "{}" is not allowed for "{}" field'.format(params[key], key)

                query['priority'] = params[key]

            if key == 'parent':
                query['parent__name__icontains'] = params[key]

        self.response['code'] = 200

        todo = ToDo.objects.filter(**query).values()

        for row in todo:
            self.response['data'].append(row)
