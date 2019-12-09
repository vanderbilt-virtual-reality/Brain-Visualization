import bz2
import os
import zlib
from collections import OrderedDict
from datetime import datetime
import re
import warnings
import numpy as np

def format_number(x):
    """Format number to string

    Function converts a number to string. For numbers of class :class:`float`, up to 17 digits will be used to print
    the entire floating point number. Any padding zeros will be removed at the end of the number.

    See :ref:`user-guide:int` and :ref:`user-guide:double` for more information on the format.

    .. note::
            IEEE754-1985 standard says that 17 significant decimal digits are required to adequately represent a
            64-bit floating point number. Not all fractional numbers can be exactly represented in floating point. An
            example is 0.1 which will be approximated as 0.10000000000000001.

    Parameters
    ----------
    x : :class:`int` or :class:`float`
        Number to convert to string

    Returns
    -------
    vector : :class:`str`
        String of number :obj:`x`
    """

    if isinstance(x, float):
        # Helps prevent loss of precision as using str() in Python 2 only prints 12 digits of precision.
        # However, IEEE754-1985 standard says that 17 significant decimal digits is required to adequately represent a
        # floating point number.
        # The g option is used rather than f because g precision uses significant digits while f is just the number of
        # digits after the decimal. (NRRD C implementation uses g).
        value = '{:.17g}'.format(x)
    else:
        value = str(x)

    return value


def format_vector(x):
    """Format a (N,) :class:`numpy.ndarray` into a NRRD vector string

    See :ref:`user-guide:int vector` and :ref:`user-guide:double vector` for more information on the format.

    Parameters
    ----------
    x : (N,) :class:`numpy.ndarray`
        Vector to convert to NRRD vector string

    Returns
    -------
    vector : :class:`str`
        String containing NRRD vector
    """

    return '(' + ','.join([format_number(y) for y in x]) + ')'


def format_optional_vector(x):
    """Format a (N,) :class:`numpy.ndarray` into a NRRD optional vector string

    Function converts a (N,) :class:`numpy.ndarray` or :obj:`None` into a string using NRRD vector format. If the input
    :obj:`x` is :obj:`None`, then :obj:`vector` will be 'none'

    See :ref:`user-guide:int vector` and :ref:`user-guide:double vector` for more information on the format.

    Parameters
    ----------
    x : (N,) :class:`numpy.ndarray` or :obj:`None`
        Vector to convert to NRRD vector string

    Returns
    -------
    vector : :class:`str`
        String containing NRRD vector
    """

    # If vector is None or all elements are NaN, then return none
    # Otherwise format the vector as normal
    if x is None or np.all(np.isnan(x)):
        return 'none'
    else:
        return format_vector(x)


def format_matrix(x):
    """Format a (M,N) :class:`numpy.ndarray` into a NRRD matrix string

    See :ref:`user-guide:int matrix` and :ref:`user-guide:double matrix` for more information on the format.

    Parameters
    ----------
    x : (M,N) :class:`numpy.ndarray`
        Matrix to convert to NRRD vector string

    Returns
    -------
    matrix : :class:`str`
        String containing NRRD matrix
    """

    return ' '.join([format_vector(y) for y in x])


def format_optional_matrix(x):
    """Format a (M,N) :class:`numpy.ndarray` of :class:`float` into a NRRD optional matrix string

    Function converts a (M,N) :class:`numpy.ndarray` of :class:`float` into a string using the NRRD matrix format. For
    any rows of the matrix that contain all NaNs for each element, the row will be replaced with a 'none' indicating
    the row has no vector.

    See :ref:`user-guide:double matrix` for more information on the format.

    .. note::
            :obj:`x` must have a datatype of float because NaN's are only defined for floating point numbers.

    Parameters
    ----------
    x : (M,N) :class:`numpy.ndarray` of :class:`float`
        Matrix to convert to NRRD vector string

    Returns
    -------
    matrix : :class:`str`
        String containing NRRD matrix
    """

    return ' '.join([format_optional_vector(y) for y in x])


def format_number_list(x):
    """Format a (N,) :class:`numpy.ndarray` into a NRRD number list.

    See :ref:`user-guide:int list` and :ref:`user-guide:double list` for more information on the format.

    Parameters
    ----------
    x : (N,) :class:`numpy.ndarray`
        Vector to convert to NRRD number list string

    Returns
    -------
    list : :class:`str`
        String containing NRRD list
    """

    return ' '.join([format_number(y) for y in x])
def parse_vector(x, dtype=None):
    """Parse NRRD vector from string into (N,) :class:`numpy.ndarray`.

    See :ref:`user-guide:int vector` and :ref:`user-guide:double vector` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String containing NRRD vector
    dtype : data-type, optional
        Datatype to use for the resulting Numpy array. Datatype can be :class:`float`, :class:`int` or :obj:`None`. If
        :obj:`dtype` is :obj:`None`, then it will be automatically determined by checking any of the vector elements
        for fractional numbers. If found, then the vector will be converted to :class:`float`, otherwise :class:`int`.
        Default is to automatically determine datatype.

    Returns
    -------
    vector : (N,) :class:`numpy.ndarray`
        Vector that is parsed from the :obj:`x` string
    """

    if x[0] != '(' or x[-1] != ')':
        raise NRRDError('Vector should be enclosed by parentheses.')

    # Always convert to float and then truncate to integer if desired
    # The reason why is parsing a floating point string to int will fail (i.e. int('25.1') will fail)
    vector = np.array([float(x) for x in x[1:-1].split(',')])

    # If using automatic datatype detection, then start by converting to float and determining if the number is whole
    # Truncate to integer if dtype is int also
    if dtype is None:
        vector_trunc = vector.astype(int)

        if np.all((vector - vector_trunc) == 0):
            vector = vector_trunc
    elif dtype == int:
        vector = vector.astype(int)
    elif dtype != float:
        raise NRRDError('dtype should be None for automatic type detection, float or int')

    return vector


def parse_optional_vector(x, dtype=None):
    """Parse optional NRRD vector from string into (N,) :class:`numpy.ndarray` or :obj:`None`.

    Function parses optional NRRD vector from string into an (N,) :class:`numpy.ndarray`. This function works the same
    as :meth:`parse_vector` except if :obj:`x` is 'none', :obj:`vector` will be :obj:`None`

    See :ref:`user-guide:int vector` and :ref:`user-guide:double vector` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String containing NRRD vector or 'none'
    dtype : data-type, optional
        Datatype to use for the resulting Numpy array. Datatype can be :class:`float`, :class:`int` or :obj:`None`. If
        :obj:`dtype` is :obj:`None`, then it will be automatically determined by checking any of the vector elements
        for fractional numbers. If found, then the vector will be converted to :class:`float`, otherwise :class:`int`.
        Default is to automatically determine datatype.

    Returns
    -------
    vector : (N,) :class:`numpy.ndarray` or :obj:`None`
        Vector that is parsed from the :obj:`x` string or :obj:`None` if :obj:`x` is 'none'
    """

    if x == 'none':
        return None
    else:
        return parse_vector(x, dtype)


def parse_matrix(x, dtype=None):
    """Parse NRRD matrix from string into (M,N) :class:`numpy.ndarray`.

    See :ref:`user-guide:int matrix` and :ref:`user-guide:double matrix` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String containing NRRD matrix
    dtype : data-type, optional
        Datatype to use for the resulting Numpy array. Datatype can be :class:`float`, :class:`int` or :obj:`None`. If
        :obj:`dtype` is :obj:`None`, then it will be automatically determined by checking any of the elements
        for fractional numbers. If found, then the matrix will be converted to :class:`float`, otherwise :class:`int`.
        Default is to automatically determine datatype.

    Returns
    -------
    matrix : (M,N) :class:`numpy.ndarray`
        Matrix that is parsed from the :obj:`x` string
    """

    # Split input by spaces, convert each row into a vector and stack them vertically to get a matrix
    matrix = [parse_vector(x, dtype=float) for x in x.split()]

    # Get the size of each row vector and then remove duplicate sizes
    # There should be exactly one value in the matrix because all row sizes need to be the same
    if len(np.unique([len(x) for x in matrix])) != 1:
        raise NRRDError('Matrix should have same number of elements in each row')

    matrix = np.vstack(matrix)

    # If using automatic datatype detection, then start by converting to float and determining if the number is whole
    # Truncate to integer if dtype is int also
    if dtype is None:
        matrix_trunc = matrix.astype(int)

        if np.all((matrix - matrix_trunc) == 0):
            matrix = matrix_trunc
    elif dtype == int:
        matrix = matrix.astype(int)
    elif dtype != float:
        raise NRRDError('dtype should be None for automatic type detection, float or int')

    return matrix


def parse_optional_matrix(x):
    """Parse optional NRRD matrix from string into (M,N) :class:`numpy.ndarray` of :class:`float`.

    Function parses optional NRRD matrix from string into an (M,N) :class:`numpy.ndarray` of :class:`float`. This
    function works the same as :meth:`parse_matrix` except if a row vector in the matrix is none, the resulting row in
    the returned matrix will be all NaNs.

    See :ref:`user-guide:double matrix` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String containing NRRD matrix

    Returns
    -------
    matrix : (M,N) :class:`numpy.ndarray` of :class:`float`
        Matrix that is parsed from the :obj:`x` string
    """

    # Split input by spaces to get each row and convert into a vector. The row can be 'none', in which case it will
    # return None
    matrix = [parse_optional_vector(x, dtype=float) for x in x.split()]

    # Get the size of each row vector, 0 if None
    sizes = np.array([0 if x is None else len(x) for x in matrix])

    # Get sizes of each row vector removing duplicate sizes
    # Since each row vector should be same size, the unique sizes should return one value for the row size or it may
    # return a second one (0) if there are None vectors
    unique_sizes = np.unique(sizes)

    if len(unique_sizes) != 1 and (len(unique_sizes) != 2 or unique_sizes.min() != 0):
        raise NRRDError('Matrix should have same number of elements in each row')

    # Create a vector row of NaN's that matches same size of remaining vector rows
    # Stack the vector rows together to create matrix
    nan_row = np.full((unique_sizes.max()), np.nan)
    matrix = np.vstack([nan_row if x is None else x for x in matrix])

    return matrix


def parse_number_list(x, dtype=None):
    """Parse NRRD number list from string into (N,) :class:`numpy.ndarray`.

    See :ref:`user-guide:int list` and :ref:`user-guide:double list` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String containing NRRD number list
    dtype : data-type, optional
        Datatype to use for the resulting Numpy array. Datatype can be :class:`float`, :class:`int` or :obj:`None`. If
        :obj:`dtype` is :obj:`None`, then it will be automatically determined by checking for fractional numbers. If
        found, then the string will be converted to :class:`float`, otherwise :class:`int`. Default is to automatically
        determine datatype.

    Returns
    -------
    vector : (N,) :class:`numpy.ndarray`
        Vector that is parsed from the :obj:`x` string
    """

    # Always convert to float and then perform truncation to integer if necessary
    number_list = np.array([float(x) for x in x.split()])

    if dtype is None:
        number_list_trunc = number_list.astype(int)

        # If there is no difference between the truncated number list and the number list, then that means that the
        # number list was all integers and we can just return that
        if np.all((number_list - number_list_trunc) == 0):
            number_list = number_list_trunc
    elif dtype == int:
        number_list = number_list.astype(int)
    elif dtype != float:
        raise NRRDError('dtype should be None for automatic type detection, float or int')

    return number_list


def parse_number_auto_dtype(x):
    """Parse number from string with automatic type detection.

    Parses input string and converts to a number using automatic type detection. If the number contains any
    fractional parts, then the number will be converted to float, otherwise the number will be converted to an int.

    See :ref:`user-guide:int` and :ref:`user-guide:double` for more information on the format.

    Parameters
    ----------
    x : :class:`str`
        String representation of number

    Returns
    -------
    result : :class:`int` or :class:`float`
        Number parsed from :obj:`x` string
    """

    value = float(x)

    if value.is_integer():
        value = int(value)

    return value
    
    
# Older versions of Python had issues when uncompressed data was larger than 4GB (2^32). This should be fixed in latest
# version of Python 2.7 and all versions of Python 3. The fix for this issue is to read the data in smaller chunks.
# Chunk size is set to be large at 1GB to improve performance. If issues arise decompressing larger files, try to reduce
# this value
_READ_CHUNKSIZE = 2 ** 32

_NRRD_REQUIRED_FIELDS = ['dimension', 'type', 'encoding', 'sizes']

ALLOW_DUPLICATE_FIELD = False
"""Allow duplicate header fields when reading NRRD files

When there are duplicated fields in a NRRD file header, pynrrd throws an error by default. Setting this field as 
:obj:`True` will instead show a warning.

Example:
    Reading a NRRD file with duplicated header field 'space' with field set to :obj:`False`.

    >>> filedata, fileheader = nrrd.read('filename_duplicatedheader.nrrd')
    nrrd.errors.NRRDError: Duplicate header field: 'space'

    Set the field as :obj:`True` to receive a warning instead.

    >>> nrrd.reader.ALLOW_DUPLICATE_FIELD = True
    >>> filedata, fileheader = nrrd.read('filename_duplicatedheader.nrrd')
    UserWarning: Duplicate header field: 'space' warnings.warn(dup_message)

Note:
    Duplicated fields are prohibited by the NRRD file specification.
"""

_TYPEMAP_NRRD2NUMPY = {
    'signed char': 'i1',
    'int8': 'i1',
    'int8_t': 'i1',
    'uchar': 'u1',
    'unsigned char': 'u1',
    'uint8': 'u1',
    'uint8_t': 'u1',
    'short': 'i2',
    'short int': 'i2',
    'signed short': 'i2',
    'signed short int': 'i2',
    'int16': 'i2',
    'int16_t': 'i2',
    'ushort': 'u2',
    'unsigned short': 'u2',
    'unsigned short int': 'u2',
    'uint16': 'u2',
    'uint16_t': 'u2',
    'int': 'i4',
    'signed int': 'i4',
    'int32': 'i4',
    'int32_t': 'i4',
    'uint': 'u4',
    'unsigned int': 'u4',
    'uint32': 'u4',
    'uint32_t': 'u4',
    'longlong': 'i8',
    'long long': 'i8',
    'long long int': 'i8',
    'signed long long': 'i8',
    'signed long long int': 'i8',
    'int64': 'i8',
    'int64_t': 'i8',
    'ulonglong': 'u8',
    'unsigned long long': 'u8',
    'unsigned long long int': 'u8',
    'uint64': 'u8',
    'uint64_t': 'u8',
    'float': 'f4',
    'double': 'f8',
    'block': 'V'
}


def _get_field_type(field, custom_field_map):
    if field in ['dimension', 'lineskip', 'line skip', 'byteskip', 'byte skip', 'space dimension']:
        return 'int'
    elif field in ['min', 'max', 'oldmin', 'old min', 'oldmax', 'old max']:
        return 'double'
    elif field in ['endian', 'encoding', 'content', 'sample units', 'datafile', 'data file', 'space', 'type']:
        return 'string'
    elif field in ['sizes']:
        return 'int list'
    elif field in ['spacings', 'thicknesses', 'axismins', 'axis mins', 'axismaxs', 'axis maxs']:
        return 'double list'
    elif field in ['kinds', 'labels', 'units', 'space units', 'centerings']:
        return 'string list'
    # No int vector fields as of now
    # elif field in []:
    #     return 'int vector'
    elif field in ['space origin']:
        return 'double vector'
    elif field in ['measurement frame']:
        return 'double matrix'
    elif field in ['space directions']:
        return 'double matrix'
    else:
        if custom_field_map and field in custom_field_map:
            return custom_field_map[field]

        # Default the type to string if unknown type
        return 'string'


def _parse_field_value(value, field_type):
    if field_type == 'int':
        return int(value)
    elif field_type == 'double':
        return float(value)
    elif field_type == 'string':
        return str(value)
    elif field_type == 'int list':
        return parse_number_list(value, dtype=int)
    elif field_type == 'double list':
        return parse_number_list(value, dtype=float)
    elif field_type == 'string list':
        # TODO Handle cases where quotation marks are around the items
        return [str(x) for x in value.split()]
    elif field_type == 'int vector':
        return parse_vector(value, dtype=int)
    elif field_type == 'double vector':
        return parse_vector(value, dtype=float)
    elif field_type == 'int matrix':
        return parse_matrix(value, dtype=int)
    elif field_type == 'double matrix':
        # For matrices of double type, parse as an optional matrix to allow for rows of the matrix to be none
        # This is only valid for double matrices because the matrix is represented with NaN in the entire row
        # for none rows. NaN is only valid for floating point numbers
        return parse_optional_matrix(value)
    else:
        raise NRRDError('Invalid field type given: %s' % field_type)


def _determine_datatype(fields):
    """Determine the numpy dtype of the data."""

    # Convert the NRRD type string identifier into a NumPy string identifier using a map
    np_typestring = _TYPEMAP_NRRD2NUMPY[fields['type']]

    # This is only added if the datatype has more than one byte and is not using ASCII encoding
    # Note: Endian is not required for ASCII encoding
    if np.dtype(np_typestring).itemsize > 1 and fields['encoding'] not in ['ASCII', 'ascii', 'text', 'txt']:
        if 'endian' not in fields:
            raise NRRDError('Header is missing required field: "endian".')
        elif fields['endian'] == 'big':
            np_typestring = '>' + np_typestring
        elif fields['endian'] == 'little':
            np_typestring = '<' + np_typestring
        else:
            raise NRRDError('Invalid endian value in header: "%s"' % fields['endian'])

    return np.dtype(np_typestring)


def _validate_magic_line(line):
    """For NRRD files, the first four characters are always "NRRD", and
    remaining characters give information about the file format version

    >>> _validate_magic_line('NRRD0005')
    8
    >>> _validate_magic_line('NRRD0006')
    Traceback (most recent call last):
        ...
    NrrdError: NRRD file version too new for this library.
    >>> _validate_magic_line('NRRD')
    Traceback (most recent call last):
        ...
    NrrdError: Invalid NRRD magic line: NRRD
    """

    if not line.startswith('NRRD'):
        raise NRRDError('Invalid NRRD magic line. Is this an NRRD file?')

    try:
        version = int(line[4:])
        if version > 5:
            raise NRRDError('Unsupported NRRD file version (version: %i). This library only supports v%i and below.'
                            % (version, 5))
    except ValueError:
        raise NRRDError('Invalid NRRD magic line: %s' % line)

    return len(line)


def read_header(file, custom_field_map=None):
    """Read contents of header and parse values from :obj:`file`

    :obj:`file` can be a filename indicating where the NRRD header is located or a string iterator object. If a
    filename is specified, then the file will be opened and closed after the header is read from it. If not specifying
    a filename, the :obj:`file` parameter can be any sort of iterator that returns a string each time :meth:`next` is
    called. The two common objects that meet these requirements are file objects and a list of strings. When
    :obj:`file` is a file object, it must be opened with the binary flag ('b') on platforms where that makes a
    difference, such as Windows.

    See :ref:`user-guide:Reading NRRD files` for more information on reading NRRD files.

    Parameters
    ----------
    file : :class:`str` or string iterator
        Filename, file object or string iterator object to read NRRD header from
    custom_field_map : :class:`dict` (:class:`str`, :class:`str`), optional
        Dictionary used for parsing custom field types where the key is the custom field name and the value is a
        string identifying datatype for the custom field.

    Returns
    -------
    header : :class:`dict` (:class:`str`, :obj:`Object`)
        Dictionary containing the header fields and their corresponding parsed value

    See Also
    --------
    :meth:`read`, :meth:`read_data`
    """

    # If the file is a filename rather than the file handle, then open the file and call this function again with the
    # file handle. Since read function uses a filename, it is easy to think read_header is the same syntax.
    if isinstance(file, str) and file.count('\n') == 0:
        with open(file, 'rb') as fh:
            header = read_header(fh, custom_field_map)
            return header

    # Collect number of bytes in the file header (for seeking below)
    header_size = 0

    # Get iterator for the file and extract the first line, the magic line
    it = iter(file)
    magic_line = next(it)

    # Depending on what type file is, decoding may or may not be necessary. Decode if necessary, otherwise skip.
    need_decode = False
    if hasattr(magic_line, 'decode'):
        need_decode = True
        magic_line = magic_line.decode('ascii', 'ignore')

    # Validate the magic line and increment header size by size of the line
    header_size += _validate_magic_line(magic_line)

    # Create empty header
    # This is an OrderedDict rather than an ordinary dict because an OrderedDict will keep it's order that key/values
    # are added for when looping back through it. The added benefit of this is that saving the header will save the
    # fields in the same order.
    header = OrderedDict()

    # Loop through each line
    for line in it:
        header_size += len(line)
        if need_decode:
            line = line.decode('ascii', 'ignore')

        # Trailing whitespace ignored per the NRRD spec
        line = line.rstrip()

        # Skip comments starting with # (no leading whitespace is allowed)
        # Or, stop reading the header once a blank line is encountered. This separates header from data.
        if line.startswith('#'):
            continue
        elif line == '':
            break

        # Read the field and value from the line, split using regex to search for := or : delimiter
        field, value = re.split(r':=?', line, 1)

        # Remove whitespace before and after the field and value
        field, value = field.strip(), value.strip()

        # Check if the field has been added already
        if field in header.keys():
            dup_message = "Duplicate header field: '%s'" % str(field)

            if not ALLOW_DUPLICATE_FIELD:
                raise NRRDError(dup_message)

            warnings.warn(dup_message)

        # Get the datatype of the field based on it's field name and custom field map
        field_type = _get_field_type(field, custom_field_map)

        # Parse the field value using the datatype retrieved
        # Place it in the header dictionary
        header[field] = _parse_field_value(value, field_type)

    # Reading the file line by line is buffered and so the header is not in the correct position for reading data if
    # the file contains the data in it as well. The solution is to set the file pointer to just behind the header.
    if hasattr(file, 'seek'):
        file.seek(header_size)

    return header


def read_data(header, fh=None, filename=None, index_order='F'):
    """Read data from file into :class:`numpy.ndarray`

    The two parameters :obj:`fh` and :obj:`filename` are optional depending on the parameters but it never hurts to
    specify both. The file handle (:obj:`fh`) is necessary if the header is attached with the NRRD data. However, if
    the NRRD data is detached from the header, then the :obj:`filename` parameter is required to obtain the absolute
    path to the data file.

    See :ref:`user-guide:Reading NRRD files` for more information on reading NRRD files.

    Parameters
    ----------
    header : :class:`dict` (:class:`str`, :obj:`Object`)
        Parsed fields/values obtained from :meth:`read_header` function
    fh : file-object, optional
        File object pointing to first byte of data. Only necessary if data is attached to header.
    filename : :class:`str`, optional
        Filename of the header file. Only necessary if data is detached from the header. This is used to get the
        absolute data path.
    index_order : {'C', 'F'}, optional
        Specifies the index order of the resulting data array. Either 'C' (C-order) where the dimensions are ordered from
        slowest-varying to fastest-varying (e.g. (z, y, x)), or 'F' (Fortran-order) where the dimensions are ordered
        from fastest-varying to slowest-varying (e.g. (x, y, z)).

    Returns
    -------
    data : :class:`numpy.ndarray`
        Data read from NRRD file

    See Also
    --------
    :meth:`read`, :meth:`read_header`
    """

    if index_order not in ['F', 'C']:
        raise NRRDError('Invalid index order')

    # Check that the required fields are in the header
    for field in _NRRD_REQUIRED_FIELDS:
        if field not in header:
            raise NRRDError('Header is missing required field: "%s".' % field)

    if header['dimension'] != len(header['sizes']):
        raise NRRDError('Number of elements in sizes does not match dimension. Dimension: %i, len(sizes): %i' % (
            header['dimension'], len(header['sizes'])))

    # Determine the data type from the header
    dtype = _determine_datatype(header)

    # Determine the byte skip, line skip and the data file
    # These all can be written with or without the space according to the NRRD spec, so we check them both
    line_skip = header.get('lineskip', header.get('line skip', 0))
    byte_skip = header.get('byteskip', header.get('byte skip', 0))
    data_filename = header.get('datafile', header.get('data file', None))

    # If the data file is separate from the header file, then open the data file to read from that instead
    if data_filename is not None:
        # If the pathname is relative, then append the current directory from the filename
        if not os.path.isabs(data_filename):
            if filename is None:
                raise NRRDError('Filename parameter must be specified when a relative data file path is given')

            data_filename = os.path.join(os.path.dirname(filename), data_filename)

        # Override the fh parameter with the data filename
        # Note that this is opened without a "with" block, thus it must be closed manually in all circumstances
        fh = open(data_filename, 'rb')

    # Get the total number of data points by multiplying the size of each dimension together
    total_data_points = header['sizes'].prod()

    # Skip the number of lines requested when line_skip >= 0
    # Irrespective of the NRRD file having attached/detached header
    # Lines are skipped before getting to the beginning of the data
    if line_skip >= 0:
        for _ in range(line_skip):
            fh.readline()
    else:
        # Must close the file because if the file was opened above from detached filename, there is no "with" block to
        # close it for us
        fh.close()

        raise NRRDError('Invalid lineskip, allowed values are greater than or equal to 0')

    # Skip the requested number of bytes or seek backward, and then parse the data using NumPy
    if byte_skip < -1:
        # Must close the file because if the file was opened above from detached filename, there is no "with" block to
        # close it for us
        fh.close()

        raise NRRDError('Invalid byteskip, allowed values are greater than or equal to -1')
    elif byte_skip >= 0:
        fh.seek(byte_skip, os.SEEK_CUR)
    elif byte_skip == -1 and header['encoding'] not in ['gzip', 'gz', 'bzip2', 'bz2']:
        fh.seek(-dtype.itemsize * total_data_points, os.SEEK_END)
    else:
        # The only case left should be: byte_skip == -1 and header['encoding'] == 'gzip'
        byte_skip = -dtype.itemsize * total_data_points

    # If a compression encoding is used, then byte skip AFTER decompressing
    if header['encoding'] == 'raw':
        data = np.fromfile(fh, dtype)
    elif header['encoding'] in ['ASCII', 'ascii', 'text', 'txt']:
        data = np.fromfile(fh, dtype, sep=' ')
    else:
        # Handle compressed data now
        # Construct the decompression object based on encoding
        if header['encoding'] in ['gzip', 'gz']:
            decompobj = zlib.decompressobj(zlib.MAX_WBITS | 16)
        elif header['encoding'] in ['bzip2', 'bz2']:
            decompobj = bz2.BZ2Decompressor()
        else:
            # Must close the file because if the file was opened above from detached filename, there is no "with" block
            # to close it for us
            fh.close()

            raise NRRDError('Unsupported encoding: "%s"' % header['encoding'])

        # Loop through the file and read a chunk at a time (see _READ_CHUNKSIZE why it is read in chunks)
        decompressed_data = bytearray()

        # Read all of the remaining data from the file
        # Obtain the length of the compressed data since we will be using it repeatedly, more efficient
        compressed_data = fh.read()
        compressed_data_len = len(compressed_data)
        start_index = 0

        # Loop through data and decompress it chunk by chunk
        while start_index < compressed_data_len:
            # Calculate the end index = start index plus chunk size
            # Set to the string length to read the remaining chunk at the end
            end_index = min(start_index + _READ_CHUNKSIZE, compressed_data_len)

            # Decompress and append data
            decompressed_data += decompobj.decompress(compressed_data[start_index:end_index])

            # Update start index
            start_index = end_index

        # Delete the compressed data since we do not need it anymore
        # This could potentially be using a lot of memory
        del compressed_data

        # Byte skip is applied AFTER the decompression. Skip first x bytes of the decompressed data and parse it using
        # NumPy
        data = np.frombuffer(decompressed_data[byte_skip:], dtype)

    # Close the file, even if opened using "with" block, closing it manually does not hurt
    fh.close()

    if total_data_points != data.size:
        raise NRRDError('Size of the data does not equal the product of all the dimensions: {0}-{1}={2}'
                        .format(total_data_points, data.size, total_data_points - data.size))

    # In the NRRD header, the fields are specified in Fortran order, i.e, the first index is the one that changes
    # fastest and last index changes slowest. This needs to be taken into consideration since numpy uses C-order
    # indexing.
    
    # The array shape from NRRD (x,y,z) needs to be reversed as numpy expects (z,y,x).
    data = np.reshape(data, tuple(header['sizes'][::-1]))

    # Transpose data to enable Fortran indexing if requested.
    if index_order == 'F':
        data = data.T

    return data


def read(filename, custom_field_map=None, index_order='F'):
    """Read a NRRD file and return the header and data

    See :ref:`user-guide:Reading NRRD files` for more information on reading NRRD files.

    .. note::
            Users should be aware that the `index_order` argument needs to be consistent between `nrrd.read` and `nrrd.write`. I.e., reading an array with `index_order='F'` will result in a transposed version of the original data and hence the writer needs to be aware of this.

    Parameters
    ----------
    filename : :class:`str`
        Filename of the NRRD file
    custom_field_map : :class:`dict` (:class:`str`, :class:`str`), optional
        Dictionary used for parsing custom field types where the key is the custom field name and the value is a
        string identifying datatype for the custom field.
    index_order : {'C', 'F'}, optional
        Specifies the index order of the resulting data array. Either 'C' (C-order) where the dimensions are ordered from
        slowest-varying to fastest-varying (e.g. (z, y, x)), or 'F' (Fortran-order) where the dimensions are ordered
        from fastest-varying to slowest-varying (e.g. (x, y, z)).

    Returns
    -------
    data : :class:`numpy.ndarray`
        Data read from NRRD file
    header : :class:`dict` (:class:`str`, :obj:`Object`)
        Dictionary containing the header fields and their corresponding parsed value

    See Also
    --------
    :meth:`write`, :meth:`read_header`, :meth:`read_data`
    """

    """Read a NRRD file and return a tuple (data, header)."""
    with open(filename, 'rb') as fh:
        header = read_header(fh, custom_field_map)
        data = read_data(header, fh, filename, index_order)

    return data, header

# Older versions of Python had issues when uncompressed data was larger than 4GB (2^32). This should be fixed in latest
# version of Python 2.7 and all versions of Python 3. The fix for this issue is to read the data in smaller chunks. The
# chunk size is set to be small here at 1MB since performance did not vary much based on the chunk size. A smaller chunk
# size has the benefit of using less RAM at once.
_WRITE_CHUNKSIZE = 2 ** 20

_NRRD_FIELD_ORDER = [
    'type',
    'dimension',
    'space dimension',
    'space',
    'sizes',
    'space directions',
    'kinds',
    'endian',
    'encoding',
    'min',
    'max',
    'oldmin',
    'old min',
    'oldmax',
    'old max',
    'content',
    'sample units',
    'spacings',
    'thicknesses',
    'axis mins',
    'axismins',
    'axis maxs',
    'axismaxs',
    'centerings',
    'labels',
    'units',
    'space units',
    'space origin',
    'measurement frame',
    'data file']

_TYPEMAP_NUMPY2NRRD = {
    'i1': 'int8',
    'u1': 'uint8',
    'i2': 'int16',
    'u2': 'uint16',
    'i4': 'int32',
    'u4': 'uint32',
    'i8': 'int64',
    'u8': 'uint64',
    'f4': 'float',
    'f8': 'double',
    'V': 'block'
}

_NUMPY2NRRD_ENDIAN_MAP = {
    '<': 'little',
    'L': 'little',
    '>': 'big',
    'B': 'big'
}


def _format_field_value(value, field_type):
    if field_type == 'int':
        return format_number(value)
    elif field_type == 'double':
        return format_number(value)
    elif field_type == 'string':
        return str(value)
    elif field_type == 'int list':
        return format_number_list(value)
    elif field_type == 'double list':
        return format_number_list(value)
    elif field_type == 'string list':
        # TODO Handle cases where the user wants quotation marks around the items
        return ' '.join(value)
    elif field_type == 'int vector':
        return format_vector(value)
    elif field_type == 'double vector':
        return format_optional_vector(value)
    elif field_type == 'int matrix':
        return format_matrix(value)
    elif field_type == 'double matrix':
        return format_optional_matrix(value)
    else:
        raise NRRDError('Invalid field type given: %s' % field_type)


def write(filename, data, header=None, detached_header=False, relative_data_path=True, custom_field_map=None,
          compression_level=9, index_order='F'):
    """Write :class:`numpy.ndarray` to NRRD file

    The :obj:`filename` parameter specifies the absolute or relative filename to write the NRRD file to. If the
    :obj:`filename` extension is .nhdr, then the :obj:`detached_header` parameter is set to true automatically. If the
    :obj:`detached_header` parameter is set to :obj:`True` and the :obj:`filename` ends in .nrrd, then the header file
    will have the same path and base name as the :obj:`filename` but with an extension of .nhdr. In all other cases,
    the header and data are saved in the same file.

    :obj:`header` is an optional parameter containing the fields and values to be added to the NRRD header.

    .. note::
            The following fields are automatically generated based on the :obj:`data` parameter ignoring these values
            in the :obj:`header`: 'type', 'endian', 'dimension', 'sizes'. In addition, the generated fields will be
            added to the given :obj:`header`. Thus, one can check the generated fields by viewing the passed
            :obj:`header`.

    .. note::
            The default encoding field used if not specified in :obj:`header` is 'gzip'.

    .. note::
            The :obj:`index_order` parameter must be consistent with the index order specified in :meth:`read`.
            Reading an NRRD file in C-order and then writing as Fortran-order or vice versa will result in the data
            being transposed in the NRRD file.

    See :ref:`user-guide:Writing NRRD files` for more information on writing NRRD files.

    Parameters
    ----------
    filename : :class:`str`
        Filename of the NRRD file
    data : :class:`numpy.ndarray`
        Data to save to the NRRD file
    detached_header : :obj:`bool`, optional
        Whether the header and data should be saved in separate files. Defaults to :obj:`False`
    relative_data_path : :class:`bool`
        Whether the data filename in detached header is saved with a relative path or absolute path.
        This parameter is ignored if there is no detached header. Defaults to :obj:`True`
    custom_field_map : :class:`dict` (:class:`str`, :class:`str`), optional
        Dictionary used for parsing custom field types where the key is the custom field name and the value is a
        string identifying datatype for the custom field.
    compression_level : :class:`int`
        Integer between 1 to 9 specifying the compression level when using a compressed encoding (gzip or bzip). A value
        of :obj:`1` compresses the data the least amount and is the fastest, while a value of :obj:`9` compresses the
        data the most and is the slowest.
    index_order : {'C', 'F'}, optional
        Specifies the index order used for writing. Either 'C' (C-order) where the dimensions are ordered from
        slowest-varying to fastest-varying (e.g. (z, y, x)), or 'F' (Fortran-order) where the dimensions are ordered
        from fastest-varying to slowest-varying (e.g. (x, y, z)).

    See Also
    --------
    :meth:`read`, :meth:`read_header`, :meth:`read_data`
    """

    if header is None:
        header = {}

    # Infer a number of fields from the NumPy array and overwrite values in the header dictionary.
    # Get type string identifier from the NumPy datatype
    header['type'] = _TYPEMAP_NUMPY2NRRD[data.dtype.str[1:]]

    # If the datatype contains more than one byte and the encoding is not ASCII, then set the endian header value
    # based on the datatype's endianness. Otherwise, delete the endian field from the header if present
    if data.dtype.itemsize > 1 and header.get('encoding', '').lower() not in ['ascii', 'text', 'txt']:
        header['endian'] = _NUMPY2NRRD_ENDIAN_MAP[data.dtype.str[:1]]
    elif 'endian' in header:
        del header['endian']

    # If space is specified in the header, then space dimension can not. See
    # http://teem.sourceforge.net/nrrd/format.html#space
    if 'space' in header.keys() and 'space dimension' in header.keys():
        del header['space dimension']

    # Update the dimension and sizes fields in the header based on the data. Since NRRD expects meta data to be in
    # Fortran order we are required to reverse the shape in the case of the array being in C order. E.g., data was read
    # using index_order='C'.
    header['dimension'] = data.ndim
    header['sizes'] = list(data.shape) if index_order == 'F' else list(data.shape[::-1])

    # The default encoding is 'gzip'
    if 'encoding' not in header:
        header['encoding'] = 'gzip'

    # A bit of magic in handling options here.
    # If *.nhdr filename provided, this overrides `detached_header=False`
    # If *.nrrd filename provided AND detached_header=True, separate header and data files written.
    # If detached_header=True and data file is present, then write the files separately
    # For all other cases, header & data written to same file.
    if filename.endswith('.nhdr'):
        detached_header = True

        if 'data file' not in header:
            # Get the base filename without the extension
            base_filename = os.path.splitext(filename)[0]

            # Get the appropriate data filename based on encoding, see here for information on the standard detached
            # filename: http://teem.sourceforge.net/nrrd/format.html#encoding
            if header['encoding'] == 'raw':
                data_filename = '%s.raw' % base_filename
            elif header['encoding'] in ['ASCII', 'ascii', 'text', 'txt']:
                data_filename = '%s.txt' % base_filename
            elif header['encoding'] in ['gzip', 'gz']:
                data_filename = '%s.raw.gz' % base_filename
            elif header['encoding'] in ['bzip2', 'bz2']:
                data_filename = '%s.raw.bz2' % base_filename
            else:
                raise NRRDError('Invalid encoding specification while writing NRRD file: %s' % header['encoding'])

            header['data file'] = os.path.basename(data_filename) \
                if relative_data_path else os.path.abspath(data_filename)
        else:
            # TODO This will cause issues for relative data files because it will not save in the correct spot
            data_filename = header['data file']
    elif filename.endswith('.nrrd') and detached_header:
        data_filename = filename
        header['data file'] = os.path.basename(data_filename) \
            if relative_data_path else os.path.abspath(data_filename)
        filename = '%s.nhdr' % os.path.splitext(filename)[0]
    else:
        # Write header & data as one file
        data_filename = filename
        detached_header = False

    with open(filename, 'wb') as fh:
        fh.write(b'NRRD0005\n')
        fh.write(b'# This NRRD file was generated by pynrrd\n')
        fh.write(b'# on ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').encode('ascii') + b'(GMT).\n')
        fh.write(b'# Complete NRRD file format specification at:\n')
        fh.write(b'# http://teem.sourceforge.net/nrrd/format.html\n')

        # Copy the options since dictionaries are mutable when passed as an argument
        # Thus, to prevent changes to the actual options, a copy is made
        # Empty ordered_options list is made (will be converted into dictionary)
        local_options = header.copy()
        ordered_options = []

        # Loop through field order and add the key/value if present
        # Remove the key/value from the local options so that we know not to add it again
        for field in _NRRD_FIELD_ORDER:
            if field in local_options:
                ordered_options.append((field, local_options[field]))
                del local_options[field]

        # Leftover items are assumed to be the custom field/value options
        # So get current size and any items past this index will be a custom value
        custom_field_start_index = len(ordered_options)

        # Add the leftover items to the end of the list and convert the options into a dictionary
        ordered_options.extend(local_options.items())
        ordered_options = OrderedDict(ordered_options)

        for x, (field, value) in enumerate(ordered_options.items()):
            # Get the field_type based on field and then get corresponding
            # value as a str using _format_field_value
            field_type = _get_field_type(field, custom_field_map)
            value_str = _format_field_value(value, field_type)

            # Custom fields are written as key/value pairs with a := instead of : delimeter
            if x >= custom_field_start_index:
                fh.write(('%s:=%s\n' % (field, value_str)).encode('ascii'))
            else:
                fh.write(('%s: %s\n' % (field, value_str)).encode('ascii'))

        # Write the closing extra newline
        fh.write(b'\n')

        # If header & data in the same file is desired, write data in the file
        if not detached_header:
            _write_data(data, fh, header, compression_level=compression_level, index_order=index_order)

    # If detached header desired, write data to different file
    if detached_header:
        with open(data_filename, 'wb') as data_fh:
            _write_data(data, data_fh, header, compression_level=compression_level, index_order=index_order)


def _write_data(data, fh, header, compression_level=None, index_order='F'):
    if index_order not in ['F', 'C']:
        raise NRRDError('Invalid index order')

    if header['encoding'] == 'raw':
        # Convert the data into a string
        raw_data = data.tostring(order=index_order)

        # Write the raw data directly to the file
        fh.write(raw_data)
    elif header['encoding'].lower() in ['ascii', 'text', 'txt']:
        # savetxt only works for 1D and 2D arrays, so reshape any > 2 dim arrays into one long 1D array
        if data.ndim > 2:
            np.savetxt(fh, data.ravel(order=index_order), '%.17g')
        else:
            np.savetxt(fh, data if index_order == 'C' else data.T, '%.17g')

    else:
        # Convert the data into a string
        raw_data = data.tostring(order=index_order)

        # Construct the compressor object based on encoding
        if header['encoding'] in ['gzip', 'gz']:
            compressobj = zlib.compressobj(compression_level, zlib.DEFLATED, zlib.MAX_WBITS | 16)
        elif header['encoding'] in ['bzip2', 'bz2']:
            compressobj = bz2.BZ2Compressor(compression_level)
        else:
            raise NRRDError('Unsupported encoding: "%s"' % header['encoding'])

        # Write the data in chunks (see _WRITE_CHUNKSIZE declaration for more information why)
        # Obtain the length of the data since we will be using it repeatedly, more efficient
        start_index = 0
        raw_data_len = len(raw_data)

        # Loop through the data and write it by chunk
        while start_index < raw_data_len:
            # End index is start index plus the chunk size
            # Set to the string length to read the remaining chunk at the end
            end_index = min(start_index + _WRITE_CHUNKSIZE, raw_data_len)

            # Write the compressed data
            fh.write(compressobj.compress(raw_data[start_index:end_index]))

            start_index = end_index

        # Finish writing the data
        fh.write(compressobj.flush())
        fh.flush()