// Copyright (c) 2023, Trigger Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('OverTime', {
	hours: function(frm) {
		frm.call('calculate_overtime_hours').then(r => {
			if (r.message) {
				console.log(r.message);
				var frm_hours = frm.doc.hours;
				if (r.message.working_hours>60) {
					frm.set_value('hours', 0);
					frappe.msgprint(__('Working hours cannot be more than 60 hours , <br> total Monthly hours: {0}', [r.message.working_hours-frm_hours]));
				}
				if (r.message.daily_hours>3) {
					frm.set_value('hours', 0);
					frappe.msgprint(__('Daily hours cannot be more than 3 hours , <br> total Daily hours: {0}', [r.message.daily_hours-frm_hours]));
				}
			}
		});
	},
	validate(frm) {
		if(frm.doc.hours<1) {
			frappe.throw(__('Hours cannot be less than 1'));
		}
	}
});
