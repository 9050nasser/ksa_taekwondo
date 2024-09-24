// Copyright (c) 2024, Trigger Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Route", {
	refresh(frm) {
        frm.fields_dict.employee.get_query = function (doc, cdt, cdn) {
			return { 
                query: "ksa_taekwondo.ksa_taekwondo.doctype.employee_route.employee_route.get_group_employees",
                filters: {
                    "parent": doc.tk_group
                }
         };
		};
	},
    
});
