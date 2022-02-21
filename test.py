import base64


with open("a.png", "rb") as image:
    b = base64.b64encode(image.read())
    print(b)
