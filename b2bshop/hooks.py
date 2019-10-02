# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "b2bshop"
app_title = "B2B Shop"
app_publisher = "libracore"
app_description = "ERPNext App for easy web orders"
app_icon = "octicon octicon-package"
app_color = "grey"
app_email = "info@libracore.com"
app_license = "AGPL"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/b2bshop/css/b2bshop.css"
# app_include_js = "/assets/b2bshop/js/b2bshop.js"

# include js, css files in header of web template
web_include_css = "/assets/b2bshop/css/rubirosa.css"
web_include_js = "/assets/b2bshop/js/woocommerce_like.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "login"

# website user home page (by Role)
role_home_page = {
	"Customer": "start"
}

website_context = {
	"base_template_path": "templates/b2b_base.html"
}

jenv = {
	"methods": [
		"get_all_items_of_refsize_for_webshop:b2bshop.utils.get_all_items_of_refsize_for_webshop",
		"get_item_details:b2bshop.utils.get_item_details",
		"get_all_item_groups:b2bshop.utils.get_all_item_groups",
		"get_parent_group:b2bshop.utils.get_parent_group",
		"get_all_corresponding_sizes:b2bshop.utils.get_all_corresponding_sizes",
		"get_item_stock:b2bshop.utils.get_item_stock",
		"get_item_slideshow:b2bshop.utils.get_item_slideshow",
		"get_slideshow_images:b2bshop.utils.get_slideshow_images",
		"get_all_items_without_size:b2bshop.utils.get_all_items_without_size"
	]
}


# Website user home page (by function)
# get_website_user_home_page = "b2bshop.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "b2bshop.install.before_install"
# after_install = "b2bshop.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "b2bshop.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"b2bshop.tasks.all"
# 	],
# 	"daily": [
# 		"b2bshop.tasks.daily"
# 	],
# 	"hourly": [
# 		"b2bshop.tasks.hourly"
# 	],
# 	"weekly": [
# 		"b2bshop.tasks.weekly"
# 	]
# 	"monthly": [
# 		"b2bshop.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "b2bshop.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "b2bshop.event.get_events"
# }
fixtures = ["Custom Field"]
