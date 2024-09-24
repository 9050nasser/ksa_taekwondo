// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Routes"] = {
	"filters": [
        {
			fieldname: "tk_group",
			label: __("TK Group"),
			fieldtype: "Link",
			options: "TK Group",
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},

	]
};