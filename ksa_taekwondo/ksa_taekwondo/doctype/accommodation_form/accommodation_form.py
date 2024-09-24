# Copyright (c) 2023, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AccommodationForm(Document):
	@frappe.whitelist()
	def get_employees(self):
		tk_group_employee = frappe.get_doc("TK Group", self.tk_group)
		for row in tk_group_employee.tk_group_employee:
			employee = self.append('accommodation')
			employee.group = row.group
			employee.employee = row.employee
			employee.designation = frappe.db.get_value("Employee", row.employee, "designation")
