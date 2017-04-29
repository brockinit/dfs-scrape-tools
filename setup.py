from distutils.core import setup

setup(
    name='dfs-scrape-tools',
    packages=['dfs-scrape-tools'],
    version='0.0.1',
    description='A web scraper that obtains and parses NFL stats and fantasy data',
    author='Brock Lanoza',
    author_email='brock@sudokrew.com',
    url='https://github.com/brockinit/dfs-scrape-tools',
    download_url='https://github.com/brockinit/dfs-scrape-tools/archive/0.0.1.tar.gz',
    keywords=['web-scrape', 'scraper', 'daily', 'fantasy', 'sports'],
    classifiers=[],
    install_requires=['bs4', 'requests'],
)
