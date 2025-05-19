import os
import requests

folder = "faces"
os.makedirs(folder, exist_ok=True)

url = "https://thispersondoesnotexist.com"
headers = {
    "User-Agent": "Mozilla/5.0"  # Pretend to be a browser to avoid being blocked
}

for i in range(100):  # Change this to how many faces you want
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            file_path = os.path.join(folder, f"face_{i+1}.jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Image saved to: {os.path.abspath(file_path)}")
        else:
            print("Failed to fetch image.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")