from django.conf import settings
from django.core.cache import cache
from apps.solutions.models import Solution, SolutionCategory
from apps.categories.models import Category


def global_context(request):
    cache_key = 'global_context_data'
    cached = cache.get(cache_key)

    if not cached:
        nav_solutions = list(
            Solution.objects.filter(status='published', is_featured=True)
            .values('title', 'slug', 'solution_category__name')
            .order_by('sort_order')[:8]
        )
        solution_categories = list(
            SolutionCategory.objects.filter(is_active=True).values('name', 'slug').order_by('sort_order')
        )
        nav_categories = list(
            Category.objects.filter(level=0, is_active=True, show_in_nav=True)
            .order_by('sort_order')[:10]
        )
        cached = {
            'nav_solutions': nav_solutions,
            'solution_categories': solution_categories,
            'nav_categories': nav_categories,
        }
        cache.set(cache_key, cached, 600)

    return {
        **cached,
        'SITE_URL': settings.SITE_URL,
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
    }
