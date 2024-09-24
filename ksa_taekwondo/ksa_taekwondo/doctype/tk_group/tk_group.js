// Copyright (c) 2024, Trigger Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("TK Group", {
	refresh(frm) {
		frm.custom_make_buttons = {
            "Employee Route": "Employee Route",
		};
		frm.make_methods = {
			"Employee Route": () =>
			frappe.model.open_mapped_doc({
				method: "ksa_taekwondo.ksa_taekwondo.doctype.tk_group.tk_group.create_employee_route",
				frm: frm,
			}),
		};
            for (const doctype in frm.make_methods) {
                frm.add_custom_button(__(doctype), frm.make_methods[doctype], __("Create"));
            }
        
	},
});
