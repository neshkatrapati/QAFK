from setuptools import setup, find_packages

setup(
    name="qafk",
    description="QT Application Framework",
    version="0.0.1.dev1",
    license="GPL",
    author="Ganesh Katrapati",
    author_email="ganesh@swecha.net",
    install_requires=['jinja2','pony'],
    packages = find_packages(),
    entry_points = {
        'console_scripts' : [
            'qafk=qafk.console:qafk'
        ]
    }
)
