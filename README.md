# Split PDF to Size
Splits a PDF into multiple files, with each file being less than a specified file size.

## Requirements
The following software must be installed:
 * Python 3
   * PyMuPDF 1.18.8

The python packages can be installed using the `requirement.txt` file:  
`pip install -r requirements.txt`

## How to Use
This tool uses the command line (PowerShell, CMD, Unix).  
Only works for pdf formatted files, use `-f` to specify the input file.  
Basic command:  
`python3 split_pdf_to_size.py -f path/to/file.pdf`

The default size that split pdf files will have at most is 20 mb.  
The size can be set between 1 and 25 mb using `-s`:  
`python3 split_pdf_to_size.py -f path/to/file.pdf -s 5`

## How it Works
This script uses a divide and conquer strategy.  
When the input file is within the size limit, nothing happens.  
Otherwise the input file is split in half.  
The file is split in half, as in the pages in the pdf.  
It could be that the first half is less data heavy than the second half.  
Thus the split files are checked on the file size.  
A similar process as before happens until all split files are beneath the specified size limit.

It could be that a file can not be split into a size smaller than the size limit.  
I.e. the data on a single page in the pdf is too large.  
An error will be shown in those cases.  
The generated files will still be available in that scenario.

## License
MIT License