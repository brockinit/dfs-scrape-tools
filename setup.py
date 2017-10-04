from distutils.core import setup

setup(
    name='interscraped',
    packages=['interscraped'],
    version='0.1.5',
    description='A web scraper that obtains and parses NFL stats and fantasy data',
    author='Brock Lanoza',
    author_email='brocklanoza@gmail.com',
    url='https://github.com/brockinit/dfs-scrape-tools',
    download_url='https://github.com/brockinit/dfs-scrape-tools/archive/0.1.5.tar.gz',
    keywords=['web-scrape', 'scraper', 'daily', 'fantasy', 'sports'],
    classifiers=[],
    license='MIT',
    install_requires=['bs4', 'requests', 'robobrowser']
)
