def get_total_leads_new(self):
        # 🔹 Step 1: Pehle user_id ke basis par grouping
        user_data = request.env['crm.lead'].read_group(
            domain=[('type', '=', 'lead')],
            fields=['user_id'],
            groupby=['user_id']
        )

        result = []
        total_live_duplicates_count = 0

        for user in user_data:
            user_id = user.get('user_id') and user['user_id'][0] or False
            user_name = user.get('user_id') and user['user_id'][1] or 'Undefined'

            # 🔹 Step 2: Ab har user ke andar stage-wise grouping karni hai
            stage_data = request.env['crm.lead'].read_group(
                domain=[('type', '=', 'lead'), ('user_id', '=', user_id)],
                fields=['lead_stage_id'],
                groupby=['lead_stage_id']
            )

            user_lead_data = []
            for stage in stage_data:
                stage_id = stage.get('lead_stage_id') and stage['lead_stage_id'][0] or False
                stage_name = stage.get('lead_stage_id') and stage['lead_stage_id'][1] or 'Undefined'

                lead_domain = [('type', '=', 'lead'), ('user_id', '=', user_id)]
                if stage_id:
                    lead_domain.append(('lead_stage_id', '=', stage_id))
                
                total_lead_count = request.env['crm.lead'].search_count(lead_domain)
                lead = request.env['crm.lead'].search(lead_domain, limit=None)

                live_leads = lead.filtered(lambda lead: lead.live_transfer)
                portal_leads = lead.filtered(lambda lead: not lead.live_transfer)

                duplicate_stage_ids = request.env['crm.lead.stage'].search([('is_duplicate_stage', '=', True)]).ids
                live_duplicates = live_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)
                portal_duplicates = portal_leads.filtered(lambda lead: lead.lead_stage_id.id in duplicate_stage_ids)

                live_duplicates_count = len(live_duplicates)
                portal_duplicates_count = len(portal_duplicates)

                total_live_duplicates_count += live_duplicates_count

                user_lead_data.append({
                    'lead_stage_id': stage_id or 'No Stage',
                    'lead_stage_name': stage_name,
                    'total_lead_count': total_lead_count,
                    'live_duplicates_count': live_duplicates_count,
                    'portal_duplicates_count': portal_duplicates_count,
                    'data': lead.ids,
                })

            result.append({
                'user_id': user_id or 'No User Assigned',
                'user_name': user_name,
                'stages': user_lead_data
            })

        return result
