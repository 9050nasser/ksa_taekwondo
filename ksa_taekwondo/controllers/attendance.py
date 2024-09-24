import frappe
from datetime import datetime
@frappe.whitelist()
def attendance_validation(attendanc_doc, doc_event):
    shift_start_time,shift_end_time = frappe.db.get_value('Shift Type',attendanc_doc.shift,['start_time','end_time']) 
    date_format = '%Y-%m-%d %H:%M:%S'
    if isinstance(attendanc_doc.in_time,str):
        datein = datetime.strptime(attendanc_doc.in_time, date_format).time()
    else:
        datein = attendanc_doc.in_time
    if isinstance(attendanc_doc.out_time,str):
        dateout = datetime.strptime(attendanc_doc.out_time, date_format).time()
    else:
        dateout = attendanc_doc.out_time
    start_time = datein
    end_time = dateout
    start_time_shift = datetime.strptime(str(shift_start_time), "%H:%M:%S")
    end_time_shift = datetime.strptime(str(shift_end_time), "%H:%M:%S")
    if start_time and start_time_shift:
        attendanc_doc.late_entry_hours = ((start_time - start_time_shift).total_seconds())/ (60 * 60)
    if end_time and end_time_shift:
        attendanc_doc.early_exit_hours = ((end_time_shift - end_time).total_seconds())/ (60 * 60)

