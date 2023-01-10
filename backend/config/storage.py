import django

from whitenoise.storage import CompressedManifestStaticFilesStorage

# https://adamj.eu/tech/2022/01/26/django-and-source-maps/#backport-to-the-future


class SourceMappedStaticFilesStorage(CompressedManifestStaticFilesStorage):
    if django.VERSION < (4, 0):
        patterns = CompressedManifestStaticFilesStorage.patterns + (
            (
                "*.js",
                (
                    (
                        r"(?m)^(//# (?-i:sourceMappingURL)=(.*))$",
                        "//# sourceMappingURL=%s",
                    ),
                ),
            ),
            (
                "*.css",
                (
                    (
                        r"(?m)^(/\*#[ \t](?-i:sourceMappingURL)=(.*)[ \t]*\*/)$",
                        "/*# sourceMappingURL=%s */",
                    ),
                ),
            ),
        )
    elif django.VERSION < (4, 1):
        # Django 4.0 switched to named patterns
        patterns = CompressedManifestStaticFilesStorage.patterns + (
            (
                "*.css",
                (
                    (
                        r"(?m)^(?P<matched>/\*#[ \t](?-i:sourceMappingURL)=(?P<url>.*)[ \t]*\*/)$",
                        "/*# sourceMappingURL=%(url)s */",
                    ),
                ),
            ),
        )
    else:
        raise AssertionError(
            "The above backported custom patterns are no longer required."
        )
