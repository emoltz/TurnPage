from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from .models import *
import random


# Create your views here.
class BookshelfView(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = 'bookSwiping/bookshelf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        random_items = random.sample(list(self.model.objects.all()), 10)
        saved_books = random.sample(list(self.model.objects.all()), 10)
        context['books'] = random_items
        context['saved_books'] = saved_books
        return context


class HomeView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "bookSwiping/home.html"
    random_items = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(self.model.objects.all())
        # change to how many random items you want
        self.random_items = random.sample(items, 15)
        # creates a list of books, random for now, from the database
        context["book01"] = self.random_items[0]
        context["book02"] = self.random_items[1]
        context["book03"] = self.random_items[2]
        context["book04"] = self.random_items[3]
        context["book05"] = self.random_items[4]
        context["book06"] = self.random_items[5]
        context["book07"] = self.random_items[6]
        context["book08"] = self.random_items[7]
        context["book09"] = self.random_items[8]
        context["book10"] = self.random_items[9]
        context["book11"] = self.random_items[10]
        context["book12"] = self.random_items[11]
        context["book13"] = self.random_items[12]
        context["book14"] = self.random_items[13]
        context["book15"] = self.random_items[14]

        context["currentBook"] = self.getCurrentBook()

        return context

    def getCurrentBook(self):
        # this will be changed to get the current book that is on top
        pass

