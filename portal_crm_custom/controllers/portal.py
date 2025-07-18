# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import pdb
from datetime import datetime
from markupsafe import Markup

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError,UserError
from odoo.http import request
from odoo.addons.portal.controllers import portal as payment_portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
import logging

_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug("Cannot `import xlrd`.")
try:
    import csv 
except ImportError:
    _logger.debug("Cannot `import csv`.")
try:
    import xlwt
except ImportError:
    _logger.debug("Cannot `import xlwt`.")
try:
    import cStringIO
except ImportError:
    _logger.debug("Cannot `import cStringIO`.")
try:
    import base64
except ImportError:
    _logger.debug("Cannot `import base64`.")


class CustomerPortal(payment_portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "crm_lead_count" in counters:
            values["crm_lead_count"] = 1

        return values

    def _prepare_crm_domain(self, partner):
        return [("type", "=", 'lead')]

    def _prepare_return_crm_domain(self, partner):
        return [("user_id", "=", [partner.id]),("type", "=", 'lead')]

    def _get_crm_lead_searchbar_sortings(self):
        return {
            "name": {"label": _("Reference"), "order": "name"},
        }

    def _prepare_crm_lead_portal_rendering_values(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        return_crm_lead_page=False,
        **kwargs,
    ):
        Leads = request.env["crm.lead"].sudo()

        if not sortby:
            sortby = "name"

        partner = request.env.user
        values = self._prepare_portal_layout_values()

        if return_crm_lead_page:
            url = "/my/crm/return"
            domain = self._prepare_return_crm_domain(partner)
        else:
            url = "/my/crm/lead"
            domain = self._prepare_crm_domain(partner)

        searchbar_sortings = self._get_crm_lead_searchbar_sortings()

        sort_order = searchbar_sortings[sortby]["order"]

        pager_values = portal_pager(
            url=url,
            total=Leads.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
        )
        domain = False
        if request.env.user.affiliate_id: 
            domain = [("affiliate_name", "=", request.env.user.affiliate_id.id),("type", "=", 'lead')] #domain for affiliate
        else:
            domain = [("full_name", "=", request.env.user.partner_id.id),("type", "=", 'lead')] #domain for customer
        orders = Leads.search(
            domain,
            order=sort_order,
            limit=self._items_per_page,
            offset=pager_values["offset"],
        )

        customers = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", request.env.company.id),
                ]
            )
        )

        values.update(
            {
                'type':'lead',
                "date": date_begin,
                "return_crm": orders.sudo() if return_crm_lead_page else Leads,
                "leads": orders.sudo() if not return_crm_lead_page else Leads,
                "customers": customers.sudo(),
                "page_name": "crm_lead",
                "pager": pager_values,
                "default_url": url,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "search_in": "content",
            }
        )

        return values

    @http.route(
        ["/my/crm/lead", "/my/crm/lead/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_crm_lead(self, **kwargs):
        values = self._prepare_crm_lead_portal_rendering_values(**kwargs)
        return request.render("portal_crm_custom.portal_my_crm_lead", values)

    @http.route(
        ["/my/crm/return", "/my/crm/return/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_crm_return(self, **kwargs):
        values = self._prepare_crm_lead_portal_rendering_values(
            return_crm_lead_page=True, **kwargs
        )
        return request.render("portal_crm_custom.portal_my_crm_return", values)

    @http.route(
        ["/my/crm/lead/<int:crm_lead_id>"], type="http", auth="user", website=True
    )
    def portal_crm_custom_lead_page(
        self,
        crm_lead_id,
        report_type=None,
        access_token=None,
        message=False,
        download=False,
        **kw,
    ):
        try:
            crm_lead_sudo = (
                request.env["crm.lead"].sudo().search([("id", "=", int(crm_lead_id))])
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        if report_type in ("html", "pdf", "text"):
            return self._show_report(
                model=crm_lead_sudo,
                report_type=report_type,
                report_ref="stock.action_report_lead",
                download=download,
            )

        backend_url = (
            f"/web#model={crm_lead_sudo._name}"
            f"&id={crm_lead_sudo.id}"
            f"&action={crm_lead_sudo._get_portal_return_action().id}"
            f"&view_type=form"
        )
        stages = request.env["crm.stage"].sudo().search([])
        customers = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", request.env.company.id),
                ]
            )
        )
        users = (
            request.env["res.users"]
            .sudo()
            .search([("company_id", "=", request.env.company.id)])
        )
        lost_reasons = request.env["crm.lost.reason"].sudo().search([])
        activity_type_ids = (
            request.env["mail.activity.type"]
            .sudo()
            .search(["|", ("res_model", "=", False), ("res_model", "=", "crm.lead")])
        )
        leads = request.env["crm.lead"].sudo().search([])
        values = {
            "lead": crm_lead_sudo if crm_lead_sudo else False,
            "stages": stages,
            "leads": leads,
            "customers": customers,
            "users": users,
            "lost_reasons": lost_reasons,
            "activity_type_ids": activity_type_ids,
            "message": message,
            "report_type": "html",
            "backend_url": backend_url,
            "res_company": crm_lead_sudo.company_id,  # Used to display correct company logo
        }

        return request.render("portal_crm_custom.lead_portal_template", values)

    @http.route(["/crm/schedule/activity"], type="http", auth="user", website=True)
    def crm_schedule_activity(
        self, report_type=None, access_token=None, message=False, download=False, **kw
    ):

        lead_id = kw.get("lead_id")
        activity_type_id = kw.get("activity_type_id")
        assign_to = kw.get("assign_to")
        due_date = kw.get("due_date")
        summary = kw.get("summary")
        request_body_text_editor_box = kw.get("request_body_text_editor_box")

        formated_duedate = False
        if due_date != "":
            due_date = due_date.replace("/", "-")
            dt = datetime.strptime(due_date, "%m-%d-%Y")
            formated_duedate = dt.strftime("%Y-%m-%d")

        lead = (
            request.env["crm.lead"].sudo().search([("id", "=", int(lead_id))], limit=1)
        )
        user = (
            request.env["res.users"]
            .sudo()
            .search([("id", "=", int(assign_to))], limit=1)
        )
        activity_type_id = (
            request.env["mail.activity.type"]
            .sudo()
            .search([("id", "=", int(activity_type_id))], limit=1)
        )

        if lead:
            lead.sudo().activity_schedule(
                activity_type_id=activity_type_id.id
                or lead.sudo()._default_activity_type().id,
                note=request_body_text_editor_box,
                date_deadline=formated_duedate or fields.date.today(),
                summary=summary,
                user_id=user.id,
            )
        return request.redirect(lead.get_portal_url())

    @http.route(["/crm/log/note"], type="http", auth="user", website=True)
    def crm_log_note(
        self, report_type=None, access_token=None, message=False, download=False, **kw
    ):

        lead_id = kw.get("lead_id")
        log_note_text_body = kw.get("log_note_text_body")
        portal_user_id = kw.get("portal_user_id")
        user_ids = set(request.httprequest.form.getlist("user_ids"))
        users_array = []
        if user_ids:
            for user in user_ids:
                users_array.append(int(user))

        lead = (
            request.env["crm.lead"].sudo().search([("id", "=", int(lead_id))], limit=1)
        )
        portal_user_id = (
            request.env["res.users"]
            .sudo()
            .search([("id", "=", int(portal_user_id))], limit=1)
        )
        users = request.env["res.users"].sudo().search([("id", "in", users_array)])
        partners = []
        if users:
            partners = users.mapped("partner_id").mapped("id")

        if lead:
            lead.sudo().message_post(
                body=Markup(log_note_text_body),
                message_type="notification",
                partner_ids=partners,
                subtype_xmlid="mail.mt_note",
                author_id=portal_user_id.id,
            )
        return request.redirect(lead.get_portal_url())


class CustomerPortalOpportunity(payment_portal.CustomerPortal):

    def _prepare_home_portal_values_opportunity(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "crm_lead_count" in counters:
            values["crm_lead_count"] = 1

        return values

    def _prepare_crm_domain_opportunity(self, partner):
        return [("type", "=", 'opportunity')]

    def _prepare_return_crm_domain_opportunity(self, partner):
        return [("user_id", "=", [partner.id]),("type", "=", 'opportunity')]

    def _get_crm_lead_searchbar_sortings_opportunity(self):
        return {
            "name": {"label": _("Reference"), "order": "name"},
        }

    def _prepare_crm_lead_portal_rendering_values_opportunity(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        return_crm_lead_page=False,
        **kwargs,
    ):
        Leads = request.env["crm.lead"].sudo()

        if not sortby:
            sortby = "name"

        partner = request.env.user
        values = self._prepare_portal_layout_values()

        if return_crm_lead_page:
            url = "/my/crm/return"
            domain = self._prepare_return_crm_domain_opportunity(partner)
        else:
            url = "/my/crm/opportunity"
            domain = self._prepare_crm_domain_opportunity(partner)
        # raise UserError(str(domain))

        searchbar_sortings = self._get_crm_lead_searchbar_sortings_opportunity()

        sort_order = searchbar_sortings[sortby]["order"]

        pager_values = portal_pager(
            url=url,
            total=Leads.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
        )
        domain = False
        if request.env.user.affiliate_id: 
            domain = [("affiliate_name", "=", request.env.user.affiliate_id.id),("type", "=", 'opportunity')] #domain for affiliate
        else:
            domain = [("full_name", "=", request.env.user.partner_id.id),("type", "=", 'opportunity')] #domain for customer
        orders = Leads.search(
            domain,
            order=sort_order,
            limit=self._items_per_page,
            offset=pager_values["offset"],
        )

        customers = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", request.env.company.id),
                ]
            )
        )

        values.update(
            {
                'type':'opportunity',
                "date": date_begin,
                "return_crm": orders.sudo() if return_crm_lead_page else Leads,
                "leads": orders.sudo() if not return_crm_lead_page else Leads,
                "customers": customers.sudo(),
                "page_name": "crm_lead",
                "pager": pager_values,
                "default_url": url,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "search_in": "content",
            }
        )

        return values

    @http.route(
        ["/my/crm/opportunity", "/my/crm/opportunity/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_crm_lead_opportunity(self, **kwargs):
        values = self._prepare_crm_lead_portal_rendering_values_opportunity(**kwargs)
        return request.render("portal_crm_custom.portal_my_crm_lead", values)

    @http.route(
        ["/my/crm/return", "/my/crm/return/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_crm_return_opportunity(self, **kwargs):
        values = self._prepare_crm_lead_portal_rendering_values_opportunity(
            return_crm_lead_page=True, **kwargs
        )
        return request.render("portal_crm_custom.portal_my_crm_return_opportunity", values)

    @http.route(
        ["/my/crm/opportunity/<int:crm_lead_id>"], type="http", auth="user", website=True
    )
    def portal_crm_custom_lead_page_opportunity(
        self,
        crm_lead_id,
        report_type=None,
        access_token=None,
        message=False,
        download=False,
        **kw,
    ):
        try:
            crm_lead_sudo = (
                request.env["crm.lead"].sudo().search([("id", "=", int(crm_lead_id))])
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        if report_type in ("html", "pdf", "text"):
            return self._show_report(
                model=crm_lead_sudo,
                report_type=report_type,
                report_ref="stock.action_report_lead",
                download=download,
            )

        backend_url = (
            f"/web#model={crm_lead_sudo._name}"
            f"&id={crm_lead_sudo.id}"
            f"&action={crm_lead_sudo._get_portal_return_action().id}"
            f"&view_type=form"
        )
        stages = request.env["crm.stage"].sudo().search([])
        customers = (
            request.env["res.partner"]
            .sudo()
            .search(
                [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "=", request.env.company.id),
                ]
            )
        )
        users = (
            request.env["res.users"]
            .sudo()
            .search([("company_id", "=", request.env.company.id)])
        )
        lost_reasons = request.env["crm.lost.reason"].sudo().search([])
        activity_type_ids = (
            request.env["mail.activity.type"]
            .sudo()
            .search(["|", ("res_model", "=", False), ("res_model", "=", "crm.lead")])
        )
        leads = request.env["crm.lead"].sudo().search([])
        values = {
            "lead": crm_lead_sudo if crm_lead_sudo else False,
            "stages": stages,
            "leads": leads,
            "customers": customers,
            "users": users,
            "lost_reasons": lost_reasons,
            "activity_type_ids": activity_type_ids,
            "message": message,
            "report_type": "html",
            "backend_url": backend_url,
            "res_company": crm_lead_sudo.company_id,  # Used to display correct company logo
        }

        return request.render("portal_crm_custom.lead_portal_template", values)

    @http.route(["/crm/schedule/activity"], type="http", auth="user", website=True)
    def crm_schedule_activity_opportunity(
        self, report_type=None, access_token=None, message=False, download=False, **kw
    ):

        lead_id = kw.get("lead_id")
        activity_type_id = kw.get("activity_type_id")
        assign_to = kw.get("assign_to")
        due_date = kw.get("due_date")
        summary = kw.get("summary")
        request_body_text_editor_box = kw.get("request_body_text_editor_box")

        formated_duedate = False
        if due_date != "":
            due_date = due_date.replace("/", "-")
            dt = datetime.strptime(due_date, "%m-%d-%Y")
            formated_duedate = dt.strftime("%Y-%m-%d")

        lead = (
            request.env["crm.lead"].sudo().search([("id", "=", int(lead_id))], limit=1)
        )
        user = (
            request.env["res.users"]
            .sudo()
            .search([("id", "=", int(assign_to))], limit=1)
        )
        activity_type_id = (
            request.env["mail.activity.type"]
            .sudo()
            .search([("id", "=", int(activity_type_id))], limit=1)
        )

        if lead:
            lead.sudo().activity_schedule(
                activity_type_id=activity_type_id.id
                or lead.sudo()._default_activity_type().id,
                note=request_body_text_editor_box,
                date_deadline=formated_duedate or fields.date.today(),
                summary=summary,
                user_id=user.id,
            )
        return request.redirect(lead.get_portal_url())

    @http.route(["/crm/log/note"], type="http", auth="user", website=True)
    def crm_log_note_opportunity(
        self, report_type=None, access_token=None, message=False, download=False, **kw
    ):

        lead_id = kw.get("lead_id")
        log_note_text_body = kw.get("log_note_text_body")
        portal_user_id = kw.get("portal_user_id")
        user_ids = set(request.httprequest.form.getlist("user_ids"))
        users_array = []
        if user_ids:
            for user in user_ids:
                users_array.append(int(user))

        lead = (
            request.env["crm.lead"].sudo().search([("id", "=", int(lead_id))], limit=1)
        )
        portal_user_id = (
            request.env["res.users"]
            .sudo()
            .search([("id", "=", int(portal_user_id))], limit=1)
        )
        users = request.env["res.users"].sudo().search([("id", "in", users_array)])
        partners = []
        if users:
            partners = users.mapped("partner_id").mapped("id")

        if lead:
            lead.sudo().message_post(
                body=Markup(log_note_text_body),
                message_type="notification",
                partner_ids=partners,
                subtype_xmlid="mail.mt_note",
                author_id=portal_user_id.id,
            )
        return request.redirect(lead.get_portal_url())
