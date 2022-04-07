import sys
import json
import base64
import requests

# Define API URL and SPK filename:
url = 'https://ssd.jpl.nasa.gov/api/horizons_file.api'
spk_filename = 'spk_file.bsp'
file = 'documents/GitHib/SpaceLaser/input.txt'

# Get the Horizons API input file from the command-line:
try:
    f = open(file)
except OSError as err:
  print("Unable to open input file '{0}': {1}".format(file, err))

# Build and submit the API request and decode the JSON-response:
response = requests.post(url, data={'format':'json'}, files={'input': f})
f.close()
try:
  data = json.loads(response.text)
except ValueError:
  print("Unable to decode JSON results")

# If the request was valid...
if (response.status_code == 200):
  #
  # If the SPK file was generated, decode it and write it to the output file:
  if "spk" in data:
    #
    # If a suggested SPK file basename was provided, use it:
    if "spk_file_id" in data:
      spk_filename = data["spk_file_id"] + ".bsp"
    try:
      f = open(spk_filename, "wb")
    except OSError as err:
      print("Unable to open SPK file '{0}': {1}".format(spk_filename, err))
    #
    # Decode and write the binary SPK file content:
    f.write(base64.b64decode(data["spk"]))
    f.close()
    print("wrote SPK content to {0}".format(spk_filename))
    sys.exit()
  #
  # Otherwise, the SPK file was not generated so output an error:
  print("ERROR: SPK file not generated")
  if "result" in data:
    print(data["result"])
  else:
    print(response.text)
  sys.exit(1)

# If the request was invalid, extract error content and display it:
if (response.status_code == 400):
  data = json.loads(response.text)
  if "message" in data:
    print("MESSAGE: {}".format(data["message"]))
  else:
    print(json.dumps(data, indent=2))

# Otherwise, some other error occurred:
print("response code: {0}".format(response.status_code))
sys.exit(2)
