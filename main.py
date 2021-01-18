import time
import tqdm
import argparse
import requests
import pandas as pd
from functools import partial
from multiprocessing import Pool, cpu_count
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def check_url(asset, args):
    result = asset

    # set headers
    headers = {"User-Agent": "EXAMPLE", "X-USER": "EXAMPLE"}

    try:
        response = requests.get(asset['URL'], headers=headers, verify=False, timeout=args.timeout)
    except requests.exceptions.InvalidURL as e:
        result['Status'] = "URL Error"
    except requests.exceptions.RequestException as e:
        result['Status'] = "Unavailable"
    else:
        result['Status'] = "Confirmed"
        for index, item in enumerate(response.history):
            result["URL - {index}".format(index=index)] = item.url
            result["Response Code - {index}".format(index=index)] = item.url
            if ("https" in item.url):
                result[args.keyword] = "Yes" if (args.keyword in response.headers) else "No"
            else:
                result[args.keyword] = "N/A"
            if (index == 1):
                break
        
        result['Hops'] = len(response.history)
        result['Final URL'] = response.url
        result['Final Response Code'] = response.status_code
        result['Final Header'] = "Yes" if (args.keyword in response.headers) else "No"
    finally:
        return result

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', help='File to parse through HSTS check', required=True)
    parser.add_argument('-k','--keyword', help='Keyword for the search', required=True)
    parser.add_argument('-o','--output', help='Set the output file name', default="result")
    parser.add_argument('-t','--timeout', help='Set timeout for each URL. Default is 10', type=int, default=10)
    args = parser.parse_args()

    assets = None

    if args.file.endswith("xlsx"):
        assets = pd.read_excel(args.file, header=0).to_dict('records')
    elif args.file.endswith("txt"):
        assets = []
        with open(args.file) as f:
            for line in f:
                assets.append({"URL":line.strip()})
    else:
        print("File type not supported!")
        exit(0)
    
    return (args, assets)

if __name__ == '__main__':
    args, assets = init()
    
    pool = Pool(processes=cpu_count())
    with pool as p:
        func = partial(check_url, args=args)
        results = list(tqdm.tqdm(p.imap_unordered(func, assets), total=len(assets)))
        
        filename = "{filename}-{date}.xlsx".format(filename = args.output, date = time.strftime("%Y%m%d-%H%M%S"))
        pd.DataFrame(results).to_excel(filename, header=True, index=False)
        
        print("Exported: {filename}".format(filename = filename)) 
    
    pool.close()
    pool.join()
