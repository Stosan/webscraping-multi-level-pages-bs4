import re
import requests
from bs4 import BeautifulSoup
from load import save_to_db



def regex_slash(string):
    """
    Modifies a URL by replacing the second slash with "/radios/play/".
    
    Args:
        string (str): Input URL.
        
    Returns:
        str: Modified URL.
    """
    pattern = r"/([^/]+)"
    match = re.search(pattern, string)
    if match:
        second_slash = match.start()
        new_string = string[:second_slash] + "/radios/play/" + string[second_slash + 8:]
        return new_string

def get_streamurl(link_to_streamurl):
    """
    Retrieves the stream URL for a radio station.

    Args:
        link_to_streamurl (str): URL of the radio station.

    Returns:
        str: Stream URL of the radio station.
    """
    strm_url = "https://streema.com" + regex_slash(link_to_streamurl)
    response = requests.get(strm_url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    audio_tag = soup.find(class_='vjs-tech')
    # src_value = audio_tag['src']
    # print(src_value)
    return ""

def main():
    """
    Main function to scrape radio station data and save to results.txt.
    """
    # URL of the webpage to scrape
    url = 'https://streema.com/radios/Lagos_2'

    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract radio station data
    radio_stations = []
    radio_elements = soup.find_all("div", class_="item")

    for element in radio_elements:
        name = element.find('div', class_='item-name').a.text
        frequency = element.find('p', class_='band-dial').text
        stream_url = get_streamurl(element.find('div', class_='item-name').a['href'])
        radio_stations.append({
            'name': name,
            'stream_url': stream_url,
            'frequency': frequency
        })
    # Save radio station data to postgresql db
    save_to_db(radio_stations)

    # Save radio station data to results.txt
    with open('results.txt', 'w') as file:
        for station in radio_stations:
            file.write(f"Name: {station['name']}\n")
            file.write(f"Stream URL: {station['stream_url']}\n")
            file.write(f"Frequency: {station['frequency']}\n\n")

if __name__ == "__main__":
    main()