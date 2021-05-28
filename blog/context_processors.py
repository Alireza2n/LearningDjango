import datetime

from blog.models import Category


def shared_context(request):
    """
    This method holds shared context variables
    across all templates
    """
    return {
        'year': datetime.datetime.today().year,
        'category_list': Category.objects.values_list('name')
    }
