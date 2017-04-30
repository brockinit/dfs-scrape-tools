from distutils.core import setup

setup(
    name='interscraped',
    packages=['interscraped'],
    version='0.0.6',
    description='A web scraper that obtains and parses NFL stats and fantasy data',
    author='Brock Lanoza',
    author_email='brock@sudokrew.com',
    url='https://github.com/brockinit/dfs-scrape-tools',
    download_url='https://github.com/brockinit/dfs-scrape-tools/archive/0.0.6.tar.gz',
    keywords=['web-scrape', 'scraper', 'daily', 'fantasy', 'sports'],
    classifiers=[],
    install_requires=['bs4', 'requests']
)
