import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_salary_slip_(salary_slip_doc, doc_event):
    hours = frappe.db.sql(f"""select sum(hours) from `tabOverTime` where employee = '{salary_slip_doc.employee}' and docstatus = 1 and overtime_date between '{salary_slip_doc.start_date}' and '{salary_slip_doc.end_date}' """, as_dict=True) 
    if hours[0]['sum(hours)']:
        salary_slip_doc.overtime_per_hours = hours[0]['sum(hours)']
    else:
        salary_slip_doc.overtime_per_hours = 0