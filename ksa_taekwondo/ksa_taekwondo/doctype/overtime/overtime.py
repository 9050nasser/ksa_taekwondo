# Copyright (c) 2023, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date


class OverTime(Document):
	@frappe.whitelist()
	def calculate_overtime_hours(self):
		# get first date on the month in overtime date field
		first_date = frappe.utils.get_first_day(self.overtime_date)
		# get last date on the month in overtime date field
		last_date = frappe.utils.get_last_day(self.overtime_date)
		# get employee working hours in the month
		working_hours = frappe.db.sql(f"""SELECT SUM(hours) as hours FROM `tabOverTime` WHERE employee = '{self.employee}' AND overtime_date between '{first_date}' and '{last_date}' and name != '{self.name}' and docstatus = 1 """,as_dict=True)
		# get employee working hours in the day
		daily_hours = frappe.db.sql(f"""SELECT SUM(hours) as hours FROM `tabOverTime` WHERE employee = '{self.employee}' AND overtime_date = '{self.overtime_date}' and name != '{self.name}' and docstatus = 1 """,as_dict=True)
		if working_hours[0]['hours'] or daily_hours[0]['hours']:
			return {'working_hours':working_hours[0]["hours"]+self.hours,'daily_hours':daily_hours[0]["hours"]+self.hours}
		else:
			return {'working_hours':0+self.hours,'daily_hours':0+self.hours}