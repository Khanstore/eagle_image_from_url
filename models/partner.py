# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

from .product import _download_image

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    image_url = fields.Char(
        string="Image URL",
        copy=False,
        help="URL of the contact/partner image. Saving the URL downloads it into the contact image.",
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
                        "Eagle Image from URL: failed to download partner image: %s",
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
                    "Eagle Image from URL: failed to download partner image: %s",
                    image_url,
                )
        return super().write(vals)
