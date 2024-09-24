frappe.ui.form.on('Task', {
	refresh(frm){
		frm.add_custom_button('Create OverTime', () => {
			create_overtime(frm)
		},)
	},
	before_save(frm) {
		// your code here
		if(frm.doc.exp_start_date && frm.doc.completed_on){
		     frm.set_value("difference",frappe.datetime.get_day_diff(cur_frm.doc.completed_on,cur_frm.doc.exp_start_date))
		}
		if(frm.doc.exp_start_date && frm.doc.exp_end_date){
			frm.set_value("estimation_difference",frappe.datetime.get_day_diff(cur_frm.doc.exp_end_date,cur_frm.doc.exp_start_date))
	   }
		   
	}
})
function create_overtime(frm){
	frappe.model.with_doctype('OverTime', function() {
	   var ot = frappe.model.get_new_doc('OverTime');
	   ot.description=frm.doc.description;
	   ot.task_id = frm.doc.name
	   frappe.set_route('Form', 'OverTime', ot.name);
	   cur_frm.refresh_fields();
   })
}