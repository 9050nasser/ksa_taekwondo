# Copyright (c) 2023, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import utils
from frappe.model.document import Document

class MinutesofMeeting(Document):
	@frappe.whitelist()
	def expense_claim(self):
		reword_doc=frappe.get_doc('Reward Setting')
		for item in self.participants:
			if  item.has_meeting_rewored:
				doc = frappe.new_doc('Expense Claim')
				doc.employee = item.participant
				doc.approval_status="Approved"
				doc.payable_account=reword_doc.account
				doc.minutes_of_meeting = self.name
				doc.append('expenses',{
					'amount':reword_doc.amount,
					'expense_date':utils.today(),
					'expense_type':reword_doc.expense_claim_type
				})
				doc.insert()
		self.is_expense_claim = 1
		self.save()