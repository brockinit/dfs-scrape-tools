from distutils.core import setup

setup(
    name='mypackage',
    packages=['mypackage'],  # this must be the same as the name above
    version='0.0.1',
    description='A web scraper that obtains and parses NFL stats and fantasy data',
    author='Brock Lanoza',
    author_email='brock@sudokrew.com',
    url='https://github.com/brockinit/mypackage',  # use the URL to the github repo
    download_url='https://github.com/peterldowns/mypackage/archive/0.1.tar.gz',  # I'll explain this in a second
    keywords=['web-scrape', 'scraper', 'daily', 'fantasy', 'sports'],
    classifiers=[],
    install_requires=['bs4', 'requests'],
)
