import requests
import cs50

def main():
    string = cs50.get_string("Request: ")
    response = requests.get(string)
    print("Code: "+ str(response.status_code))

main()