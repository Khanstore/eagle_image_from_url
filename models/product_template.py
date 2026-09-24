# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

from .product import _download_image

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    image_url_template = fields.Char(
        string="Image URL",
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("image_1920") and vals.get("image_url_template"):
                try:
                    image = _download_image(vals["image_url_template"])
                    if image:
                        vals["image_1920"] = image
                except Exception:
                    _logger.exception(
                        "Eagle Image from URL: failed to download template image: %s",
                        vals.get("image_url_template"),
                    )
        return super().create(vals_list)

    def write(self, vals):
        image_url_template = vals.get("image_url_template")
        if image_url_template:
            try:
                image = _download_image(image_url_template)
                if image:
                    vals["image_1920"] = image
            except Exception:
                _logger.exception(
                    "Eagle Image from URL: failed to download template image: %s",
                    image_url_template,
                )
        return super().write(vals)
