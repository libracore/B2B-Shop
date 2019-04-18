import frappe
from erpnext.stock.utils import get_bin


def get_all_items_of_refsize_for_webshop():
	sql_query = """SELECT t1.`name`
		FROM `tabItem` AS t1
		INNER JOIN `tabItem Variant Attribute` AS t2 ON t1.`name` = t2.`parent`
		WHERE t1.`show_variant_in_website` = '1'
		AND t2.`attribute` = 'Size'
		AND t2.`attribute_value` = '42'"""
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items

def get_item_details(item):
	sql_query = """SELECT t1.`image`, t1.`item_name`, t1.`item_group`, t1.`web_long_description`, t2.`is_pre_sale`, t1.`sirv_link`
		FROM `tabItem` AS t1
		INNER JOIN `tabItem Group` AS t2 ON t1.`item_group` = t2.`name`
		WHERE t1.`name` = '{0}'""".format(item)
	item_details = frappe.db.sql(sql_query, as_list=True)
	return item_details

def get_all_item_groups():
	sql_query = """SELECT t1.`name`
		FROM `tabItem Group` AS t1
		WHERE t1.`show_in_website` = '1'"""
	item_groups = frappe.db.sql(sql_query, as_list=True)
	return item_groups
	
def get_parent_group(group):
	sql_query = """SELECT t1.`parent_item_group`
		FROM `tabItem Group` AS t1
		WHERE t1.`show_in_website` = '1'
		AND t1.`name` = '{0}'""".format(group)
	parent_group = frappe.db.sql(sql_query, as_list=True)
	return parent_group
	
def get_all_corresponding_sizes(item):
	template = get_template(item)
	color = get_color(item)
	_all_items = get_all_items(template[0][0])
	all_items = []
	for item in _all_items:
		all_items.append(item[0])
	
	sql_query = """SELECT DISTINCT t1.`attribute_value`, t1.`parent`
		FROM `tabItem Variant Attribute` AS t1
		INNER JOIN `tabItem Variant Attribute` AS t2 ON t1.`parent` = t2.`parent`
		WHERE t1.`attribute` = 'Size'
		AND t1.`parent` IN ({0})
		AND t2.`attribute_value` = '{1}'
		ORDER BY t1.`attribute_value` ASC""".format("'"+"', '".join(all_items)+"'", color[0][0])
	all_corresponding_sizes = frappe.db.sql(sql_query, as_list=True)
	return all_corresponding_sizes
	
def get_all_items(template):
	sql_query = """SELECT `name`
		FROM `tabItem`
		WHERE `variant_of` = '{0}'
		AND `show_variant_in_website` = '1'""".format(template)
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items
	
def get_template(item):
	sql_query = """SELECT `variant_of`
		FROM `tabItem`
		WHERE `name` = '{0}'""".format(item)
	template = frappe.db.sql(sql_query, as_list=True)
	return template
	
def get_color(item):
	sql_query = """SELECT `attribute_value`
		FROM `tabItem Variant Attribute`
		WHERE `parent` = '{0}'
		AND `attribute` = 'Colour'""".format(item)
	color = frappe.db.sql(sql_query, as_list=True)
	return color

def get_warehouses():
	sql_query = """SELECT `warehouse`
		FROM `tabB2B Warehouse`"""
	warehouses = frappe.db.sql(sql_query, as_list=True)
	return warehouses

def get_item_stock(item):
	qty = 0
	warehouses = get_warehouses()
	for warehouse in warehouses:
		bin = get_bin(item, warehouse[0])
		qty = qty + bin.actual_qty
	if qty > 0:
		return '<span style="color: green;"><i class="fa fa-check"></i></span>'
	else:
		return '<span style="color: red;"><i class="fa fa-times"></i></span>'

def get_item_slideshow(item):
	sql_query = """SELECT `slideshow`
		FROM `tabItem`
		WHERE `name` = '{0}'""".format(item)
	slideshow = frappe.db.sql(sql_query, as_list=True)
	return slideshow

def get_slideshow_images(slideshow):
	sql_query = """SELECT `image`
		FROM `tabWebsite Slideshow Item`
		WHERE `parent` = '{0}'
		ORDER BY `idx` ASC""".format(slideshow)
	slideshow_images = frappe.db.sql(sql_query, as_list=True)
	return slideshow_images

def get_all_items_without_size():
	sql_query = """SELECT DISTINCT t1.`parent`
		FROM `tabItem Variant Attribute` AS t1
		WHERE t1.`attribute` <> 'Size'
		AND NOT EXISTS (SELECT t2.`parent` FROM `tabItem Variant Attribute` AS t2  WHERE t1.`parent` = t2.`parent` AND t2.`attribute` = 'Size')"""
	_all_items_without_size = frappe.db.sql(sql_query, as_list=True)
	all_items = []
	for item in _all_items_without_size:
		all_items.append(item[0])
	sql_query = """SELECT DISTINCT t1.`name`
		FROM `tabItem` AS t1
		WHERE t1.`name` IN ({0})
		AND t1.`has_variants` = '0'
		AND t1.`show_variant_in_website` = '1'""".format("'"+"', '".join(all_items)+"'")
	all_items_without_size = frappe.db.sql(sql_query, as_list=True)
	return all_items_without_size
