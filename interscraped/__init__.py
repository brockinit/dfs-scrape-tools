from interscraped import roto_guru


def daily_fantasy(options=None):
    if not options:
        return roto_guru.scraper()
    else:
        years = weeks = game = None
        if 'years' in options:
            years = options['years']
        if 'weeks' in options:
            weeks = options['weeks']
        if 'game' in options:
            game = options['game']

        return roto_guru.scraper(years, weeks, game)
