import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_expense_claim(source_name):
    def update_item(source, target, source_parent):
        target.approval_status = "Approved"
        for row in source.costings:
            child = target.append('expenses')
            child.expense_type = row.expense_type
            child.amount = row.total_amount
    doclist = get_mapped_doc("Travel Request",source_name, {
					"Travel Request": {
						"doctype": "Expense Claim",
						"postprocess": update_item
					}
				})
    return doclist