// Copyright (c) 2023, Trigger Solutions and contributors
// For license information, please see license.txt
frappe.ui.form.on("Reward Setting", "onload", function(frm) {
    frm.set_query("account", function() {
        return {
            "filters": {
                "account_type": "Payable",
                "is_group": 0
            }
        };
    });
});
frappe.ui.form.on('Reward Setting', {
	// refresh: function(frm) {

	// }
});
