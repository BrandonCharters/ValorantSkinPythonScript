from bs4 import BeautifulSoup
import csv

# The HTML content with multiple tables
html_content = """

"""

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all tables in the HTML
tables = soup.select('table.wikitable')

# Process each table individually
for table in tables:
    # Find all rows in the current table
    rows = table.select('tbody tr')
    
    # Prepare the CSV data for this table
    csv_data = []
    headers = ["Skin Image", "Skin Name", "Skin Edition", "Skin Collection", "Skin Cost", "Skin Weapon"]
    csv_data.append(headers)
    
    # Extract data from each row
    for row in rows:
        cells = row.find_all('td')
        if not cells or len(cells) < 5:
            continue
        
        # Extract data
        skin_image = cells[0].a['href'] if cells[0].a else ''
        skin_name = cells[0].img['alt'] if cells[0].img else ''
        skin_edition = cells[1].img['alt'] if cells[1].img else ''
        skin_collection = cells[2].a.text if cells[2].a else ''
        skin_cost = cells[3].get_text(strip=True).split(';')[-1].replace('\xa0', '').replace(',', '')
        
        # Derive Skin Weapon from the Skin Name (e.g., "Classic" from "Avalanche Classic")
        skin_weapon = skin_name.split()[-1] if skin_name else ''
        
        # Append to CSV data
        csv_data.append([skin_image, skin_name, skin_edition, skin_collection, skin_cost, skin_weapon])
    
    # Determine the file name based on the weapon's name
    weapon_skin_name = skin_weapon if skin_weapon else "Unknown_Weapon"  # Fallback if no weapon name
    csv_file_path = f"{weapon_skin_name.replace(' ', '_')}_Data.csv"
    
    # Save to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    
    print(f"CSV file saved as {csv_file_path}")
