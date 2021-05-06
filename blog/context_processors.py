import datetime


def shared_context(request):
    """
    This method holds shared context variables
    across all templates
    """
    return {
        'year': datetime.datetime.today().year
    }
