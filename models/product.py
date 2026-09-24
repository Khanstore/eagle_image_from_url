# -*- coding: utf-8 -*-

from odoo import api, fields, models
import base64
import logging
import ssl
import urllib.error
import urllib.request

_logger = logging.getLogger(__name__)


def _download_image(url):
    """Download an image from URL and return base64 bytes."""
    if not url:
        return False

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/153.0.0.0 Safari/537.36"
        )
    }
    request = urllib.request.Request(url, headers=headers)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(request, context=context, timeout=30) as response:
        data = response.read()

    return base64.b64encode(data)


class Product(models.Model):
    _inherit = "product.product"

    image_url = fields.Char(
        string="Image URL",
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("image_1920") and vals.get("image_url"):
                try:
                    image = _download_image(vals["image_url"])
                    if image:
                        vals["image_1920"] = image
                except Exception:
                    _logger.exception(
                        "Eagle Image from URL: failed to download product image: %s",
                        vals.get("image_url"),
                    )
        return super().create(vals_list)

    def write(self, vals):
        image_url = vals.get("image_url")
        if image_url:
            try:
                image = _download_image(image_url)
                if image:
                    vals["image_1920"] = image
            except Exception:
                _logger.exception(
                    "Eagle Image from URL: failed to download product image: %s",
                    image_url,
                )
        return super().write(vals)
