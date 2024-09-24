frappe.ui.form.on('Expense Claim', {
	refresh(frm) {
		// your code here
	}
});
frappe.ui.form.on("Expense Claim Detail",{
    'currency'(frm, cdt, cdn){
        get_rate(frm,cdt,cdn)
    },'currency_amount'(frm,cdt,cdn){
        get_rate(frm,cdt,cdn)
    }
});
function get_rate(frm,cdt,cdn){
    const row = frappe.get_doc(cdt,cdn)
    if(frm.doc.company){
        frappe.db.get_value('Company',frm.doc.company,'default_currency').then(r=>{
            const copmany_default_currency= r.message.default_currency;
            frappe.db.get_value('Currency Exchange',{
                'from_currency':['=', row.currency],
                'to_currency':['=', copmany_default_currency]}
                ,'exchange_rate').then(r=>{
                    const rate = r.message.exchange_rate;
                    const test = 1
                    
                    if(row.currency == copmany_default_currency){
                        frappe.model.set_value(cdt, cdn,'exchange_rate', test);
                        frappe.model.set_value(cdt, cdn, 'amount', row.currency_amount*test)
                    }
                    else{
                        frappe.model.set_value(cdt, cdn,'exchange_rate', rate);
                        frappe.model.set_value(cdt, cdn, 'amount', row.currency_amount*rate)
                    }
                    frm.refresh_fields()
            })
        })
    }      
}

