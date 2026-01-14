import base64
# Run this on your laptop where token.pickle exists
with open("token.pickle", "rb") as f:
    print(base64.b64encode(f.read()).decode("utf-8"))