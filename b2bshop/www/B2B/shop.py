from __future__ import unicode_literals
import frappe
from b2bshop.scripts.matrix_tools import get_master_dict, get_specs_for_modal

no_cache = 1
no_sitemap = 1

def get_context(context):
    #item master dict and specs
    context.items_for_page = get_master_dict()
    context.item_specs = get_specs_for_modal()

    #background image
    context.bg_img = get_settings("bg_img")

    #style select
    context.style = get_settings("style_select")

    # section for accordion
    if context.style == "Accordion":
        context.spec_based_on = get_settings("spezification_select")
        context.acc_colour = get_settings("acc_colour")
        context.sel_acc_colour = get_settings("sel_acc_colour")
        context.acc_img = get_settings("acc_img")
        context.spec_colour = get_settings("spec_colour")
        context.order_colour = get_settings("order_colour")
        context.spec_mark_colour = get_settings("spec_mark_colour")
        context.order_mark_colour = get_settings("order_mark_colour")
        context.tables_hatching = get_settings("tables_hatching")
        if context.tables_hatching == "1":
            context.tables_hatching_colour = get_settings("tables_hatching_colour")
        context.order_hover_colour = get_settings("order_hover_colour")
        context.spec_hover_colour = get_settings("spec_hover_colour")

    #other settings
    context.cart_btn_colour = get_settings("cart_btn_colour")
    context.sel_cart_btn_colour = get_settings("sel_cart_btn_colour")
    context.popup_colour = get_settings("popup_colour")

def get_settings(setting):
    sql_query = """SELECT `value`
        FROM `tabSingles`
        WHERE `doctype` = 'B2B Settings'
        AND `field` = '{0}'""".format(setting)
    __setting = frappe.db.sql(sql_query, as_dict=True)
    setting = ""
    for _setting in __setting:
        setting = _setting.value
    return setting

def get_all_parent_groups():
    sql_query = """SELECT `name`
        FROM `tabItem Group`
        WHERE `is_group` = '1'"""
    all_parent_groups = frappe.db.sql(sql_query, as_list=True)
    return all_parent_groups

def get_all_sub_groups_of_parent(parent):
    sql_query = """SELECT `name`
        FROM `tabItem Group`
        WHERE `is_group` = '0'
        AND `parent_item_group` = '{0}'""".format(parent)
    all_sub_groups = frappe.db.sql(sql_query, as_list=True)
    return all_sub_groups

def get_all_templates_of_sub_group(sub_group):
    sql_query = """SELECT `name`
        FROM `tabItem`
        WHERE `has_variants` = '1'
        AND `item_group` = '{0}'""".format(sub_group)
    all_templates_of_sub_group = frappe.db.sql(sql_query, as_list=True)
    return all_templates_of_sub_group
