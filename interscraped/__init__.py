from interscraped import (
    roto_guru,
    def_pts_vs,
    player_data,
    consistency_ratings,
    player_projections,
    fanduel_salaries,
    snap_counts
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


def def_vs(credentials, weeks=default_weeks, years=default_years):
    return def_pts_vs.scraper(credentials, weeks=default_weeks, years=default_years)


def player_stats(credentials, weeks=default_weeks, years=default_years):
    return player_data.scraper(credentials, weeks=default_weeks, years=default_years)


def player_consistency(file_path):
    return consistency_ratings.scraper(file_path)


def player_projections(credentials, weeks=default_weeks, years=default_years):
    return player_projections.scraper(credentials, weeks=default_weeks, years=default_years)


def player_snap_counts(credentials, weeks=default_weeks, years=default_years):
    return player_projections.scraper(credentials, weeks=default_weeks, years=default_years)


def player_salaries(credentials, weeks=default_weeks, years=default_years):
    return player_projections.scraper(credentials, weeks=default_weeks, years=default_years)
