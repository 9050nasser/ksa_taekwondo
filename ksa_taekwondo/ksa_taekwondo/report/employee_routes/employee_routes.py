# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt
import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": ("Employee Route"),
            "fieldname": "employee_route",
            "fieldtype": "Link",
            "options": "Employee Route",
            "width": 130
        },
        {
            "label": ("Group Name"),
            "fieldname": "group_name",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 130
        },
        {
            "label": ("Employee Full Name"),
            "fieldname": "full_name",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Passport no"),
            "fieldname": "passport_no",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Group"),
            "fieldname": "group",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Date of Birth"),
            "fieldname": "dob",
            "fieldtype": "Date",
            "width": 130
        },
        {
            "label": ("Location"),
            "fieldname": "location",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Check In"),
            "fieldname": "departure",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("Check Out"),
            "fieldname": "check_out",
            "fieldtype": "Data",
            "width": 130
        },
    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("tk_group"):
        conditions += "and employee_route.tk_group = %(tk_group)s"
    if filters.get("employee"):
        conditions += "and employee_route.employee = %(employee)s"
       
    result = []
    item_results = frappe.db.sql("""
            select 
            employee_route.name,
            employee_route.group_name,
            employee_route.employee,
            employee_route.full_name,
            employee_route.passport_no,
            employee_route.group,
            employee_route.dob,
            employee_route_details.location,
            employee_route_details.departure,
            employee_route_details.check_out
                                 
            from `tabEmployee Route` employee_route 
            join `tabEmployee Route Details` employee_route_details on employee_route.name = employee_route_details.parent
            where 1=1
            {conditions}
            order by employee_route.name
        """.format(conditions=conditions), filters, as_dict=1)

    for item_dict in item_results:
        data = {
            "employee_route":item_dict.name,
            "group_name":item_dict.group_name,
            "employee":item_dict.employee,
            "full_name":item_dict.full_name,
            "passport_no":item_dict.passport_no,
            "group":item_dict.group,
            "dob":item_dict.dob,
            "location":item_dict.location,
            "departure":item_dict.departure,
            "check_out":item_dict.check_out,
        }
        result.append(data)
    if result:
        result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
    return result