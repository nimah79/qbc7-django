from rest_framework.pagination import CursorPagination
from base64 import b64decode, b64encode
from urllib import parse
from rest_framework.utils.urls import replace_query_param
from collections import namedtuple

Cursor = namedtuple('Cursor', ['offset', 'reverse', 'position'])


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class IdBasedCursorPagination(CursorPagination):
    ordering = '-id'

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)[::-1]
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return replace_query_param(self.base_url, self.cursor_query_param, encoded)

    def decode_cursor(self, request):
        """
        Given a request with a cursor, return a `Cursor` instance.
        """
        # Determine if we have a cursor, and if so then decode it.
        encoded = request.query_params.get(self.cursor_query_param)
        if encoded is None:
            return None

        try:
            querystring = b64decode(encoded.encode('ascii')).decode('ascii')[::-1]
            tokens = parse.parse_qs(querystring, keep_blank_values=True)

            offset = tokens.get('o', ['0'])[0]
            offset = _positive_int(offset, cutoff=self.offset_cutoff)

            reverse = tokens.get('r', ['0'])[0]
            reverse = bool(int(reverse))

            position = tokens.get('p', [None])[0]
        except (TypeError, ValueError):
            raise NotFound('self.invalid_cursor_message')

        return Cursor(offset=offset, reverse=reverse, position=position)
