frappe.ui.form.on('Accommodation Form', {
	contact_person(frm) {
        if(frm.doc.contact_person){
            frappe.db.get_doc("Contact",frm.doc.contact_person).then(r=>{
                if(r.phone_nos.length>0){
                    frm.set_value("phone",r.phone_nos[0].phone)
                    frm.set_value("email",r.email_ids[0].email_id)
                }
               
            })
        }
        else{
            frm.set_value("phone","")
            frm.set_value("email","")
        }
	},
    check_in(frm) {
        if(frm.doc.check_in && frm.doc.check_out){
            frm.set_value("number_of_nights",frappe.datetime.get_day_diff(frm.doc.check_out,frm.doc.check_in))
        }else{
            frm.set_value("number_of_nights","")
        }
    },
    check_out(frm) {
        if(frm.doc.check_in && frm.doc.check_out){
            frm.set_value("number_of_nights",frappe.datetime.get_day_diff(frm.doc.check_out,frm.doc.check_in))
        }else{
            frm.set_value("number_of_nights","")
        }
    },
    tk_group(frm) {
        if (frm.doc.tk_group){
            // fill child table accommodation with employees of the selected group
            frm.clear_table('accommodation');
            frappe.call({
                method: "get_employees",
                doc: frm.doc,
                callback: function(r) {
                        frm.refresh_field('accommodation');
                    
                }
            });
        }
    },
    refresh(frm) {
		frm.set_query('employee', 'accommodation', function(doc, cdt, cdn) {
			var d = locals[cdt][cdn];
                return {
                    filters:{
                        "group": d.group
                    }
                }
			
		});
	}


})

frappe.ui.form.on('Accommodation', {

	accommodation_add(frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, "check_in", frm.doc.check_in);
        frappe.model.set_value(cdt, cdn, "check_out", frm.doc.check_out);
        frappe.model.set_value(cdt, cdn, "number_of_nights", frm.doc.number_of_nights);
	},
    employee(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; 
        frappe.db.get_doc("Employee",row.employee).then(r=>{
            frappe.model.set_value(cdt, cdn, "designation", r.designation);
            frappe.model.set_value(cdt, cdn, "employee_name", r.employee_name);
        })
	},
    check_in(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; 
        if(row.check_in && row.check_out){
            frappe.model.set_value(cdt,cdn,"number_of_nights",frappe.datetime.get_day_diff(row.check_out,row.check_in))
        }else{
            frappe.model.set_value(cdt,cdn,"number_of_nights","")
        }
    },
    check_out(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; 
        if(row.check_in && row.check_out){
            frappe.model.set_value(cdt,cdn,"number_of_nights",frappe.datetime.get_day_diff(row.check_out,row.check_in))
        }else{
            frappe.model.set_value(cdt,cdn,"number_of_nights","")
        }
    },
    room_type(frm, cdt, cdn) {
        let row = locals[cdt][cdn]; 
        if(row.room_type && frm.doc.accommodation[row.idx -2].room_type == "Twin"){ 
            frappe.msgprint(__(`You Can't Set Room Type As <b>${row.room_type}</b> Becouse This Person Residing with:<br> <b> ${frm.doc.accommodation[row.idx -2].employee_name} `));
            frappe.model.set_value(cdt,cdn,"room_type","")
        }
        if(row.room_type && frm.doc.accommodation[row.idx -2].room_type == "Triple"){ 
            frappe.msgprint(__(`You Can't Set Room Type As <b>${row.room_type}</b> Becouse This Person Residing with:<br> <b> ${frm.doc.accommodation[row.idx -2].employee_name} `));
            frappe.model.set_value(cdt,cdn,"room_type","")
        }
        if(row.room_type && frm.doc.accommodation[row.idx -3].room_type == "Triple"){ 
            frappe.msgprint(__(`You Can't Set Room Type As <b>${row.room_type}</b> Becouse This Person Residing with:<br> <b> ${frm.doc.accommodation[row.idx -2].employee_name} <br>${frm.doc.accommodation[row.idx -3].employee_name}  `));
            frappe.model.set_value(cdt,cdn,"room_type","")
        }
    },
})