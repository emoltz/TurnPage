from django.http import HttpResponse
from django.templatetags.static import static
from django.views.decorators.http import require_POST


@require_POST
def htmx_test(request):
    static_url = static("js/book_covers/image.jpg")
    return HttpResponse(
        '<img class="img" src="' + static_url + '"alt="">'
    )

