// Copyright (c) 2023, TS and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance"] = {
	"filters": [
		{
			label: "Company",
			fieldname: "company",
			fieldtype: "Link",
			options: "Company"
		},
		{
			label: "From",
			fieldname: "from_date",
			fieldtype: "Date"
		},
		{
			label: "To",
			fieldname: "to_date",
			fieldtype: "Date",
		},
		{
			label: "Employee",
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee"
		},
		{
			label: "Department",
			fieldname: "department",
			fieldtype: "Link",
			options: "Department"
		},
		{
			label: "Late Entry",
			fieldname: "late_entry",
			fieldtype: "Check"
		},
		{
			label: "Early Exit",
			fieldname: "early_exit",
			fieldtype: "Check"
		}
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname.includes('@Working Hours') && data && data[column.fieldname] != "Working Hours") {
			value = "<span style='color:blue'>" + value + "</span>";
		}
		else if (column.fieldname.includes('@Overtime') && data && data[column.fieldname] != "Overtime") {
			value = "<span style='color:green'>" + value + "</span>";
		}
		else if (column.fieldname.includes('@Late Hours') && data && data[column.fieldname] != "Late Hours") {
			value = "<span style='color:red'>" + value + "</span>";
		}

		return value;
	},
	onload: function(report) {
		console.log(report);
	}
};
