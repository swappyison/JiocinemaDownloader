import requests

# Function to fetch and print episode URLs
def fetch_and_print_episode_urls(api_url):
    url = f"https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/{api_url}&responseType=common"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        episodes = data.get("result", [])

        if episodes:
            for episode in episodes:
                url_structure_new = episode.get("seo", {}).get("urlStructureNew")
                if url_structure_new:
                    print(url_structure_new)
                else:
                    print("urlStructureNew not found for an episode.")
        else:
            print("No episodes found in the response.")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

# Ask the user for the show ID
show_id = input("Enter the show ID: ")

# URL to fetch the JSON data from
show_url = f"https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/view/show/{show_id}?&responseType=common&features=include:buttonsTray&premiumTrays=false&devicePlatformType=desktop"

# Send an HTTP GET request to the show URL
show_response = requests.get(show_url)

# Check if the request was successful (status code 200)
if show_response.status_code == 200:
    # Parse the JSON response for the show
    show_data = show_response.json()

    # Extract the 'id' values from 'trayTabs'
    tray_tabs_ids = [tab['id'] for tray in show_data.get('trays', []) for tab in tray.get('trayTabs', [])]

    # Sending GET requests to the specified URL for each 'id' value
    for id_value in tray_tabs_ids:
        # Initialize page number and flag
        page = 1
        has_more_pages = True

        while has_more_pages:
            episode_url = f"https://content-jiovoot.voot.com/psapi/voot/v1/voot-web/content/generic/series-wise-episode?sort=episode:asc&id={id_value}&responseType=common&page={page}"
            episode_response = requests.get(episode_url)

            # Check if the request was successful (status code 200) for episode data
            if episode_response.status_code == 200:
                episode_data = episode_response.json()
                episodes = episode_data.get('result', [])

                if episodes:
                    for episode in episodes:
                        url_structure_new = episode.get('seo', {}).get('urlStructureNew')
                        if url_structure_new:
                            print(url_structure_new)
                        else:
                            print("urlStructureNew not found for an episode.")
                    
                    # Check if there are more pages to fetch
                    if len(episodes) < 10:
                        has_more_pages = False
                    else:
                        page += 1  # Move to the next page
                else:
                    # No more episodes found
                    has_more_pages = False
            else:
                print(f"Failed to retrieve episode data for ID {id_value}, Page {page}. Status code: {episode_response.status_code}")
                has_more_pages = False
else:
    print(f"Failed to retrieve show data. Status code: {show_response.status_code}")

with open("episode_url.txt", "w") as output_file:
    # ... (rest of your code)

    # Instead of printing, write the URLs to the file
    if url_structure_new:
        output_file.write(url_structure_new + "\n")
    else:
        output_file.write("urlStructureNew not found for an episode.\n")
