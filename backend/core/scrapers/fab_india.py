# backend/core/scrapers/fab_india.py
from .base import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class FabIndiaScraper(BaseScraper):
    def search_product(self, parsed_query):
        """Search for products on FabIndia"""
        self.driver.get("https://www.fabindia.com/")
        search_box = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-input"))
        )
        search_term = f"{parsed_query['color']} {parsed_query['product_type']}"
        search_box.send_keys(search_term)
        search_box.submit()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-list")))

    def get_results(self):
        """Extract product results from FabIndia"""
        products = []
        items = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item"))
        )

        for item in items[:5]:  # Limit to 5 results
            try:
                products.append({
                    "title": item.find_element(By.CSS_SELECTOR, ".product-name").text,
                    "price": item.find_element(By.CSS_SELECTOR, ".price").text.replace('₹', '').strip(),
                    "image_url": item.find_element(By.CSS_SELECTOR, "img.product-image").get_attribute("src"),
                    "product_url": item.find_element(By.CSS_SELECTOR, "a.product-link").get_attribute("href"),
                    "size": self._extract_size(item),
                    "material": self._extract_material(item)
                })
            except Exception as e:
                print(f"Error parsing FabIndia product: {str(e)}")
                continue
        
        return products

    def _extract_size(self, item):
        """Extract size information if available"""
        try:
            return item.find_element(By.CSS_SELECTOR, ".size-info").text
        except:
            return "Not specified"

    def _extract_material(self, item):
        """Extract material information if available"""
        try:
            return item.find_element(By.CSS_SELECTOR, ".material-info").text
        except:
            return "Not specified"