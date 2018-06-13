from __future__ import unicode_literals
import frappe
from b2bshop.scripts.matrix_tools import get_master_dict

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.items_for_page = get_master_dict()
	context.bg_img = get_settings("bg_img")
	context.acc_colour = get_settings("acc_colour")
	context.sel_acc_colour = get_settings("sel_acc_colour")
	context.cart_btn_colour = get_settings("cart_btn_colour")
	context.sel_cart_btn_colour = get_settings("sel_cart_btn_colour")
	context.acc_img = get_settings("acc_img")
	context.popup_colour = get_settings("popup_colour")
	context.spec_colour = get_settings("spec_colour")
	context.order_colour = get_settings("order_colour")
	context.spec_mark_colour = get_settings("spec_mark_colour")
	context.order_mark_colour = get_settings("order_mark_colour")
	context.tables_hatching = get_settings("tables_hatching")
	if context.tables_hatching == "1":
		context.tables_hatching_colour = get_settings("tables_hatching_colour")
	context.order_hover_colour = get_settings("order_hover_colour")
	context.spec_hover_colour = get_settings("spec_hover_colour")


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
