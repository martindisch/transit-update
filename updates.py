def get_key():
    with open("apikey", "r") as f:
        key = f.read().strip()
    return key

if __name__ == "__main__":
    print(get_key())
