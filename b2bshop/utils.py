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
	sql_query = """SELECT t1.`image`, t1.`item_name`, t1.`item_group`, t1.`web_long_description`, t2.`is_pre_sale`, t1.`is_pre_order`
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
	if template:
		color = get_color(item)
		season = get_season(item)
		sole_color = get_sole_color(item)
		
		_all_items = get_all_items(template[0][0])
		all_items = []
		for item in _all_items:
			all_items.append(item[0])
		
		if color:
			# get all corresponding items of color
			color_sql_query = """SELECT DISTINCT
							`tabItem Variant Attribute`.`parent`
							FROM `tabItem Variant Attribute`
							WHERE `tabItem Variant Attribute`.`attribute` = 'Colour'
							AND `tabItem Variant Attribute`.`attribute_value` = '{color}'
							AND `tabItem Variant Attribute`.`parent` IN ({parent_list})""".format(parent_list="'"+"', '".join(all_items)+"'", color=color[0][0])
							
			if season:
				if sole_color:
					# get all corresponding items of season, color and sole color
					season_sql_query = """SELECT DISTINCT
									`tabItem Variant Attribute`.`parent`
									FROM `tabItem Variant Attribute`
									WHERE `tabItem Variant Attribute`.`attribute` = 'Season'
									AND `tabItem Variant Attribute`.`attribute_value` = '{season}'
									AND `tabItem Variant Attribute`.`parent` IN ({color_sql_query})""".format(color_sql_query=color_sql_query, season=season[0][0])
									
					sole_color_sql_query = """SELECT DISTINCT
									`tabItem Variant Attribute`.`parent`
									FROM `tabItem Variant Attribute`
									WHERE `tabItem Variant Attribute`.`attribute` = 'Sole Colour'
									AND `tabItem Variant Attribute`.`attribute_value` = '{sole_color}'
									AND `tabItem Variant Attribute`.`parent` IN ({season_sql_query})""".format(season_sql_query=season_sql_query, sole_color=sole_color[0][0])

					sql_query = """SELECT DISTINCT
									`tabItem Variant Attribute`.`attribute_value`,
									`tabItem Variant Attribute`.`parent`
									FROM `tabItem Variant Attribute`
									WHERE `tabItem Variant Attribute`.`attribute` = 'Size'
									AND `tabItem Variant Attribute`.`parent` IN ({sole_color_sql_query})
									ORDER BY `tabItem Variant Attribute`.`attribute_value` ASC""".format(sole_color_sql_query=sole_color_sql_query)
				else:
					# get all corresponding items of season and color
					season_sql_query = """SELECT DISTINCT
									`tabItem Variant Attribute`.`parent`
									FROM `tabItem Variant Attribute`
									WHERE `tabItem Variant Attribute`.`attribute` = 'Season'
									AND `tabItem Variant Attribute`.`attribute_value` = '{season}'
									AND `tabItem Variant Attribute`.`parent` IN ({color_sql_query})""".format(color_sql_query=color_sql_query, season=season[0][0])

					sql_query = """SELECT DISTINCT
									`tabItem Variant Attribute`.`attribute_value`,
									`tabItem Variant Attribute`.`parent`
									FROM `tabItem Variant Attribute`
									WHERE `tabItem Variant Attribute`.`attribute` = 'Size'
									AND `tabItem Variant Attribute`.`parent` IN ({season_sql_query})
									ORDER BY `tabItem Variant Attribute`.`attribute_value` ASC""".format(season_sql_query=season_sql_query)
							
			else:
				# get all corresponding items of color without season
				no_season_sql_query = """SELECT DISTINCT
								`tabItem Variant Attribute`.`parent`
								FROM `tabItem Variant Attribute`
								WHERE `tabItem Variant Attribute`.`attribute` = 'Season'
								AND `tabItem Variant Attribute`.`parent` IN ({color_sql_query})""".format(color_sql_query=color_sql_query)
				
				sql_query = """SELECT DISTINCT
								`tabItem Variant Attribute`.`attribute_value`,
								`tabItem Variant Attribute`.`parent`
								FROM `tabItem Variant Attribute`
								WHERE `tabItem Variant Attribute`.`attribute` = 'Size'
								AND `tabItem Variant Attribute`.`parent` IN ({color_sql_query})
								AND `tabItem Variant Attribute`.`parent` NOT IN ({no_season_sql_query})
								ORDER BY `tabItem Variant Attribute`.`attribute_value` ASC""".format(color_sql_query=color_sql_query, no_season_sql_query=no_season_sql_query)
							
		else:
			# fallback, should never be used
			sql_query = """SELECT DISTINCT
								`tabItem Variant Attribute`.`attribute_value`,
								`tabItem Variant Attribute`.`parent`
								FROM `tabItem Variant Attribute`
								WHERE `tabItem Variant Attribute`.`attribute` = 'Size'
								AND `tabItem Variant Attribute`.`parent` IN ({parent_list})
								ORDER BY `tabItem Variant Attribute`.`attribute_value` ASC""".format(parent_list="'"+"', '".join(all_items)+"'")
							
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
	
def get_season(item):
	sql_query = """SELECT `attribute_value`
		FROM `tabItem Variant Attribute`
		WHERE `parent` = '{0}'
		AND `attribute` = 'Season'""".format(item)
	season = frappe.db.sql(sql_query, as_list=True)
	return season

def get_sole_color(item):
	sql_query = """SELECT `attribute_value`
		FROM `tabItem Variant Attribute`
		WHERE `parent` = '{0}'
		AND `attribute` = 'Sole Colour'""".format(item)
	sole_color = frappe.db.sql(sql_query, as_list=True)
	return sole_color

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
	
def get_item_stock_of_default(item, warehouse):
	qty = 0
	bin = get_bin(item, warehouse)
	qty = bin.actual_qty
	return qty
	
@frappe.whitelist()
def check_and_update_warehouse_in_quotation(item, qty):
	default_warehouse = frappe.get_doc("Item", item).default_warehouse
	if qty:
		qty = int(qty)
	if get_item_stock_of_default(item, default_warehouse) < qty:
		customer = get_party().name
		_quotation = frappe.db.sql("""SELECT `name` FROM `tabQuotation` WHERE `customer_name` = '{customer}' AND `docstatus` = 0 LIMIT 1""".format(customer=customer), as_list=True)[0][0]
		quotation = frappe.get_doc("Quotation", _quotation)
		for quotation_item in quotation.items:
			if quotation_item.item_code == item:
				fallback_warehouse = get_fallback_warehouse(default_warehouse)
				quotation_item.warehouse = fallback_warehouse
				fallback_qty = get_item_stock_of_default(item, fallback_warehouse)
				quotation_item.actual_qty = fallback_qty
				quotation_item.projected_qty = fallback_qty
				quotation.save()
	
def get_fallback_warehouse(default_warehouse):
	warehouses = get_warehouses()
	for warehouse in warehouses:
		if warehouse[0] != default_warehouse:
			return warehouse[0]
	
def get_party():
	user = frappe.session.user
	contact = frappe.get_doc("Contact", frappe.db.sql("""SELECT `name` FROM `tabContact` WHERE `user` = '{user}' OR `email_id` = '{user}' LIMIT 1""".format(user=user), as_list=True)[0][0])
	for link in contact.links:
		if link.link_doctype == 'Customer':
			party = link.link_name
	return frappe.get_doc("Customer", party)
	

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
