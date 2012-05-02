from setuptools import setup

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

setup(
    name='tw2.jit',
    version='2.0.3',
    description='toscawidgets2 wrapper for the javascript infovis toolkit(jit)',
    long_description=long_description,
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://github.com/toscawidgets/tw2.jit',
    license='MIT',
    install_requires=[
        "tw2.core>=2.0.0",
        "tw2.jquery",
        "genshi",
        "mako",
        "tw2.sqla",
        "sqlalchemy",
        "BeautifulSoup",
        ],
    packages=[
        'tw2',
        'tw2.jit',
        'tw2.jit.samples',
        'tw2.jit.widgets',
    ],
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        tw2.jit = tw2.jit
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
    ],
)
