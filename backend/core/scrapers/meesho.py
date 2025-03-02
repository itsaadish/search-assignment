# backend/core/scrapers/meesho.py
from .base import BaseScraper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urlencode, quote
import time

class MeeshoScraper(BaseScraper):
    # Filter configuration mapping
    FILTER_MAP = {
        "color": {"label_id": 4, "name": "Color"},
        "gender": {"label_id": 9, "name": "Gender"},
        "size": {"label_id": 17, "name": "Size"}
    }

    # Predefined filter data for gender, color, and size
    FILTERS_DATA = {
        "all_filters": [
            {
                "label_id": 9,  # Gender
                "label": "Gender",
                "values": [
                    {
                        "label_value_id": 443,
                        "display_name": "Women",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy45Iiwib3AiOiJpbiIsInZhbHVlIjoiNDQzIn0="
                    },
                    {
                        "label_value_id": 444,
                        "display_name": "Men",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy45Iiwib3AiOiJpbiIsInZhbHVlIjoiNDQ0In0="
                    },
                    {
                        "label_value_id": 445,
                        "display_name": "Girls",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy45Iiwib3AiOiJpbiIsInZhbHVlIjoiNDQ1In0="
                    },
                    {
                        "label_value_id": 446,
                        "display_name": "Boys",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy45Iiwib3AiOiJpbiIsInZhbHVlIjoiNDQ2In0="
                    }
                ]
            },
            {
                "label_id": 4,  # Color
                "label": "Color",
                "values": [
                    {
                        "label_value_id": 29,
                        "display_name": "Black",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiMjkifQ=="
                    },
                    {
                        "label_value_id": 30,
                        "display_name": "White",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiMzAifQ=="
                    },
                    {
                        "label_value_id": 32,
                        "display_name": "Brown",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbUVlIjoiMzIifQ=="
                    },
                    {
                        "label_value_id": 36,
                        "display_name": "Grey",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiMzYifQ=="
                    },
                    {
                        "label_value_id": 37,
                        "display_name": "Khaki",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiMzcifQ=="
                    },
                    {
                        "label_value_id": 39,
                        "display_name": "Multicolor",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiMzkifQ=="
                    },
                    {
                        "label_value_id": 40,
                        "display_name": "Olive",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDAifQ=="
                    },
                    {
                        "label_value_id": 41,
                        "display_name": "Orange",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDEifQ=="
                    },
                    {
                        "label_value_id": 42,
                        "display_name": "Pink",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDIifQ=="
                    },
                    {
                        "label_value_id": 43,
                        "display_name": "Purple",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDMifQ=="
                    },
                    {
                        "label_value_id": 44,
                        "display_name": "Red",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDQifQ=="
                    },
                    {
                        "label_value_id": 47,
                        "display_name": "Silver",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy40Iiwib3AiOiJpbiIsInZhbHVlIjoiNDcifQ=="
                    }
                ]
            },
            {
                "label_id": 17,  # Size
                "label": "Size",
                "values": [
                    {
                        "label_value_id": 596,
                        "display_name": "L",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjU5NiJ9"
                    },
                    {
                        "label_value_id": 597,
                        "display_name": "M",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjU5NyJ9"
                    },
                    {
                        "label_value_id": 599,
                        "display_name": "S",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjU5OSJ9"
                    },
                    {
                        "label_value_id": 601,
                        "display_name": "Xl",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjYwMSJ9"
                    },
                    {
                        "label_value_id": 602,
                        "display_name": "Xs",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjYwMiJ9"
                    },
                    {
                        "label_value_id": 604,
                        "display_name": "XXS",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjYwNCJ9"
                    },
                    {
                        "label_value_id": 605,
                        "display_name": "Xxxl",
                        "payload": "eyJmaWVsZCI6ImxhYmVscy4xNyIsIm9wIjoiaW4iLCJ2YWx1ZSI6IjYwNSJ9"
                    }
                ]
            }
        ]
    }

    def _construct_meesho_url(self, query):
        """
        Constructs Meesho URL with filters based on query parameters.
        Format: {product_type, color, gender, size}
        """
        base_url = "https://www.meesho.com/search"
        params = {
            "q": query["product_type"],
            "searchIdentifier": "text_search"
        }
        params_list = [f"{k}={v}" for k, v in params.items()]

        filter_index = {k: 0 for k in self.FILTER_MAP}  # Track filter indices

        for filter_type in ["color", "gender", "size"]:
            if not query.get(filter_type):
                continue

            filter_cfg = self.FILTER_MAP[filter_type]
            filter_group = next(
                (f for f in self.FILTERS_DATA["all_filters"]
                if f["label_id"] == filter_cfg["label_id"]), None
            )

            if not filter_group:
                continue

            # Find matching filter value (case-insensitive)
            filter_value = next(
                (v for v in filter_group["values"]
                 if v["display_name"].strip().lower() == query[filter_type].strip().lower()),
                None
            )

            if filter_value:
                idx = filter_index[filter_type]
                base = f"{filter_cfg['name']}[{idx}]"

                params_list.append(f"{base}[id]={filter_value['label_value_id']}")
                params_list.append(f"{base}[label]={filter_value['display_name']}")
                params_list.append(f"{base}[payload]={quote(filter_value['payload'])}")

                filter_index[filter_type] += 1

        final_url = f"{base_url}?{'&'.join(params_list)}"
        return final_url

    def search_product(self, parsed_query):
        """
        Navigates to the Meesho search page with filters applied.
        """
        search_url = self._construct_meesho_url(parsed_query)
        self.driver.get(search_url)

        # Dismiss any initial pop-ups or overlays
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
            )
            close_button.click()
        except (NoSuchElementException, TimeoutException):
            pass  # No pop-up found, proceed

        time.sleep(2)  # Allow time for results to load

    def get_results(self):
        """
        Extracts product data from the search results page.
        Returns up to 20 products.
        """
        products = []
        
        items = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".NewProductCardstyled__CardStyled-sc-6y2tys-0"))
        )

        print(items[:min(20, len(items))])

        for card in items[:min(20, len(items))]:
            try:
            # Extract title from the product title element
                try:
                    title = card.find_element(By.CSS_SELECTOR, ".NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5").text
                except NoSuchElementException:
                    title = "N/A"
                
                # Extract price from the price element (h5 tag)
                try:
                    price = card.find_element(By.CSS_SELECTOR, "h5.sc-eDvSVe.dwCrSh").text
                except NoSuchElementException:
                    price = "N/A"
                
                # Extract the image URL from the <img> tag within the card
                try:
                    image_url = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                except NoSuchElementException:
                    image_url = "N/A"
                
                # Extract the product URL from the parent <a> tag
                try:
                    product_url = card.find_element(By.XPATH, "..").get_attribute("href")
                except NoSuchElementException:
                    product_url = "N/A"
                
                # Optionally extract the size, if available. Replace '.size-class' with the actual selector.
                try:
                    size = card.find_element(By.CSS_SELECTOR, ".size-class").text
                except NoSuchElementException:
                    size = "N/A"
                
                # Append the extracted details to your products list
                products.append({
                    "title": title,
                    "price": price,
                    "size": size,
                    "image_url": image_url,
                    "product_url": product_url
                })
            except NoSuchElementException as e:
                print(f"Error extracting product data: {e}")
                print(card.get_attribute('outerHTML'))
                continue  # Skip incomplete product cards

        return products