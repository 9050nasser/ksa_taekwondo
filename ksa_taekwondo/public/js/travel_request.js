frappe.ui.form.on('Travel Request', {
    onload(frm){
        frm.set_query('country', () => {
            return {
                filters: {
                    name: ['!=','Saudi Arabia']
                }
            }
        })
    },
    refresh(frm){
        if (frm.doc.docstatus == 1){
            frm.add_custom_button('Expense Claim', () => {
                frappe.model.open_mapped_doc({
					method: 'ksa_taekwondo.public.py.travel_request.create_expense_claim',
					frm: frm,
                    doc:frm.doc
				})
            }, 'Create');    
        }
        
        
    },
    validate(frm){
        if(frm.doc.itinerary.length>0){
            frm.set_value("travel_days", frappe.datetime.get_day_diff(frm.doc.itinerary[0].arrival_date , frm.doc.itinerary[0].departure_date )+1);
        }
        setup(frm)
    },
    before_save(frm){
       
    },
    // employee(frm) {
    //     setup(frm)
    // },
    // travel_type(frm){
    //     setup(frm)
    // },
    // travel_days(frm){
    //     setup(frm)
    // },
    // travel_funding(frm){
    //     setup(frm)
    // },
    // country(frm){
    //     setup(frm)
    // }
})

function setup(frm){
    var num = 0
    if(cur_frm.doc.travel_insurance == "No" && cur_frm.doc.food_and_housing_insurance == "No"){
        num = 1
    }
    else if(cur_frm.doc.travel_insurance == "Yes" && cur_frm.doc.food_and_housing_insurance == "No"){
        num = .75
    }
    else if(cur_frm.doc.travel_insurance == "No" && cur_frm.doc.food_and_housing_insurance == "Yes"){
        num = .75
   }
    else if(cur_frm.doc.travel_insurance == "Yes" && cur_frm.doc.food_and_housing_insurance == "Yes"){
        num = .50
    }
    if (frm.doc.employee){
        
        frappe.db.get_value('Employee',frm.doc.employee,"designation").then(r =>{
            var designation = r.message.designation
            frappe.db.get_doc('Designation',designation,"designation").then(d =>{
                var items = d.business_travel_allowance
                items.forEach(item => {
                    if(frm.doc.travel_type=="Domestic"){
                        frm.set_value('costings', [])
                        cur_frm.refresh_fields("costings");
                        var childTable = cur_frm.add_child("costings");
                        childTable.expense_type= item.type
                        childTable.total_amount = item.inside_ksa * frm.doc.travel_days * num
                        cur_frm.refresh_fields("costings");
                    }
                    else{
                        if(frm.doc.country){
                            frappe.db.get_value('Country',frm.doc.country,"distance").then(value =>{
                                console.log(value.message.distance)
                                if (value.message.distance == "Near"){
                                    frm.set_value('costings', [])
                                    cur_frm.refresh_fields("costings");
                                    var childTable = cur_frm.add_child("costings");
                                    childTable.expense_type= item.type
                                    childTable.total_amount = item.outside_ksa * ( frm.doc.travel_days + 2 ) * num
                                    cur_frm.refresh_fields("costings");
                                }else{
                                    frm.set_value('costings', [])
                                    cur_frm.refresh_fields("costings");
                                    var childTable = cur_frm.add_child("costings");
                                    childTable.expense_type= item.type
                                    childTable.total_amount = item.outside_ksa * ( frm.doc.travel_days + 3 ) * num
                                    cur_frm.refresh_fields("costings");
                                }
                                
                            })
                        }
                        
                    }
                    
                });
            });
            
        });
        
    }
}