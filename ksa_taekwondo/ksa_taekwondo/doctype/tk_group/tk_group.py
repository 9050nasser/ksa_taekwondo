# Copyright (c) 2024, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def create_employee_route(source_name, target_doc=None):
	doc = get_mapped_doc("TK Group", source_name, {
		"TK Group": {
			"doctype": "Employee Route",
			"field_map": {
				"name": "tk_group",
			}
		}
	}, target_doc)

	return doc

class TKGroup(Document):
	pass

	
