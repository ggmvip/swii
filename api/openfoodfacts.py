#!/usr/bin/env python3
"""
OpenFoodFacts API Wrapper
"""

import requests
import json
from typing import Optional, Dict
from .cache import APICache


class OpenFoodFactsClient:
    """
    Client for OpenFoodFacts API with caching support
    """
    
    BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
    
    def __init__(self, timeout: int = 5, use_cache: bool = True):
        """
        Initialize OpenFoodFacts client
        
        Args:
            timeout: Request timeout in seconds
            use_cache: Enable caching of API responses
        """
        self.timeout = timeout
        self.use_cache = use_cache
        
        if self.use_cache:
            self.cache = APICache(maxsize=500, ttl=3600)
    
    def get_product_info(self, barcode: str) -> Optional[Dict]:
        """
        Get product information from barcode
        
        Args:
            barcode: Product barcode (e.g., "3017620422003")
            
        Returns:
            Dict with product info or None if not found
            {
                'name': str,
                'brand': str,
                'material': str,  # Packaging material if available
                'category': str,
                'image_url': str
            }
        """
        # Check cache first
        if self.use_cache:
            cached_result = self.cache.get(barcode)
            if cached_result is not None:
                return cached_result
        
        try:
            # Clean barcode (remove spaces, special characters)
            barcode_clean = ''.join(filter(str.isdigit, barcode))
            
            if not barcode_clean:
                return None
            
            # Make API request
            url = f"{self.BASE_URL}/{barcode_clean}.json"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                # Cache "not found" for shorter TTL
                if self.use_cache:
                    self.cache.set(barcode, None, ttl=600)  # 10 minutes
                return None
            
            data = response.json()
            
            # Check if product exists
            if data.get("status") != 1 or not data.get("product"):
                if self.use_cache:
                    self.cache.set(barcode, None, ttl=600)
                return None
            
            # Extract product information
            product = data["product"]
            result = {
                'name': product.get('product_name', 'Unknown Product'),
                'brand': product.get('brands', ''),
                'material': self._extract_material(product),
                'category': product.get('categories', ''),
                'image_url': product.get('image_url', ''),
                'raw_data': product  # Keep raw data for debugging
            }
            
            # Cache successful result
            if self.use_cache:
                self.cache.set(barcode, result)
            
            return result
            
        except requests.Timeout:
            print(f"Timeout fetching product {barcode}")
            return None
        except requests.RequestException as e:
            print(f"API request failed for {barcode}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error for {barcode}: {e}")
            return None
    
    def _extract_material(self, product: Dict) -> str:
        """
        Extract packaging material from product data
        
        Args:
            product: Raw product dict from API
            
        Returns:
            Material string (e.g., "PET", "HDPE", "Glass")
        """
        # Check packaging field
        packaging = product.get('packaging', '').lower()
        
        # Common material keywords
        materials = {
            'pet': 'PET',
            'hdpe': 'HDPE',
            'plastic': 'Plastic',
            'glass': 'Glass',
            'metal': 'Metal',
            'aluminum': 'Aluminum',
            'cardboard': 'Cardboard',
            'paper': 'Paper'
        }
        
        for keyword, material_name in materials.items():
            if keyword in packaging:
                return material_name
        
        return 'Unknown'
    
    def get_cache_stats(self) -> Dict:
        """Get cache hit/miss statistics"""
        if self.use_cache:
            return self.cache.get_stats()
        return {'hits': 0, 'misses': 0, 'size': 0}


# Example usage
if __name__ == "__main__":
    client = OpenFoodFactsClient(use_cache=True)
    
    # Test with Coca-Cola barcode
    product = client.get_product_info("3017620422003")
    
    if product:
        print("Product found:")
        print(f"  Name: {product['name']}")
        print(f"  Brand: {product['brand']}")
        print(f"  Material: {product['material']}")
    else:
        print("Product not found")
    
    # Test cache
    product2 = client.get_product_info("3017620422003")  # Should be cached
    
    stats = client.get_cache_stats()
    print(f"\nCache stats: {stats}")
