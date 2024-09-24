// Copyright (c) 2023, Trigger Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Minutes of Meeting', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.is_expense_claim==0)
		{
			frm.add_custom_button(__("Pay a Reward"), function(){
				frm.call('expense_claim').then(r=>{
					frm.reload_doc()
					frappe.msgprint(__('Expense Claim Created Successfully'));
				})
			  });
		}
	}
});
