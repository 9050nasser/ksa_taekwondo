# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_expense_claim(source_name, target_doc=None):

	doc = get_mapped_doc("Requests", source_name, {
		"Requests": {
			"doctype": "Expense Claim",
			"field_map": {
				"issue_to": "employee",
				"name": "custom_request"
			}
		}
	}, target_doc)

	return doc

class Requests(Document):
	@frappe.whitelist()
	def generate_request_task(self,department,comment=None,attachments=None):
		self.delete_request_task()
		self.set("concerned_departments", [])
		for i in range(len(department)):
				child = self.append('concerned_departments')
				child.department = department[i]
				child.action = "Draft"
		self.save()
		self.generate_events(comment,attachments)



	@frappe.whitelist()
	def generate_events(self,comment,attachments):
		file = frappe.get_all("File", fields = ["file_url","is_private"], filters = {"attached_to_doctype": self.doctype,
		"attached_to_name":self.name}, order_by="creation desc")

		for item in self.concerned_departments:
			requests_tasks_doc = frappe.new_doc('Requests Tasks')
			requests_tasks_doc.refrence_name = item.name
			requests_tasks_doc.order_type = self.order_type
			requests_tasks_doc.comment = comment
			requests_tasks_doc.request_date = self.request_date
			requests_tasks_doc.sport = self.sport
			requests_tasks_doc.grade = self.grade
			requests_tasks_doc.department = item.department
			requests_tasks_doc.more_information = self.more_informations
			requests_tasks_doc.requests =self.name	
			# requests_tasks_doc.add_attachment(attachments)
			name = requests_tasks_doc.insert().name
			for attachment in attachments:
				doc = frappe.get_doc("Requests Tasks",name)
				doc.attached_file = attachment["file_url"]
				doc.save()
			item.requests_tasks = name
	
		self.save()

	def delete_request_task(self):
		if len(self.concerned_departments):
			for item in self.concerned_departments:
				if item.requests_tasks:
					frappe.delete_doc('Requests Tasks',item.requests_tasks,force=1)

@frappe.whitelist()
def update_deprtment(department, doc=None):
	frappe.db.sql(""" update `tabRequests` set department = %s where name = %s """,(department,doc))
	frappe.db.commit()

