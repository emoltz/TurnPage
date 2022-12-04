from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.templatetags.static import static
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView
from django.core import serializers
from utils.db_functions import *
import random
from django_htmx.middleware import HtmxDetails

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

# Create your views here.
class OnboardingView(LoginRequiredMixin, TemplateView):
    template_name = "bookSwiping/onboarding.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_list = Genre.objects.all()
        # genre_list = ["Romance", "Sci-Fi", "Fantasy", "Mystery", "Young Adult", "Philosophy", "Religion", "History", "Biography"]
        context["genre_list"] = genre_list
        return context


class BookshelfView(LoginRequiredMixin, TemplateView):
    model = Book
    template_name = "bookSwiping/bookshelf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_books = []
        liked_books_database = Bookshelf.objects.all().filter(
            user=user, read_status="U"
        )
        for book in liked_books_database:
            liked_books.append(book.book)

        context["bookshelf"] = liked_books
        saved_books = []
        saved_books_database = Bookshelf.objects.all().filter(
            user=user, read_status="R"
        )

        for book in saved_books_database:
            saved_books.append(book.book)

        context["saved_books"] = saved_books
        context["liked_books_json"] = serializers.serialize("json", liked_books)
        return context


@require_POST
@login_required
def selected_genres(request):
    # user = request.user
    genre_list = request.POST.getlist("selected_genres[]")
    if genre_list:
        for genre in genre_list:
            addUserGenre(request.user, genre)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def move_to_saved_books(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "R")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def move_to_liked_books(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "U")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def delete_book(request):
    book_id = request.POST.get("book_id")
    if book_id:
        book = Book.objects.get(id=book_id)
        moveShelf(book, request.user, "T")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@login_required
@require_POST
def book_shelf(request):
    user = request.user
    book_id = request.POST.get("id")
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            # book.users_liked_list.add(request.user)
            addToShelf(book, user, "R")
            # returns JSON response
            return JsonResponse({"status": "ok"})
        except Book.DoesNotExist:
            pass
    # if fails
    return JsonResponse({"status": "error"})


@login_required
@require_POST
def book_like(request):
    # get current user
    user = request.user
    # the below commented-put line is if we want to extend the user class in the future
    # t_user = TurnPageUser.objects.get(user=user)

    # get the book id from the request
    book_id = request.POST.get("id")
    # get action, if specified in HTML
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            # book.users_liked_list.add(request.user)
            recommended_book = addToShelf(book, user, "U")
            # TODO take the recommended book id and display that 2 books deep
            # returns JSON response
            return JsonResponse({"status": "ok",
                                 "body": recommended_book.json()})
        except Book.DoesNotExist:
            # if book doesn't exist, do nothing... we may want to log something to the console at some point.
            pass
    # if fails
    return JsonResponse({"status": "error"})


@login_required
@require_POST
def book_dislike(request):
    # get current user
    user = request.user
    # the below commented-put line is if we want to extend the user class in the future
    # t_user = TurnPageUser.objects.get(user=user)

    # get the book id from the request
    book_id = request.POST.get("id")
    # get action, if specified in HTML
    action = request.POST.get("action")
    if book_id or action:
        try:
            # DB Functions go below
            book = Book.objects.get(id=book_id)
            addToShelf(book, user, "T")
            # returns JSON response
            return JsonResponse({"status": "ok"})
        except Book.DoesNotExist:
            # if book doesn't exist, do nothing... we may want to log something to the console at some point.
            pass
    # if fails
    return JsonResponse({"status": "error"})


class HomeView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "books"
    template_name = "bookSwiping/home.html"
    recommended_book_list = []
    next_recommended_book = model.objects.all()[0]
    test = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        # change context data based on book swipe

        

        context = super().get_context_data(**kwargs)
        all_books = self.model.objects.all()

        # book_id = 36
        # self.next_recommended_book = self.model.objects.get(id=book_id)




        # Mock rec engine
        try:
            ud = UserDemographics.objects.get(user=self.request.user)
            genres = list(ud.genre.all())
            lists = []
            for g in genres:
                nyt = list(g.nyt_list.all())
                for n in nyt:
                    if n not in lists:
                        lists.append(n)
            if lists:
                items = list(self.model.objects.filter(nyt_lists__in=lists))
            else:
                items = list(self.model.objects.all())
        except ObjectDoesNotExist:
            # if any of the above aren't found, give the default
            items = list(self.model.objects.all())
        ubs = list(Bookshelf.objects.filter(user=self.request.user))
        for i in range(len(items)):
            if items[i] in ubs:
                del items[i]

        # change to how many random items you want
        semi_random_book_list = random.sample(items, 15)
        # creates a list of books, random for now, from the database
        context["all_books"] = all_books
        context["book01"] = semi_random_book_list[0]
        context["book02"] = semi_random_book_list[1]
        # add recommended book to book3

        # fetch with API
        # API info:
        # url: https://8kwwql5a02.execute-api.us-east-1.amazonaws.com/dev/
        # Params: uid, bid, direc

        # third book will be the first recommended book
        if len(self.recommended_book_list) != 0:
            context["book03"] = self.recommended_book_list[2]
            context["book04"] = self.recommended_book_list[3]
            context["book05"] = self.recommended_book_list[4]
            context["book06"] = self.recommended_book_list[5]
            context["book07"] = self.recommended_book_list[6]
            context["book08"] = self.recommended_book_list[7]
            context["book09"] = self.recommended_book_list[8]
            context["book10"] = self.recommended_book_list[9]
            context["book11"] = self.recommended_book_list[10]
            context["book12"] = self.recommended_book_list[11]
            context["book13"] = self.recommended_book_list[12]
            context["book14"] = self.recommended_book_list[13]
            context["book15"] = self.recommended_book_list[14]
        else:
            context["book03"] = semi_random_book_list[2]
            context["book04"] = semi_random_book_list[3]
            context["book05"] = semi_random_book_list[4]
            context["book06"] = semi_random_book_list[5]
            context["book07"] = semi_random_book_list[6]
            context["book08"] = semi_random_book_list[7]
            context["book09"] = semi_random_book_list[8]
            context["book10"] = semi_random_book_list[9]
            context["book11"] = semi_random_book_list[10]
            context["book12"] = semi_random_book_list[11]
            context["book13"] = semi_random_book_list[12]
            context["book14"] = semi_random_book_list[13]
            context["book15"] = semi_random_book_list[14]
        context["random_books"] = serializers.serialize("json", semi_random_book_list)
        return context


@require_POST
def htmx_test(request: HtmxHttpRequest) -> HttpResponse:
    books = Book.objects.all()
    book = books[1]
    # TODO so, I think the issue is that all the other post functions must be re-written as HTMX functions. So it should no longer return a json object, but the actual HTML that it will insert inot the next div
    static_url = static("js/book_covers/image.jpg")
    static_url2 = "https://storage.googleapis.com/du-prd/books/images/9780345484208.jpg"
    return HttpResponse(
        f'<img class="book-cover-img" src="{book.cover_img}"alt="">'
    )
