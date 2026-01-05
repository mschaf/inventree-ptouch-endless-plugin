from PIL.Image import Resampling
from PIL import Image

from django.db import models
from django.utils.translation import gettext_lazy as _

from plugin import InvenTreePlugin
from report.models import LabelTemplate
from plugin.machine import BaseMachineType
from plugin.machine.machine_types import LabelPrinterBaseDriver, LabelPrinterMachine
from plugin.mixins import MachineDriverMixin, AppMixin

from .labelprinterkit.printers import P700, P750W, H500, E500, E550W
from .labelprinterkit.backends.network import TCPBackend
from .labelprinterkit.job import Job
from .labelprinterkit.constants import Media
from .labelprinterkit.page import Page

PLUGIN_VERSION = "0.1.0"

ALL_MODELS = {
    "P700": P700,
    "P750W": P750W,
    "H500": H500,
    "E500": E500,
    "E550W": E550W,
}

class PTouchEndlessPlugin(AppMixin, MachineDriverMixin, InvenTreePlugin):
    """Inventree plugin supporting specifically Brother PTouch Series printers."""

    AUTHOR = "Martin Schaflitzl"
    DESCRIPTION = "Printer driver for brother ptouch series printers, supporting a variable length labels."
    VERSION = PLUGIN_VERSION

    MIN_VERSION = "1.1.0"

    NAME = "PTouch Endless Plugin"
    SLUG = "ptouch-endless"
    TITLE = "PTouch Endless Plugin"

    BLOCKING_PRINT = True

    def get_machine_drivers(self) -> list:
        return [PTouchEndlessDriver]


class PTouchEndlessDriver(LabelPrinterBaseDriver):
    SLUG = "ptouch-endless"
    NAME = "PTouch Endless Label Printer Driver"
    DESCRIPTION = "Brother label printing driver for InvenTree supporting labels with a dynamic width, depending on the amount of content."

    def __init__(self, *args, **kwargs):
        """Initialize the BrotherLabelPrinterDriver."""
        self.MACHINE_SETTINGS = {
            "MODEL": {
                "name": _("Printer Model"),
                "description": _("Select model of Brother printer"),
                "choices": self.get_model_choices,
                "default": "P750W",
                "required": True,
            },
            "IP_ADDRESS": {
                "name": _("IP Address"),
                "description": _("IP address of the brother label printer"),
                "default": "",
            },
        }

        super().__init__(*args, **kwargs)

    def get_model_choices(self, **kwargs):
        return [(model, model) for model in list(ALL_MODELS.keys())]

    def init_machine(self, machine: BaseMachineType):
        machine.set_status(LabelPrinterMachine.MACHINE_STATUS.CONNECTED)

    def print_label(
        self,
        machine: LabelPrinterMachine,
        label: LabelTemplate,
        item: models.Model,
        **kwargs,
    ) -> None:

        supersampling_factor = 8
        image = self.render_to_png(label, item, dpi=96*supersampling_factor)

        target_size = (int(image.size[0] / supersampling_factor), int(image.size[1] / supersampling_factor))

        monochrome_image = image.resize(target_size, resample=Resampling.NEAREST).convert("L").point(lambda p: 255 if p > 128 else 0, "1")

        rendered_html = self.render_to_html(label, item)
        print(rendered_html)
        if "<!--@brother-dynamic-width-printer-driver:shrink-if-possible-->" in rendered_html:
            monochrome_image = _trim_right_whitespace(monochrome_image)

        page = Page.from_image(monochrome_image)
        # page.image.save('/tmp/label.png')

        job = Job(_media_from_height(monochrome_image.size[1]), half_cut=True)
        job.add_page(page)

        backend = TCPBackend(machine.get_setting("IP_ADDRESS", "D"))
        printer = _printer_class_from_model_string(machine.get_setting("MODEL", "D"))(backend)
        printer.print(job)


def _trim_right_whitespace(img: Image.Image) -> Image.Image:
    """
    Removes only-white columns on the right side of a 1-bit image.
    Result: rightmost column contains at least one black pixel (unless image is fully white).
    """
    if img.mode != "1":
        img = img.convert("1")

    w, h = img.size

    # Convert to L for cheap pixel access (white=255, black=0)
    g = img.convert("L")
    px = g.load()

    # Scan from right to left for a column that contains any black pixel
    last_col = -1
    for x in range(w - 1, -1, -1):
        for y in range(h):
            if px[x, y] == 0:  # black
                last_col = x
                break
        if last_col != -1:
            break

    if last_col == -1:
        # No black pixels at all -> nothing meaningful to trim; return as-is (or return 1px width if you prefer)
        return img

    # Crop to include last_col
    return img.crop((0, 0, last_col + 1, h))


def _media_from_height(value):
    value = int(value)

    if value ==  Media.W3_5.value.printarea:
        return Media.W3_5
    if value == Media.W6.value.printarea:
        return Media.W6
    if value == Media.W9.value.printarea:
        return Media.W9
    if value == Media.W12.value.printarea:
        return Media.W12
    if value == Media.W18.value.printarea:
        return Media.W18
    if value == Media.W24.value.printarea:
        return Media.W24

    raise BaseException(f"Could not determine media type from height ({value})")


def _printer_class_from_model_string(printer_class):
    if printer_class not in ALL_MODELS:
        raise ValueError(f"Printer class {printer_class} not supported")

    return ALL_MODELS[printer_class]
