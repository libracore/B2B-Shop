#
# matrix_tools.py
#
# Copyright (C) libracore, 2017
# https://www.libracore.com or https://github.com/libracore
#
# For information on ERPNext, refer to https://erpnext.org/
#
# Execute with $ bench execute b2bshop.scripts.matrix_tools.<function>
#

import frappe

def get_master_dict():
	master_dict = get_group_structure()
	for main_group in master_dict:
		for sub_group in master_dict[main_group]:
			master_dict[main_group][sub_group]["templates"] = {}
			templates = get_all_templates(sub_group)
			for template in templates:
				master_dict[main_group][sub_group]["templates"][template.item_code] = {}
				master_dict[main_group][sub_group]["templates"][template.item_code]["specs"] = get_specs(template.item_code)
				master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"] = {}
				attributes = get_attributes(template.item_code)
				for attribute in attributes:
					_p_attr = get_possibily_atribute_values(template.item_code, attribute.attribute)
					master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"][attribute.attribute] = []
					for p_attr in _p_attr:
						master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"][attribute.attribute].append(p_attr.attribute_value)
						
				if len(master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"]) == 1:
					attris = []
					for key in master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"]:
						attris.append(key)
					master_dict[main_group][sub_group]["templates"][template.item_code]["items"] = get_itemcodes_and_attribute_values_based_on_parent_and_1_dimensional_attributes(attris[0], template.item_code)
					
						
				if len(master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"]) == 2:
					attris = []
					for key in master_dict[main_group][sub_group]["templates"][template.item_code]["attributes"]:
						attris.append(key)
					master_dict[main_group][sub_group]["templates"][template.item_code]["items"] = get_itemcodes_and_attribute_values_based_on_parent_and_2_dimensional_attributes(attris[0], attris[1], template.item_code)
					
	return master_dict

def get_specs_for_modal():
	master_dict = get_group_structure()
	for main_group in master_dict:
		for sub_group in master_dict[main_group]:
			master_dict[main_group][sub_group]["templates"] = {}
			templates = get_all_templates(sub_group)
			for template in templates:
				master_dict[main_group][sub_group]["templates"][template.item_code] = {}
				#master_dict[main_group][sub_group]["templates"][template.item_code]["specs"] = get_specs(template.item_code)
				attributes = get_attributes(template.item_code)
				for attribute in attributes:
					if attribute.attribute == 'Colour':
						if not attribute.attribute in master_dict[main_group][sub_group]["templates"][template.item_code]:
							master_dict[main_group][sub_group]["templates"][template.item_code][attribute.attribute] = {}
							_items = get_items_of_template(template.item_code)
							_master_items = []
							for items in _items:
								for item in items:
									_master_items.append(item)
							master_items = "', '".join(_master_items)
							colours = get_colours_of_templateitems(master_items)
							for _colour in colours:
								for colour in _colour:
									master_dict[main_group][sub_group]["templates"][template.item_code][attribute.attribute][colour] = {}
									spec = get_one_item_spec_per_template_and_colour(template.item_code, colour)
									master_dict[main_group][sub_group]["templates"][template.item_code][attribute.attribute][colour]["image"] = spec[0].image
									master_dict[main_group][sub_group]["templates"][template.item_code][attribute.attribute][colour]["description"] = spec[0].description

	return master_dict
	
def get_one_item_spec_per_template_and_colour(template, colour):
	sql_query = """SELECT t1.description, t1.image
		FROM ((`tabItem` AS t1
		INNER JOIN `tabItem Variant Attribute` AS t2 ON t1.variant_of = t2.parent)
		INNER JOIN `tabItem Variant Attribute`AS t3 ON t1.item_code = t3.parent)
		WHERE t2.parent = '{0}'
		AND t3.attribute_value = '{1}'
		AND t1.show_variant_in_website = '1'
		LIMIT 1""".format(template, colour)
	spec = frappe.db.sql(sql_query, as_dict=True)
	return spec

def get_items_of_template(template):
	sql_query = """SELECT t1.item_code
		FROM `tabItem` AS t1
		WHERE t1.variant_of = '{0}'
		AND t1.show_variant_in_website = '1'""".format(template)
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items
	
def get_colours_of_templateitems(items):
	sql_query = """SELECT DISTINCT t1.attribute_value
		FROM `tabItem Variant Attribute` AS t1
		WHERE t1.parent IN ('{0}')
		AND t1.attribute = 'Colour'""".format(items)
	all_items = frappe.db.sql(sql_query, as_list=True)
	return all_items

def get_group_structure():
	master_dict = {}
	main_groups = get_all_main_groups()
	for main_group in main_groups:
		master_dict[main_group.name] = {}
		sub_groups = get_all_sub_groups(main_group.name)
		for sub_group in sub_groups:
			master_dict[main_group.name][sub_group.name] = {}
	return master_dict

def get_all_main_groups():
	sql_query = """SELECT t1.name
		FROM `tabItem Group` AS t1
		WHERE t1.is_group = '1'
		AND t1.show_in_website = '1'"""
	all_main_groups = frappe.db.sql(sql_query, as_dict=True)
	return all_main_groups

def get_all_sub_groups(main_group):
	sql_query = """SELECT t1.name
		FROM `tabItem Group` AS t1
		WHERE t1.is_group = '0'
		AND t1.parent_item_group = '{0}'
		AND t1.show_in_website = '1'""".format(main_group)
	all_sub_groups = frappe.db.sql(sql_query, as_dict=True)
	return all_sub_groups

def get_all_templates(sub_group):
	sql_query = """SELECT t1.item_code
		FROM `tabItem` AS t1
		WHERE t1.item_group = '{0}'
		AND t1.has_variants = '1'
		AND t1.show_in_website = '1'""".format(sub_group)
	all_templates = frappe.db.sql(sql_query, as_dict=True)
	return all_templates

def get_attributes(template):
	sql_query = """SELECT t1.attribute
		FROM `tabItem Variant Attribute` AS t1
		WHERE t1.parent = '{0}'""".format(template)
	attributes = frappe.db.sql(sql_query, as_dict=True)
	return attributes
	
def get_possibily_atribute_values(template, attribute):
	items = get_all_items_for_attribute_values(template, attribute)
	sql_query = """SELECT DISTINCT t1.attribute_value
		FROM `tabItem Variant Attribute` AS t1
		WHERE t1.attribute = '{0}'
		AND t1.parent IN ('{1}')
		ORDER BY t1.attribute_value""".format(attribute, "', '".join(items))
	possibily_atribute_values = frappe.db.sql(sql_query, as_dict=True)
	return possibily_atribute_values

	
def get_all_items_for_attribute_values(template, attribute):
	sql_query = """SELECT t1.item_code
		FROM `tabItem` AS t1
		WHERE t1.variant_of = '{0}'
		AND t1.show_variant_in_website = '1'""".format(template)
	_items = frappe.db.sql(sql_query, as_dict=True)
	items = []
	for _item in _items:
		items.append(_item.item_code)
	return items
	
def get_itemcodes_and_attribute_values_based_on_parent_and_2_dimensional_attributes(attr_1, attr_2, parent):
	sql_query = """SELECT t1.name AS item_code, t2.attribute_value AS `{0}`, t3.attribute_value AS `{1}`
		FROM ((`tabItem` AS t1
		INNER JOIN `tabItem Variant Attribute` AS t2 ON t1.name = t2.parent)
		INNER JOIN `tabItem Variant Attribute` AS t3 ON t1.name = t3.parent)
		WHERE t2.attribute = '{0}'
		AND t2.attribute_value IS NOT NULL
		AND t3.attribute = '{1}'
		AND t3.attribute_value IS NOT NULL
		AND t1.variant_of = '{2}'
		AND t1.show_variant_in_website = '1'
		ORDER BY t2.attribute_value, t3.attribute_value""".format(attr_1, attr_2, parent)

	master_dict = frappe.db.sql(sql_query, as_dict=True)
	return master_dict
	
def get_itemcodes_and_attribute_values_based_on_parent_and_1_dimensional_attributes(attr_1, parent):
	sql_query = """SELECT t1.name AS item_code, t2.attribute_value AS `{0}`
		FROM (`tabItem` AS t1
		INNER JOIN `tabItem Variant Attribute` AS t2 ON t1.name = t2.parent)
		WHERE t2.attribute = '{0}'
		AND t2.attribute_value IS NOT NULL
		AND t1.variant_of = '{1}'
		AND t1.show_variant_in_website = '1'
		ORDER BY t2.attribute_value""".format(attr_1, parent)

	master_dict = frappe.db.sql(sql_query, as_dict=True)
	return master_dict

def get_specs(template):
	sql_query = """SELECT t1.description, t1.image
		FROM `tabItem` AS t1
		WHERE t1.item_code = '{0}'
		AND t1.has_variants = '1'
		AND t1.show_in_website = '1'""".format(template)
	specs = frappe.db.sql(sql_query, as_dict=True)
	return specs