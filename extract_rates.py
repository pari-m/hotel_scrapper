import sys

import requests
from datetime import datetime
from pydantic import BaseModel
import csv
from pathlib import Path

BASE_URL = "https://www.qantas.com/hotels/api/ui/properties/"


class Rate(BaseModel):
    room_name: str
    rate_name: str
    no_of_guests: int
    cancellation_policy: str
    price: float
    best_deal: bool
    currency: str
    timestamp: str


class HotelDetailsScraper:
    def __init__(self, csv_file_path):
        self.csv_file_location = csv_file_path
        self.rates = []

    def construct_url(self, hotels_id, check_in, check_out):
        base_url = BASE_URL
        #found this url in the network tab of the developer tools :)
        url = f"{base_url}{hotels_id}/availability?checkIn={check_in}&checkOut={check_out}&adults=2&children=0&infants=0&payWith=cash"
        return url

    def make_request(self, url):
        headers = {'Referer': url}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: Unable to fetch data. {e}")
            return None

    def scrape_details(self):
        with open(self.csv_file_location, 'r') as hotel_list_file:
            hotel_list = csv.DictReader(hotel_list_file)
            for one_days_details in hotel_list:
                hotels_id, check_in, check_out = one_days_details['hotels_id'], one_days_details['check_in'], one_days_details['check_out']
                url = self.construct_url(hotels_id, check_in, check_out)
                json_data = self.make_request(url)
                if json_data:
                    self.extract_rates(json_data)
                    self.write_rates_to_csv()

    def extract_rates(self, json_data):
        for room_type in json_data.get('roomTypes'):
            for offer in room_type.get('offers'):
                rate = Rate(
                    room_name=room_type.get("name"),
                    rate_name=offer.get("name"),
                    no_of_guests=room_type.get("maxOccupantCount"),
                    cancellation_policy=offer.get("cancellationPolicy", {}).get("description"),
                    price=offer.get("charges", {}).get("total", {}).get("amount"),
                    best_deal=offer.get("promotion", {}).get("name", "") == "Top Deal",
                    currency=offer.get("charges", {}).get("total", {}).get("currency"),
                    timestamp=datetime.now().isoformat()
                )
                self.rates.append(rate)
                print(rate.json())

    def write_rates_to_csv(self):
        csv_write_file_path = 'check_in_check_out_details/extracted_rates.csv'
        with open(csv_write_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Room Name', 'Rate Name', 'Number of Guests', 'Cancellation Policy', 'Price', 'Top Deal', 'Currency',
                 'Timestamp'])
            for rate in self.rates:
                writer.writerow([
                    rate.room_name,
                    rate.rate_name,
                    rate.no_of_guests,
                    rate.cancellation_policy,
                    rate.price,
                    rate.best_deal,
                    rate.currency,
                    rate.timestamp
                ])

        print(f'Rates have been written to {csv_write_file_path}')


if __name__ == "__main__":
    print(f"")
    print(f"Name of csv file to process? Press enter to use default file ")
    file_name = input()
    if len(file_name) == 0:
        print(f"Using default file")
        file_name = 'raw_files/hotels.csv'
    elif Path(file_name).exists():
        print(f"file exists using {file_name} csv file")
    else:
        print(f"File {file_name} does not exist please try again")
        sys.exit()
    scraper = HotelDetailsScraper(file_name)
    scraper.scrape_details()