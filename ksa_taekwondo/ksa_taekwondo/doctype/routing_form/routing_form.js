// Copyright (c) 2023, Trigger Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Routing Form', {
	refresh(frm) {
		frm.set_query('employee', 'routing_details', function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
                return {
                    filters:{
                        "group": d.group
                    }
                }
			
		});
	}
})

frappe.ui.form.on('Routing Details', {
	routing_details_add(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "departure", frm.doc.departure);
        frappe.model.set_value(cdt, cdn, "return", frm.doc.return);
	},
	employee(frm, cdt, cdn) {
		let row = locals[cdt][cdn]; 
		if(row.employee){
			frappe.db.get_doc("Employee",row.employee).then(r=>{
				frappe.model.set_value(cdt, cdn, "dob", r.date_of_birth);
				frappe.model.set_value(cdt, cdn, "name_english", r.full_name_in_arabic);
				frappe.model.set_value(cdt, cdn, "name_arabic", r.employee_name);
				frappe.model.set_value(cdt, cdn, "passport_no", r.passport_number);
				frappe.model.set_value(cdt, cdn, "issuing_date", r.date_of_issue);
				frappe.model.set_value(cdt, cdn, "expired_date", r.valid_upto);
			})
		}
		else{
			frappe.model.set_value(cdt, cdn, "dob", "");
				frappe.model.set_value(cdt, cdn, "name_english", "");
				frappe.model.set_value(cdt, cdn, "name_arabic", "");
				frappe.model.set_value(cdt, cdn, "passport_no", "");
				frappe.model.set_value(cdt, cdn, "issuing_date", "");
				frappe.model.set_value(cdt, cdn, "expired_date", "");
		}
		
	}
})
