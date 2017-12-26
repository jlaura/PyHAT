from libpysat.examples import get_path
from libpysat.fileio import io_ccs

def test_14_item_header_csv():
    examplefile = get_path('CL5_398645626CCS_F0030004CCAM02013P3.csv')
    io_ccs.CCAM_CSV(examplefile)
