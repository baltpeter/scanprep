# scanprep – Prepare scanned PDF documents

> Small utility to prepare scanned documents. Supports separating PDF files by separator pages and removing blank pages.

<!-- TODO: GIF showing how to use scanprep -->

Scanprep can be used to prepare scanned documents for further processing with existing tools (like the great [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF)) or directly for archival. It allows splitting multiple documents that were scanned in a single batch into multiple files. In addition, it can also remove blank pages from the output (this is especially helpful if using a duplex scanner).

For document separation, separator pages need to be inserted between the different documents before scanning. These pages tell the program where to split. You can either use the [included separator page](/separator-page.pdf) or create your own. The separator page simply needs to have a barcode that encodes the text `SCANPREP_SEP` (you can use any [barcode type supported by zbar](http://zbar.sourceforge.net/about.html)).

## Installation

### From source

To install scanprep from source, simply clone this repository and install the dependencies:

```sh
git clone https://github.com/baltpeter/scanprep.git
cd scanprep
pip install -r requirements.txt # You may want to do this in a venv.
# You may also need to install the zbar shared library. See: https://pypi.org/project/pyzbar/

python3 scanprep.py -h
```

## Usage

```
usage: scanprep.py [-h] [--page-separation] [--blank-removal] input_pdf [output_dir]

positional arguments:
  input_pdf             The PDF document to process.
  output_dir            The directory where the output documents will be saved. (defaults to the
                        current directory)

optional arguments:
  -h, --help            show this help message and exit
  --page-separation, --no-page-separation
                        Do (or do not) split document into separate files by the included
                        separator pages. (default yes)
  --blank-removal, --no-blank-removal
                        Do (or do not) remove empty pages from the output. (default yes)
```

## License

Scanprep is licensed under the MIT license, see the `LICENSE` file for details. Issues and pull requests are welcome!