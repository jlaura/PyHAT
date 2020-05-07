import pandas as pd
from libpyhat.examples import get_path
import libpyhat.utils.lookup as lookup

def test_lookup():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    result = lookup.lookup(df, lookupfile=[get_path('lookup.csv'),get_path('lookup2.csv')], skiprows=0, left_on='LIBS ID', right_on='LIBS ID')
    assert result[('meta', 'foo')][result[('meta', 'LIBS ID')] == 'LIB00053'].values[0] == 'k'
    assert result[('meta', 'foo')][result[('meta', 'LIBS ID')] == 'LIB00140'].values[0] == 'e'

test_lookup()