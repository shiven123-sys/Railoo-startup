from django.conf import settings


def site_meta(request):
    """Small set of globals every template can use without re-fetching them."""
    return {
        "SITE_NAME": "Railoo",
        "SITE_TAGLINE": "Swachh Safar, Surakshit Bharat",
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
