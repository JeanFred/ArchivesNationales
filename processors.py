# -*- coding: latin-1 -*-

"""Partnership with the Archives Nationales."""

import re


def split_and_apply_template_on_each(field, old_field_value, template, mapper, separator=","):
    """Split the old value against the given separator and apply the template on each part"""
    bits = old_field_value.split(separator)
    translated_bits = [mapper.get(x.strip(), x.strip()) for x in bits]
    new_value = ', '.join(["{{%s|%s}}" % (template, x) for x in translated_bits])
    return {field: new_value}


def look_for_sizes(field, old_field_value):
    """Wrapper for matching sizes."""
    new_value = look_for_sizes_unwrapped(old_field_value)
    return {field: new_value}


def _clean_dim(dim):
    """Clean a dimension-like string"""
    return re.sub(r"\s?,\s?", '.', dim).strip()


def look_for_sizes_unwrapped(text):
    """Return the given text with size patterns converted"""

    def repl(m):
        """Convert the pattern matchd in {{Size}}."""
        elements = m.groupdict()
        unit = elements.pop('unit')
        l = filter(None, [elements[x] for x in sorted(elements.keys())])
        s = '|'.join([_clean_dim(dim) for dim in l])
        return " {{Size|%s|%s}}" % (unit, s)

    size_pattern = re.compile(r"""
        (                      # All of that being conditional...
            (?P<a>[\d,\s]+?)   # Digits, comma or whitespace, captured as group
            (\sx\s)            # Whitespace, x, whitespace
        )?
        (                      # Same thing
            (?P<b>[\d,\s]+?)
            (\sx\s)
        )?
        (?P<z>[\d,\s]+?)
        \s+
        (?P<unit>[c|m]m)
        """, re.X)
    new_value = re.sub(size_pattern, repl, text)
    return new_value
