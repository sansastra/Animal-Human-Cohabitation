import requests

URL = "http://10.42.0.1:8080/post_image"
files = {'file': open('jpeg.jpeg', 'rb')}
r = requests.post(URL, files=files)
print(r.text)
