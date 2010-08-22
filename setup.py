from setuptools import setup, find_packages

setup(
    name='tw2.jit',
    version='0.1a1',
    description='',
    author='Ralph Bean',
    author_email='ralph.bean@gmail.com',
    url='',
    install_requires=[
        "tw2.core",
        "genshi",
        ],
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    test_suite = 'nose.collector',
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        tw2.jit = tw2.jit
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    tests_require = ['BeautifulSoup'],
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
