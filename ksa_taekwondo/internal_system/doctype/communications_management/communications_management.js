// Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Communications management', {
	type: function(frm) {
		if(frm.is_new()){
			if(frm.doc.type =='صادر'){
				frm.set_value('naming_series','OUT-.#####')
			}
			else{
				frm.set_value('naming_series','IN-.#####')
			}
		}
	},
	date: function(frm) {
		
		if(frm.doc.date){
			const d = new Date(frm.doc.date);
			const x = new Intl.DateTimeFormat('ar-TN-u-ca-islamic', {day: 'numeric', month: 'numeric',weekday: 'long',year : 'numeric'}).format(d);
			frm.set_value('hijri_date',Intl.DateTimeFormat('ar-SA-islamic-umalqura').format(d))
			frm.set_value('hijri_year',x.substring(x.length-5,x.length-3))
		}
		else{
			frm.set_value('hijri_date',null)
			frm.set_value('hijri_year',null)
		}
	},
});
