from roto_guru import roto_guru_scraper


def main(job, options=None):
    scrapers = {
        'roto_guru_scraper': roto_guru_scraper
    }

    scrape_job = scrapers[job]

    if scrape_job:
        return scrape_job()
    else:
        print('No job of this type available')


main('roto_guru_scraper')
