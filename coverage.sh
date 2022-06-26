
coverage run -m pytest && coverage report && coverage html && python -m webbrowser htmlcov/index.html > /dev/null 2>&1
