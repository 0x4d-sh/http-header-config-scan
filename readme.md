# HTTP-header Config Scan
Using multiprocessing to perform mass HTTP-header configuration scan of the network using input from excel or text file.

The output will be in `.xlsx` file format.

# Pre-requisite
- Python 3 and libraries
- File (.xlsx/.txt) that contain list of domain-names to be scanned

For `.xlsx`, the script will read the first row of the excel as the column header and header with `URL` will be used for the scan.
For `.txt`, the script will read the domains/urls in rows, for example, please reference to `hosts.txt`

## Usage
Run `python3 main.py -f <input filie in .xlsx/.txt> -k <http header> -t <timeout> -o <output prefix>`

![Default Mode Gif](example/example.gif "Network Config Scan")
