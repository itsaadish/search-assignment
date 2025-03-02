# backend/core/tasks.py
from .models import SearchQuery, ProductResult
from .scrapers import MeeshoScraper, NykaaScraper, FabIndiaScraper
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def start_scraping(search_id):
    try:
        search = SearchQuery.objects.get(id=search_id)
        parsed_query = search.parsed_query

        # Get the channel layer
        channel_layer = get_channel_layer()
        room_group_name = f'search_{search_id}'

        # Function to send logs to the frontend
        def send_log(message):
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'send_update',
                    'message': message,
                }
            )

        # Function to send status updates to the frontend
        def send_status(status):
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'send_update',
                    'status': status,
                }
            )
        
        # Initialize scrapers
        scrapers = {
            'meesho': MeeshoScraper(),
            'nykaa': NykaaScraper(),
            'fabindia': FabIndiaScraper()
        }
        send_log("Scraping started")
        logger.info("Scraping started")
        print("scraping started")
        # Run scraping for each requested brand
        brands = parsed_query.get('brands', ['meesho', 'nykaa'])  # Get the list or default
        if not brands:  # If the list is empty, replace it with the default
            brands = [ 'nykaa','meesho']
        print(brands)
        logger.info(f"Brands to search: {brands}")
        for brand in brands:
            if brand.lower() in scrapers:
                scraper = scrapers[brand.lower()]
                try:
                    send_log(f"Searching for {brand}")
                    logger.info(f"Searching for {brand}")
                    scraper.search_product(parsed_query)
                    results = scraper.get_results()
                    logger.info(f"Found {len(results)} products for {brand}")
                    # Save results
                    for result in results:
                        print(result)
                        ProductResult.objects.create(
                            search=search,
                            website=brand,
                            **result
                        )
                        logger.info(f"Product saved: {result['title']}")
                except Exception as e:
                    error_message = f"Error in scraping or storing data for {brand}: {e}"
                    send_log(error_message)
                    logger.error(error_message)
                    # Log scraping errors
                    continue
                finally:
                    scraper.close()
        
        search.status = 'completed'
        send_status('completed')
        search.save()
        
    except Exception as e:
        error_message = f"Error in start_scraping: {e}"
        send_log(error_message)
        logger.error(error_message)
        search.status = 'failed'
        search.save()
        send_status('failed')
        raise e