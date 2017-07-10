from interscraped import (
    roto_guru,
    def_pts_vs,
    player_data,
    consistency_ratings,
    player_projections
)


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


def def_vs(options=None):
    return def_pts_vs.scraper()


def indiv_player(options=None):
    return player_data.scraper()


def player_consistency(options=None):
    return consistency_ratings.scraper()


def indiv_projections(options=None):
    return player_projections.scraper()
