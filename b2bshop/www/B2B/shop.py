from __future__ import unicode_literals
import frappe
from b2bshop.scripts.matrix_tools import get_master_dict

def get_context(context):
	context.items_for_page = get_master_dict()
