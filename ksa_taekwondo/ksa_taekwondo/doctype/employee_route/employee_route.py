# Copyright (c) 2024, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# searches for group employee
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_group_employees(doctype, txt, searchfield, start, page_len, filters):
	if filters.get("parent"):
		return frappe.db.sql(
			"""
			SELECT 
				employee, 
				employee_name
			FROM
				`tabTK Group Employee`
			WHERE 
				parent = '{0}'
			""".format(filters.get("parent")),  as_list=1)
	else:
		return frappe.db.sql(
			"""
			SELECT 
				employee, 
				employee_name
			FROM
				`tabEmployee`
			""", as_list=1)


class EmployeeRoute(Document):
	pass
