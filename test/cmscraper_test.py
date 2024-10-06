import unittest
from unittest.mock import patch, MagicMock
from src import cmscraper


class TestCMScraper(unittest.TestCase):

    @patch('requests.get')  # Mock requests.get to avoid actual API calls
    def test_fetch_accessories(self, mock_get):
        # Simulate a valid API response for accessories
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'name': 'Test Accessory',
                'id': 12345,
                'currentStock': 100,
                'totalTrades': 1000,
                'basePrice': 5000000,
                'mainCategory': 20,
                'subCategory': 1
            },
            {
                'name': 'Manos Belt',
                'id': 67890,
                'currentStock': 50,
                'totalTrades': 200,
                'basePrice': 100000000,
                'mainCategory': 20,
                'subCategory': 4
            }
        ]
        mock_get.return_value = mock_response

        # Call the function
        accessories = cmscraper.fetch_accessories()
        self.assertEqual(len(accessories), 2)
        self.assertEqual(accessories[0]['name'], 'Test Accessory')
        self.assertEqual(accessories[1]['name'], 'Manos Belt')
        accessories = cmscraper.filter_accessories(accessories)
        self.assertEqual(len(accessories), 1)
        self.assertEqual(accessories[0]['name'], 'Test Accessory')
        # Check if accessories are filtered correctly
        self.assertEqual(len(accessories), 1)  # Manos Belt should be filtered out
        self.assertEqual(accessories[0]['name'], 'Test Accessory')  # Only 'Test Accessory' should remain

    

    @patch('requests.get')
    def test_handle_api_error(self, mock_get):
        # Simulate an API error
        mock_response = MagicMock()
        mock_response.status_code = 500  # Internal Server Error
        mock_get.return_value = mock_response

        # Ensure that the function handles errors correctly
        with self.assertRaises(Exception):  # Adjust exception type based on your error handling
            cmscraper.fetch_accessories()  # Call the function and expect it to raise an error


if __name__ == '__main__':
    unittest.main()