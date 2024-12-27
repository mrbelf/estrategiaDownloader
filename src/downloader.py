import requests

def download_video(url, filename):
    try:
        # Send a GET request to the video URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Open the file in binary write mode
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1 MB chunks
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def download_pdf(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download PDF. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")