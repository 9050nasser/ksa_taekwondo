# Copyright (c) 2023, TS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta
from frappe.utils import getdate,formatdate
from frappe import _

def execute(filters=None):
	columns, data = [], []
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	if not (from_date and to_date):
		return columns, data
	else:
		from_date = getdate(str(from_date))
		to_date = getdate(str(to_date))
		if from_date > to_date:
			frappe.msgprint("From Date Can Not Be After To Date!")
			return columns, data
	
	conditions = get_conditions(filters)
	columns = get_columns(filters)
	data_dict = {}
	for col in columns:
		if '@' in col.get('fieldname'):
			data_dict[col.get('fieldname')] = col.get('fieldname').split('@')[1]
	data = [data_dict]
	data_query = frappe.db.sql(f"""
		select a.working_hours, a.employee, a.employee_name, a.shift, a.attendance_date, a.department, a.late_entry, a.early_exit, a.in_time, a.out_time
		from `tabAttendance` a
		where a.docstatus = 1
		and a.status != "Absent"
		{conditions}
	""",as_dict = 1)

	for row in data_query:
		working_hours = 0
		overtime = 0
		late_hours = 0
		if row.get("shift"):
			shift = frappe.get_doc("Shift Type", row.get("shift"))
		else:
			continue
		
		data_dict = {
			"employee": _(f"""<strong><a href = "/app/Form/Employee/{row.get("employee")}">{row.get("employee")} </a></strong>"""),
			"employee_name":  row.get("employee_name"),
			"department": row.get("department"),
			"shift": row.get("shift")
		}
		working_hours = row.get("working_hours")
		shift_hours = get_time_diff(str(shift.start_time), str(shift.end_time))
		data_dict["shift_hours"] = round(shift_hours,2)
		hours_diff = shift_hours - working_hours
		if hours_diff > 0:
			late_hours = hours_diff
		elif hours_diff < 0:
			overtime = hours_diff * -1
		working_hours_key = str(row.get("attendance_date")) + "@Working Hours"
		overtime_key = str(row.get("attendance_date")) + "@Overtime"
		late_hours_key = str(row.get("attendance_date")) + "@Late Hours"
		late_entry_key = str(row.get("attendance_date")) + "@Late Entry"
		early_exit_key = str(row.get("attendance_date")) + "@Early Exit"
		in_time_key = str(row.get("attendance_date")) + "@In Time"
		out_time_key = str(row.get("attendance_date")) + "@Out Time"
		data_dict[in_time_key] = str(row.get("in_time")).split(' ')[1] if row.get("in_time") else ""
		data_dict[out_time_key] = str(row.get("out_time")).split(' ')[1] if row.get("out_time") else ""
		data_dict[late_entry_key] = row.get("late_entry")
		data_dict[early_exit_key] = row.get("early_exit")
		data_dict[working_hours_key] = round(working_hours,2)
		data_dict[overtime_key] = round(overtime,2)
		data_dict[late_hours_key] = round(late_hours,2)
		data_dict["total@Working Hours"] = round(working_hours,2)
		data_dict["total@Overtime"] = round(overtime,2)
		data_dict["total@Late Hours"] = round(late_hours,2)

		if data_dict["employee"] in str(data):
			for record in data:
				if record.get("employee") == data_dict["employee"]:
					record[working_hours_key] = data_dict[working_hours_key]
					record[overtime_key] = data_dict[overtime_key]
					record[late_hours_key] = data_dict[late_hours_key]
					record[late_entry_key] = row.get("late_entry")
					record[early_exit_key] = row.get("early_exit")
					record[in_time_key] = str(row.get("in_time")).split(' ')[1] if row.get("in_time") else ""
					record[out_time_key] = str(row.get("out_time")).split(' ')[1] if row.get("out_time") else ""
					record["total@Working Hours"] = round(record["total@Working Hours"] + round(working_hours,2),2)
					record["total@Overtime"] = round(record["total@Overtime"] + round(overtime,2),2)
					record["total@Late Hours"] = round(record["total@Late Hours"] + round(late_hours,2),2)
					break
		else:
			data.append(data_dict)
	data_dict = {
		"employee": "Totals"
	}
	for col in columns:
		if '@' in col.get('fieldname') and "Late Entry" not in col.get('fieldname') and "Early Exit" not in col.get('fieldname'):
			total = 0
			for row in data:
				if not row.get(col.get('fieldname')):
					row[col.get('fieldname')] = 0
				else:
					try:
						total += row.get(col.get('fieldname'))
					except:
						continue
			data_dict[col.get('fieldname')] = round(total,2)

	data.append({})
	data.append(data_dict)
	return columns, data

def get_columns(filters):
	from_date = getdate(str(filters.get("from_date")))
	to_date = getdate(str(filters.get("to_date")))
	columns = [
		{
			"label": "Employee",
			"fieldname": "employee",
			"fieldtype": "Data"
		},
		{
			"label": "Employee Name",
			"fieldname": "employee_name",
			"fieldtype": "Data"
		},
		{
			"label": "Department",
			"fieldname": "department",
			"fieldtype": "Data"
		},
		{
			"label": "Shift",
			"fieldname": "shift",
			"fieldtype": "Data"
		},
		{
			"label": "Shift Hours",
			"fieldname": "shift_hours",
			"fieldtype": "Data"
		}
	]
	while from_date <= to_date:
		columns.append({
			"label": formatdate(str(from_date)),
			"fieldname": str(from_date) + "@Working Hours",
			"fieldtype": "Data",
			"width":150
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@Overtime",
			"fieldtype": "Data",
			"width":100
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@Late Hours",
			"fieldtype": "Data",
			"width":100
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@Late Entry",
			"fieldtype": "Data",
			"width":100
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@Early Exit",
			"fieldtype": "Data",
			"width":100
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@In Time",
			"fieldtype": "Data",
			"width":100
		})
		columns.append({
			"label": "",
			"fieldname": str(from_date) + "@Out Time",
			"fieldtype": "Data",
			"width":100
		})
		from_date += timedelta(days= 1)

	columns.append({
		"label": "Totals",
		"fieldname": "total@Working Hours",
		"fieldtype": "Data",
		"width":150
	})
	columns.append({
		"label": "",
		"fieldname": "total@Overtime",
		"fieldtype": "Data",
		"width":100
	})
	columns.append({
		"label": "",
		"fieldname": "total@Late Hours",
		"fieldtype": "Data",
		"width":100
	})
	return columns

def get_conditions(filters):
	conditions = ""
	company = filters.get("company")
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	employee = filters.get("employee")
	department = filters.get("department")
	late_entry = filters.get("late_entry")
	early_exit = filters.get("early_exit")
	if company:
		conditions += f" and a.company = '{company}'"
	if from_date and to_date:
		conditions += f" and a.attendance_date between '{from_date}' and '{to_date}'"
	if employee:
		conditions += f" and a.employee = '{employee}'"
	if department:
		conditions += f" and a.department = '{department}'"
	if late_entry:
		conditions += f" and a.late_entry = {late_entry}"
	if early_exit:
		conditions += f" and a.early_exit = {early_exit}"
	return conditions

def get_time_diff(start_time,end_time):
	t1 = datetime.strptime(start_time, "%H:%M:%S")
	t2 = datetime.strptime(end_time, "%H:%M:%S")
	delta = t2 - t1
	hours = delta.total_seconds()/3600
	return hours