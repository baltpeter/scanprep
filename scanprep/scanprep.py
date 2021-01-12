import argparse
import fitz
from PIL import Image, ImageFilter, ImageStat
import numpy as np
import os
import pathlib
from pyzbar.pyzbar import decode


# Algorithm inspired by: https://dsp.stackexchange.com/a/48837
def page_is_empty(img):
    threshold = np.mean(ImageStat.Stat(img).mean) - 50
    img = img.convert('L').point(lambda x: 255 if x > threshold else 0)

    # Staples, folds, punch holes et al. tend to be confined to the left and right margin, so we crop off 10% there.
    # Also, we crop off 5% at the top and bottom to get rid of the page borders.
    lr_margin = img.width * 0.10
    tb_margin = img.height * 0.05
    img = img.crop((lr_margin, tb_margin, img.width -
                    lr_margin, img.height - tb_margin))

    # Use erosion and dilation to get rid of small specks but make actual text/content more significant.
    img = img.filter(ImageFilter.MaxFilter(1))
    img = img.filter(ImageFilter.MinFilter(3))

    white_pixels = np.count_nonzero(img)
    total_pixels = img.size[0] * img.size[1]
    ratio = (total_pixels - white_pixels) / total_pixels

    return ratio < 0.005


def page_is_separator(img):
    detected_barcodes = decode(img)
    for barcode in detected_barcodes:
        if barcode.data == b'SCANPREP_SEP':
            return True
    return False


def get_new_docs_pages(doc, separate=True, remove_blank=True):
    docs = [[]]

    for page in doc:
        pixmap = page.getPixmap()
        img = Image.frombytes(
            "RGB", (pixmap.width, pixmap.height), pixmap.samples)

        if separate and page_is_separator(img):
            docs.append([])
            continue
        if remove_blank and page_is_empty(img):
            continue

        docs[-1].append(page.number)

    return list(filter(lambda d: len(d) > 0, docs))


def emit_new_documents(doc, filename, out_dir, separate=True, remove_blank=True):
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

    new_docs = get_new_docs_pages(doc, separate, remove_blank)
    for i, pages in enumerate(new_docs):
        new_doc = fitz.open()  # Will create a new, blank document.
        for j, page_no in enumerate(pages):
            new_doc.insertPDF(doc, from_page=page_no,
                              to_page=page_no, final=(j == len(pages) - 1))
        new_doc.save(os.path.join(out_dir, f"{i}-{filename}"))


# Taken from: https://stackoverflow.com/a/9236426
class ActionNoYes(argparse.Action):
    def __init__(self, opt_name, dest, default=True, required=False, help=None):
        super(ActionNoYes, self).__init__(['--' + opt_name, '--no-' + opt_name],
                                          dest, nargs=0, const=None, default=default, required=required, help=help)

    def __call__(self, p, namespace, values, option_string=None):
        if option_string.startswith('--no-'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_pdf', help='The PDF document to process.')
    parser.add_argument(
        'output_dir', help='The directory where the output documents will be saved. (defaults to the current directory)', nargs='?', default=os.getcwd())
    parser._add_action(ActionNoYes('page-separation', 'separate',
                                   help='Do (or do not) split document into separate files by the included separator pages. (default yes)'))
    parser._add_action(ActionNoYes('blank-removal', 'remove_blank',
                                   help='Do (or do not) remove empty pages from the output. (default yes)'))
    args = parser.parse_args()

    emit_new_documents(fitz.open(os.path.abspath(args.input_pdf)), os.path.basename(
        args.input_pdf), os.path.abspath(args.output_dir), args.separate, args.remove_blank)


if __name__ == '__main__':
    main()
