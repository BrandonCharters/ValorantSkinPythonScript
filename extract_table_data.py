import requests
from bs4 import BeautifulSoup
import csv

# List of weapon names to construct URLs
weapon_names = [
    # "Classic",
    # "Shorty",
    # "Frenzy",
    # "Ghost",
    # "Sheriff",
    # "Stinger",
    # "Spectre",
    # "Bucky",
    # "Judge",
    # "Bulldog",
    # "Guardian",
    # "Phantom",
    # "Vandal",
    # "Marshal",
    # "Operator",
    # "Outlaw",
    # "Ares",
    # "Odin",
    "Melee",  # Include Melee
]

# Base URL structure
base_url = "https://valorant.fandom.com/wiki/"

# Iterate through each weapon
for weapon in weapon_names:
    url = f"{base_url}{weapon}"
    print(f"Scraping URL: {url}")

    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        continue

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the first table with the class "wikitable sortable"
    table = soup.select_one("table.wikitable.sortable")
    if not table:
        print(f"No table found for {weapon}. Skipping...")
        continue

    # Extract rows from the table
    rows = table.select("tbody tr")
    csv_data = []

    # Different logic for Melee table
    if weapon == "Melee":
        headers = [
            "Skin Image",
            "Skin Collection",
            "Skin Name",
            "Skin Cost",
            "Skin Weapon",
        ]
        csv_data.append(headers)

        for row in rows:
            cells = row.find_all("td")
            if not cells or len(cells) < 4:
                continue

            # Check if there's a rowspan to update the collection
            if cells[1].has_attr("rowspan"):
                current_collection = (
                    cells[1].a.text if cells[1].a else current_collection
                )
            elif (
                len(cells) > 1 and cells[1].a
            ):  # Update collection if directly provided
                current_collection = cells[1].a.text

            # Extract data
            skin_image = cells[0].a["href"] if cells[0].a else ""
            skin_name = cells[2].get_text(strip=True)
            skin_cost = (
                cells[3]
                .get_text(strip=True)
                .split(";")[-1]
                .replace("\xa0", "")
                .replace(",", "")
            )
            skin_weapon = "Melee"

            # Append data with the current collection
            csv_data.append(
                [skin_image, current_collection, skin_name, skin_cost, skin_weapon]
            )
    else:
        headers = [
            "Skin Image",
            "Skin Name",
            "Skin Edition",
            "Skin Collection",
            "Skin Cost",
            "Skin Weapon",
        ]
        csv_data.append(headers)

        for row in rows:
            cells = row.find_all("td")
            if not cells or len(cells) < 5:
                continue

            # Extract data
            skin_image = cells[0].a["href"] if cells[0].a else ""
            skin_name = cells[0].img["alt"] if cells[0].img else ""
            skin_edition = cells[1].img["alt"] if cells[1].img else ""
            skin_collection = cells[2].a.text if cells[2].a else ""
            skin_cost = (
                cells[3]
                .get_text(strip=True)
                .split(";")[-1]
                .replace("\xa0", "")
                .replace(",", "")
            )
            skin_weapon = skin_name.split()[-1] if skin_name else ""

            # Append to CSV data
            csv_data.append(
                [
                    skin_image,
                    skin_name,
                    skin_edition,
                    skin_collection,
                    skin_cost,
                    skin_weapon,
                ]
            )

    # Save the data for the weapon to a CSV file
    csv_file_path = f"{weapon}_Skins.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print(f"Data for {weapon} saved to {csv_file_path}")
