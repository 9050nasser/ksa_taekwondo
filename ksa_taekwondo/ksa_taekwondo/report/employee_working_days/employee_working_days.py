# Copyright (c) 2023, Trigger Solutions and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_data(filters):
	sql = ""
	if filters.employee:
		sql += f" and employee = '{filters.employee}'"
	if filters.shift_type:
		sql += f" and shift = '{filters.shift_type}'"
	data = frappe.db.sql(f"""select employee, employee_name,shift, count(name) as total_working_days, sum(working_hours) as employee_working_hours , sum(late_entry_hours) as total_late_entry, sum(early_exit_hours) as total_exit_early from `tabAttendance` 
					where attendance_date between TIMESTAMP('{filters.from_date}', '00:00:00') and TIMESTAMP('{filters.to_date}', '23:59:59') and docstatus = 1 {sql} group by employee_name""", as_dict=1)
	return data
	

def get_columns():
	return [
		{
			"fieldname": "employee",
			"label": "Employee Code",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 150
		},
		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "shift",
			"label": "Shift",
			"fieldtype": "Link",
			"options": "Shift Type",
			"width": 150
		},
		{
			"fieldname": "total_working_days",
			"label": "Total Working Days",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "employee_working_hours",
			"label": "Employee Working Hours",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "total_late_entry",
			"label": "Total Late Entry",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "total_exit_early",
			"label": "Total Exit Early",
			"fieldtype": "Float",
			"width": 150
		}
	]
		


