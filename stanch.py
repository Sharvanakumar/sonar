import frappe
import os

@frappe.whitelist(allow_guest=True)
def getMeta(**args):
	doctype = args['doctype']
	# print(frappe.form_dict.get("Purchase Invoice"))
	try:
		return frappe.get_meta(doctype)
	except Exception as err:
		print(err)

@frappe.whitelist(allow_guest=True)
def getDoctypes():
	parent_doctypes = frappe.get_list('DocType',filters={'istable':0},pluck='name')
	parent_doctypes.append("Doctype")
	return parent_doctypes


@frappe.whitelist(allow_guest=True)
def getDocIds(**args):
	document = frappe.get_list(args['doctype'],pluck='name')
	return document

@frappe.whitelist(allow_guest=True)
def get_global_default():
	return frappe.defaults.get_defaults()
	
@frappe.whitelist(allow_guest=True)
def getGlobalDefaultData():
	global_defaults = frappe.get_doc("Global Defaults")
	return global_defaults

@frappe.whitelist(allow_guest=True)
def get_locals_details():
	localsObject = {}
	companies = frappe.get_list("Company",pluck='name',fields="*")
	currencies = frappe.get_list("Currency",pluck='name',fields="*")
	company_details = []
	
	for i in companies:
		company = frappe.get_doc("Company",i)
		company_details.append(company)
		
	currency_details = []
	for i in currencies:
		currency = frappe.get_doc("Currency",i)
		if(currency.enabled):
			currency_details.append(currency)
	
	
	localsObject['company_details'] = company_details
	localsObject['currency_details'] = currency_details
	
	# return frappe.get_doc("Currency","INR")

	return localsObject

@frappe.whitelist(allow_guest=True)
def generate_file(doctype):
    base_path = '/stanch_app/src/client_scripts/Form'
    file_name = f"{doctype.lower().replace(' ', '_')}.ts"
    file_path = os.path.join(base_path, file_name)

    if os.path.exists(file_path):
        return f"File {file_name} already exists. No need to generate."

    file_content = f'''
import FormClass from "./classes";
import FormManager from "./classes/FormManager";

class {doctype.replace(' ', '')} extends FormClass {{
    constructor() {{
        super();
        this.csMethods = {{

        }};

        this.customMethods = {{

        }};
    }}

    // Write methods here
}}

export default {doctype.replace(' ', '')};
'''

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(file_content)
        return f"File {file_name} created successfully at {file_path}"
	
@frappe.whitelist(allow_guest=True)
def get_boot_file():
	print(dir(frappe.boot))
	return "hi"