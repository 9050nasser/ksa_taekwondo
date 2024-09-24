# Copyright (c) 2023, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeRequest(Document):
	def validate(self):
		total_salary = frappe.db.get_value("Salary Structure Assignment",{"employee":self.employee},"total_salary")
		allowances,country,employment_type = frappe.db.get_value("Employee",self.employee,["allowances","country","employment_type"])
		basic = 0
		housing_allowance = 0
		transportation_allowance = 0
		social_insurance = 0
		if allowances ==  "بدون بدلات":
			basic = total_salary
		elif allowances == "بدل سكن فقط":
			housing_allowance = total_salary * .25
			basic = total_salary- self.housing_allowance
		elif allowances == "بدل مواصلات فقط":
			transportation_allowance = total_salary * .10
			basic = total_salary - self.transportation_allowance
		elif allowances == "مستحق للبدلات":
			basic = total_salary/1.35
			housing_allowance = basic * 0.25
			transportation_allowance = basic * 0.10
		else:
			basic = total_salary/1.35
			housing_allowance = 0
			transportation_allowance = 0
		
		if country == "Saudi Arabia" and employment_type == "دوام كامل":
			social_insurance = (basic + housing_allowance) * 0.0975
		self.basic = basic
		self.housing_allowance = housing_allowance
		self.transportation_allowance = transportation_allowance
		self.social_insurance = social_insurance
		

		
		
