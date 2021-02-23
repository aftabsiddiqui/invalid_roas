import urllib, json
import urllib.request
import datetime

ripe_url = "https://stat.ripe.net/data/rpki-validation/data.json?resource={}&prefix={}"


def roa(resource, prefix):
    fetch_url = ripe_url.format(resource, prefix)
    fetch_req = urllib.request.Request(fetch_url)
    response = urllib.request.urlopen(fetch_req)
    data_string = response.read()
    response_data = json.loads(data_string)
    status = response_data["data"]["status"]
    return status


url = "https://bgpstuff.net/invalids"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'curl/7.64.1')
# req.add_header('Accept', '*/*')
req.add_header('content-type', 'application/json')
response = urllib.request.urlopen(req)
data_string = response.read()
response_data = json.loads(data_string)
current_time = datetime.datetime.now().date()
output_events = []
invalids = response_data["Response"]["Invalids"]
if len(invalids) == 0:
    print("No Invalids Found")
else:
    for test in invalids:
        file_name = "invalid_{}.txt".format(current_time)
        for prefix in test["Prefixes"]:
            status=roa(test["ASN"], prefix)
            with open(file_name, mode='a') as csv_file:
                csv_file.write(test["ASN"] + " " + prefix + " " + status)
                csv_file.write("\n")

