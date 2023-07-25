#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Set the DJANGO_SETTINGS_MODULE environment variable to point to your settings.py file.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openai_test.settings")

    # Load Django settings
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
