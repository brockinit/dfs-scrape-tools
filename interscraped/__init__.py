from interscraped import roto_guru, fantasy_data, def_pts_vs, player_data


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


def snap_counts(options=None):
    if not options:
        raise ValueError
    else:
        email = password = None
        if 'email' in options:
            email = options['email']
        if 'password' in options:
            password = options['password']
        if not email and not password:
            raise ValueError
        else:
            return fantasy_data.scraper(email, password)


def def_vs(options=None):
    if not options:
        raise ValueError
    else:
        email = password = None
        if 'email' in options:
            email = options['email']
        if 'password' in options:
            password = options['password']
        if not email and not password:
            raise ValueError
        else:
            return def_pts_vs.scraper(email, password)


def indiv_player_data(options=None):
    if not options:
        raise ValueError
    else:
        email = password = None
        if 'email' in options:
            email = options['email']
        if 'password' in options:
            password = options['password']
        if not email and not password:
            raise ValueError
        else:
            return player_data.scraper(email, password)
