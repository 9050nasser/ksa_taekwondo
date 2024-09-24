# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from frappe.model.naming import make_autoname
import frappe
from datetime import date
import time
from pyqrcode import create as qr_create
import io
import os
from frappe.model.document import Document

class Communicationsmanagement(Document):
	def after_insert(self):    
		# creating qr code for the Sales Invoice
		qr_code = self.get("qr_code")
		if qr_code and frappe.db.exists({"doctype": "File", "file_url": qr_code}):
			return
		xml = f"""{frappe.utils.get_url()+"/app/Communications%20management/"+self.name}"""
		qr_image = io.BytesIO()
		xml = qr_create(xml, error='L')
		xml.png(qr_image, scale=2, quiet_zone=1)
		# making file
		filename = f"DOC-QR-CODE-{self.name}.png".replace(os.path.sep, "__")
		_file = frappe.get_doc({
			"doctype": "File",
			"file_name": filename,
			"content": qr_image.getvalue(),
			"is_private": 1
		})
		_file.save()
		# assigning to document
		self.db_set('qr_code', _file.file_url)
		self.notify_update()

	def before_save(self):
		from frappe.desk.form.load import get_attachments
		self.attachments = 0 if len(get_attachments('Communications management',self.name))-1 < 0 else len(get_attachments('Communications management',self.name))-1
