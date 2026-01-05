from __future__ import annotations

from io import BytesIO
from django import template
from django.utils.termcolors import background
from ..labelprinterkit.constants import Media
import qrcode.constants as ECL
from qrcode.exceptions import DataOverflowError
import math
from qrcode.main import QRCode
from django.utils.safestring import mark_safe
import report.helpers
register = template.Library()

@register.filter
def mm_to_ptouch_height_px(value):
    if value == 3.5:
        print(f"pixel height: {Media.W3_5.value.printarea}")
        return Media.W3_5.value.printarea
    if value == 6:
        print(f"pixel height: {Media.W6.value.printarea}")
        return Media.W6.value.printarea
    if value == 9:
        print(f"pixel height: {Media.W9.value.printarea}")
        return Media.W9.value.printarea
    if value == 12:
        print(f"pixel height: {Media.W12.value.printarea}")
        return Media.W12.value.printarea
    if value == 18:
        print(f"pixel height: {Media.W18.value.printarea}")
        return Media.W18.value.printarea
    if value == 24:
        print(f"pixel height: {Media.W24.value.printarea}")
        return Media.W24.value.printarea

    raise BaseException("Height must be one of 3.5, 6, 9, 12, 18 or 24")


@register.filter
def mm_to_ptouch_width_px(value):
    print(f"pixel value: {value}")
    width = int((value - 3.5) * (180/25.4))
    print(f"pixel width: {width}")
    return width


@register.simple_tag
def shrink_if_possible():
    return mark_safe("<!--@brother-dynamic-width-printer-driver:shrink-if-possible-->")