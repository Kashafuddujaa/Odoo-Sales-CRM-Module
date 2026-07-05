# Optional custom image for the sales_crm addon.
# docker-compose.yml uses the stock odoo:17.0 image by default; build this
# instead when you need extra Python dependencies baked in.
FROM odoo:17.0

USER root

# Add any extra Python requirements here, e.g.:
# COPY requirements.txt /tmp/requirements.txt
# RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY ./sales_crm /mnt/extra-addons/sales_crm

USER odoo
