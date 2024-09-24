// Copyright (c) 2023, Trigger Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Working Days"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"label": __("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
			"label": __("Shift Type"),
			"fieldname": "shift_type",
			"fieldtype": "Link",
			"options": "Shift Type",
		}
	]
};
