
import pytest
from scraping import *
from products import Product, ProductDatabase

class TestFurnitureRetrieval:    
    def test_should_retrieve_html_parsed_from_url(self):
        html_parsed = retrieve_html_parsed_from_url('Cadeira escritorio')
        assert html_parsed is not None
        assert type(html_parsed) == BeautifulSoup
    
    def test_should_get_info_list_about_products(self):
        parsed_html = ParsedPage.parsed_html
        previous_total = ProductDatabase.get_products_total()
        products = get_info_list_about_products(parsed_html)
        # import pdb; pdb.set_trace()
        assert type(products) == list
        assert ProductDatabase.get_products_total() == len(products) + previous_total

    # def test_should_match_get_info_list_about_products_total_with_product_database_total(self):
    #     parsed_html = ParsedPage.parsed_html
    #     previous_total = ProductDatabase.get_products_total()
    #     products = get_info_list_about_products(parsed_html)
    #     # import pdb; pdb.set_trace()
    #     assert ProductDatabase.get_products_total() == len(products) + previous_total
    
    currency_test_data = [
        ('1.234,78', 1234.78),
        ('538,90', 538.90),
        ('34.890,90', 34890.90),
        ('1,90', 1.90)
    ]
    @pytest.mark.parametrize("currency_str,expected_float", currency_test_data)
    def test_should_convert_BRL_currency_to_float(self, currency_str, expected_float):
        value = convert_BRL_currency_to_float(currency_str)
        assert value == expected_float
    
    # def test_should_get_info_dict_for_product(self):
    #     parsed_html = ParsedPage.parsed_html
    #     grid_items = parsed_html.find_all("div", class_="product-grid-item")
    #     item = grid_items[0]
    #     # import pdb; pdb.set_trace()
    #     info_dict = get_info_dict_for_product(item)
    #     assert type(info_dict) == dict


class TestProductStorage:
    def test_should_store_products_on_json(self):
        import os
        # import pdb; pdb.set_trace()
        # products = ProductDatabase.products
        store_products_on_json(ProductDatabase.products, 'products.json')
        assert os.path.exists('products.json') == True
    
    def test_should_populate_products_database_from_json_and_return_list(self):
        ProductDatabase.clear_database()
        # import pdb; pdb.set_trace()
        previous_total = ProductDatabase.get_products_total()
        products_list = populate_products_database_from_json_and_return_list()
        assert ProductDatabase.get_products_total() == previous_total + len(products_list)
        assert type(products_list[0]) == Product

    def test_filter_and_save_products_on_json(self):
        import os

        filter_and_save_products_on_json(price__lt=800, price__gte=300)
        assert os.path.exists('filtered_products.json') == True

