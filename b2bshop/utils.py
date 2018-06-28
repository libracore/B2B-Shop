import frappe

def get_all_parent_groups():
	sql_query = """SELECT `name`
		FROM `tabItem Group`
		WHERE `is_group` = '1'
		AND `show_in_website` = '1'"""
	all_parent_groups = frappe.db.sql(sql_query, as_list=True)
	return all_parent_groups
	
def get_all_sub_groups_of_parent(parent):
	sql_query = """SELECT `name`
		FROM `tabItem Group`
		WHERE `is_group` = '0'
		AND `parent_item_group` = '{0}'
		AND `show_in_website` = '1'""".format(parent)
	all_sub_groups = frappe.db.sql(sql_query, as_list=True)
	return all_sub_groups
	
def get_all_templates_of_sub_group(sub_group):
	sql_query = """SELECT `name`
		FROM `tabItem`
		WHERE `has_variants` = '1'
		AND `item_group` = '{0}'
		AND `show_in_website` = '1'""".format(sub_group)
	all_templates_of_sub_group = frappe.db.sql(sql_query, as_list=True)
	return all_templates_of_sub_group
	
def check_if_with_size(template):
	sql_query = """SELECT `attribute`
		FROM `tabItem Variant Attribute`
		WHERE `parent` = '{0}'""".format(template)
	all_attributes_of_template = frappe.db.sql(sql_query, as_list=True)
	
	has_size = False
	
	for attribute in all_attributes_of_template:
		if attribute[0] == "Size":
			has_size = True
	return has_size

def get_code_and_colors(template):
	_all_items = get_all_items(template)
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	
	code_and_colors = get_all_colors_of_items(all_items)
	return code_and_colors
	
def get_all_items(template):
	sql_query = """SELECT `name`
		FROM `tabItem`
		WHERE `variant_of` = '{0}'""".format(template)
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items
	
def get_all_colors_of_items(all_items):
	sql_query = """SELECT DISTINCT `attribute_value`
		FROM `tabItem Variant Attribute`
		WHERE `parent` IN ({0})
		AND `attribute` = 'Colour'
		ORDER BY `attribute_value` ASC""".format("'"+"', '".join(all_items)+"'")
	all_colors = frappe.db.sql(sql_query, as_list=True)
	return all_colors

def get_all_sizes_with_codes_to_color_of_item(all_items):
	sql_query = """SELECT DISTINCT `attribute_value`, `parent`
		FROM `tabItem Variant Attribute`
		WHERE `parent` IN ({0})
		AND `attribute` = 'Size'
		ORDER BY `attribute_value` ASC""".format("'"+"', '".join(all_items)+"'")
	all_sizes = frappe.db.sql(sql_query, as_list=True)
	return all_sizes
	
def get_all_items_to_color_size(all_items):
	sql_query = """SELECT DISTINCT `attribute_value`, `parent`
		FROM `tabItem Variant Attribute`
		WHERE `parent` IN ({0})
		AND `attribute` = 'Size'
		ORDER BY `attribute_value` ASC""".format("'"+"', '".join(all_items)+"'")
	all_sizes = frappe.db.sql(sql_query, as_list=True)
	return all_sizes
	
def get_all_items_to_color(all_items, color):
	sql_query = """SELECT `parent`
		FROM `tabItem Variant Attribute`
		WHERE `parent` IN ({0})
		AND `attribute_value` = '{1}'""".format("'"+"', '".join(all_items)+"'", color)
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items

def get_code_and_sizes(template, color):
	_all_items = get_all_items(template)
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	_all_items = get_all_items_to_color(all_items, color)
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	return get_all_items_to_color_size(all_items)
	
def get_item_img_and_desc(template, color):
	_all_items = get_all_items(template)
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	_all_items = get_all_items_to_color(all_items, color)
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	item = ""
	__item = get_item_46(all_items)
	for _item in __item:
		item = _item[0]
	sql_query = """SELECT `image`, `description`
		FROM `tabItem`
		WHERE `name` = '{0}'""".format(item)
	item_specs = frappe.db.sql(sql_query, as_dict=True)
	return item_specs
	
def get_item_46(all_items):
	sql_query = """SELECT `parent`
		FROM `tabItem Variant Attribute`
		WHERE `parent` IN ({0})
		AND `attribute_value` = '46'""".format("'"+"', '".join(all_items)+"'")
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items