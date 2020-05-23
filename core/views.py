from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Q

from .models import Document, Chapter

# Home page view
class Home(ListView):
    model = Chapter
    template_name = 'pages/home.html'
    context_object_name = 'chapters'

# Uploading document page view
class Upload(CreateView):
    model = Document
    template_name = 'pages/upload.html'
    fields = ['file']
    success_url = '/'

# Displaying search results page view
class Search(TemplateView):
    model = Chapter
    template_name = 'pages/search.html'

    # Get searched string or None
    def get_query(self, *args, **kwargs):
        if self.request.GET.get('query'):
            return self.request.GET.get('query').split(' ')
        else:
            return None

    # Run the query
    def get_result(self, q, *args, **kwargs):
        return self.model.objects.filter(Q(title__icontains=q) | Q(text__icontains=q)).distinct()

    # Check if query returned anything and merge all result lists
    def get_queryset(self, *agrs, **kwargs):
        if not self.get_query():
            return None
        else:
            results = []
            for q in self.get_query():
                if results == []:
                    results = self.get_result(q)
                else :
                    results = list(set(results) & set(self.get_result(q)))
            return results

    # Send all necessary variables to page render
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query') or ''
        context['results'] = self.get_queryset()
        return context
