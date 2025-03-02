# backend/core/scrapers/nykaa.py
from .base import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class NykaaScraper(BaseScraper):
    # Filter configuration mapping
    FILTER_MAP = {
        "color": {"key": "color_filter", "title": "Color"},
        "gender": {"key": "gender_filter", "title": "Gender"},
        "size": {"key": "instock_size_nykaa_filter", "title": "Size"}
    }

    # Predefined filter data for gender, color, and size
    FILTERS_DATA = {
        "gender_filter": {
            "Men": "5197",
            "Women": "5196",
            "Boys": "5199",
            "Girls": "5198"
        },
        "color_filter": {
            "Blue": "16",
            "Black": "67",
            "Navy Blue": "19",
            "Grey": "69",
            "White": "23",
            "Green": "20",
            "Multi-Color": "470",
            "Brown": "229",
            "Pink": "65",
            "Beige": "22",
            "Olive": "230",
            "Red": "66",
            "Yellow": "70",
            "Khaki": "238",
            "Off White": "228",
            "Purple": "72",
            "Orange": "68",
            "Maroon": "227",
            "Cream": "9575",
            "Charcoal": "23732",
            "Indigo": "9973",
            "Peach": "71",
            "Burgundy": "9509",
            "Ivory": "4102",
            "Silver": "144",
            "Tan": "671",
            "Rust": "231",
            "Lavender": "21",
            "Wine": "20558",
            "Mustard": "17",
            "Teal": "18",
            "Mauve": "24360",
            "Coral": "127",
            "Turquoise": "235",
            "Aqua": "25816",
            "Nude": "237",
            "Gold": "145",
            "Magenta": "234",
            "Taupe": "236"
        },
        "instock_size_nykaa_filter": {
            "XXS": "18826",
            "XS": "18827",
            "S": "18828",
            "M": "18829",
            "L": "18831",
            "XL": "18832",
            "2XL": "18833",
            "3XL": "18834",
            "4XL": "18835",
            "5XL": "18836",
            "Free Size": "18842",
            "0-3 months": "18516",
            "3-6 months": "18517",
            "6-9 months": "18518",
            "9-12 months": "18519",
            "12-24 Months": "18520",
            "2-4 years": "18521",
            "4-6 years": "18522",
            "6-8 years": "18523",
            "8-10 years": "18524",
            "10-12 years": "18525",
            "12-14 years": "18526",
            "14-16 years": "18527",
            "16+": "18528",
            "24": "18875",
            "26": "18877",
            "28": "18879",
            "30": "18881",
            "32": "18883",
            "34": "18885",
            "36": "18887",
            "38": "18891",
            "40": "18895",
            "42": "18898",
            "44": "18900"
        }
    }

    def search_product(self, parsed_query):
        """
        Navigates to the Nykaa Fashion search page with filters applied.
        """
        search_url = self._construct_nykaa_url(parsed_query)
        print(f"Searching Nykaa Fashion with URL: {search_url}")
        try:
            self.driver.get(search_url)
        except Exception as e:
            print(f"Error navigating to Nykaa Fashion URL: {e}")

        # Dismiss any initial pop-ups or overlays
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
            )
            close_button.click()
        except (NoSuchElementException, TimeoutException):
            print("No pop-up found")
            pass  # No pop-up found, proceed

        time.sleep(2)  # Allow time for results to load

    def _construct_nykaa_url(self, query):
        """
        Constructs Nykaa Fashion URL with filters combined into a single 'f' parameter.
        Format: {product_type, color, gender, size}
        """
        base_url = "https://www.nykaafashion.com/catalogsearch/result/"
        params = {
            "q": query["product_type"]
        }

        # List to store filter strings
        filter_strings = []

        # Add filter parameters
        for filter_type in ["gender", "size", "color"]:
            if not query.get(filter_type):
                continue

            filter_cfg = self.FILTER_MAP[filter_type]
            filter_key = filter_cfg["key"]
            
            # Get the filter value mapping
            filter_mapping = self.FILTERS_DATA.get(filter_key, {})
            
            # Find matching filter value (case-insensitive)
            # Try exact match first
            filter_id = None
            for key, val in filter_mapping.items():
                if key.lower() == query[filter_type].lower():
                    filter_id = val
                    break
            
            # If no exact match, try partial match
            if filter_id is None:
                for key, val in filter_mapping.items():
                    if query[filter_type].lower() in key.lower() or key.lower() in query[filter_type].lower():
                        filter_id = val
                        break
            
            if filter_id:
                # Append the filter string in the format "key=value_"
                filter_strings.append(f"{filter_key}%3D{filter_id}_")

        # Combine all filter strings into a single 'f' parameter
        if filter_strings:
            params["f"] = "%3B".join(filter_strings)

        # Construct the final URL with parameters
        param_str = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{base_url}?{param_str}"

    def get_results(self):
        """ Extracts product data from Nykaa Fashion search results page. Returns up to 20 products. """
        products = []
        try:
            # Wait for product cards to load
            product_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-384pms"))
            )


            print(product_cards[:min(20, len(product_cards))])

            # Process up to 20 product cards
            for card in product_cards[:min(20, len(product_cards))]:
                try:
                    # Extract product title
                    try:
                        brand = card.find_element(By.CSS_SELECTOR, "[data-at='product-title']").text
                    except NoSuchElementException:
                        brand = "N/A"

                    # Extract brand
                    try:
                        title = card.find_element(By.CSS_SELECTOR, "[data-at='product-subtitle']").text
                    except NoSuchElementException:
                        title = "N/A"

                    # Extract price
                    try:
                        price = card.find_element(By.CSS_SELECTOR, ".css-1ijk06y").text
                    except NoSuchElementException:
                        price = "N/A"

                    # Extract image URL
                    try:
                        image_url = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    except NoSuchElementException:
                        image_url = "N/A"

                    # Extract product URL
                    try:
                        product_url = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    except NoSuchElementException:
                        product_url = "N/A"

                    # Add extracted product data to list
                    products.append({
                        "title": title,
                        "price": price,
                        "image_url": image_url,
                        "product_url": product_url
                    })
                except Exception as e:
                    print(f"Error extracting product data: {e}")
                    continue
        
        except Exception as e:
            print(f"Error in nykaa get_results: {e}")
        return products