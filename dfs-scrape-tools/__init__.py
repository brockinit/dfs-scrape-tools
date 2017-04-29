from roto_guru import roto_guru_scraper


def roto_guru(options):
    return roto_guru_scraper(options.years, options.weeks, options.game)
