from dateutil import rrule
from openerp import models, fields, api, _
import datetime
from openerp import http
from openerp.http import request
import logging
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta, date

_logger = logging.getLogger(__name__)




def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
class product_free_spot(models.TransientModel):
    _name = 'product.free_spot'
    #_inherit = 'calendar.event'
    _inherit = ["mail.thread", "ir.needaction_mixin"]
    
    @api.one
    def _compute(self, ):
        #attendee = self._find_my_attendee([self.id])
        #self.is_attendee = bool(attendee)
        #self.attendee_status = attendee.state if attendee else 'needsAction'
        #self.display_time = self._get_display_time(cr, uid, meeting.start, meeting.stop, meeting.duration, meeting.allday, context=context)
        self.display_start = self.start_date if self.allday else self.start_datetime
        self.start = self.start_date if self.allday else self.start_datetime
        self.stop = self.stop_date if self.allday else self.stop_datetime

    
    
    state = fields.Selection([('draft', 'Unconfirmed'), ('open', 'Confirmed')], string='Status', readonly=True, track_visibility='onchange')
    name = fields.Char('Meeting Subject', required=True, states={'done': [('readonly', True)]})
    is_attendee = fields.Boolean(compute=_compute, string='Attendee',)
    #attendee_status = fields': fields.function(_compute, string='Attendee Status', type="selection", selection=calendar_attendee.STATE_SELECTION, multi='attendee'),
    allday = fields.Boolean('All Day', states={'done': [('readonly', True)]})
    start_datetime = fields.Datetime('Start DateTime', states={'done': [('readonly', True)]}, track_visibility='onchange')
    stop_datetime =  fields.Datetime('End Datetime', states={'done': [('readonly', True)]}, track_visibility='onchange')
    duration =  fields.Float('Duration', states={'done': [('readonly', True)]})
    description = fields.Text('Description', states={'done': [('readonly', True)]})

    user_id = fields.Many2one('res.users', 'Responsible', states={'done': [('readonly', True)]})
    color_partner_id = fields.Integer(related='user_id.partner_id.color',  string="colorize", )  # Color of creator
    active = fields.Boolean(string='Active', help="If the active field is set to true, it will allow you to hide the event alarm information without removing it.")
    categ_ids = fields.Many2many('calendar.event.type', 'meeting_category_rel', 'event_id', 'type_id', 'Tags')
    partner_ids = fields.Many2many('res.partner')
    product_id = fields.Many2one('product.template','Product')
    employee_id = fields.Many2one('hr.employee','Employee')
    
    #attendee_ids': fields.one2many('calendar.attendee', 'event_id', 'Attendees', ondelete='cascade')
    #'partner_ids': fields.many2many('res.partner', 'calendar_event_res_partner_rel', string='Attendees', states={'done': [('readonly', True)]}),
    #'alarm_ids': fields.many2many('calendar.alarm', 'calendar_alarm_calendar_event_rel', string='Reminders', ondelete="restrict", copy=False),




#    partner_ids = fields.Many2many('res.partner', 'product_booking_res_partner_rel', string='Attendees', states={'done': [('readonly', True)]})
 #   alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_product_booking_rel', string='Reminders', ondelete="restrict", copy=False)
 #   attendee_ids = fields.One2many('product.attendee', 'event_id', string='Attendees', ondelete='cascade')
        
        #def search_read(self, cr, uid, domain=None, fields=None, offset=0, limit=None, order=None, context=None):

    #~ def __init__(self,pool,cr):
        #~ raise Warning('Hello World')

    def get_free_spots(self, start_dt, product_id=False, calendar=False,employee_id=False):
        _logger.warning('<<<<<<<<<<<freeeeeee>>>>>>>>>>>: %s' % start_dt.replace(hour=8, minute=8, second=8))
        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
        if produkt_id:
            product = self.env['product.template'].browse(product_id)

        self.select([('date_start','>=',start_dt),('date_start','<',start_dt.timedelta(days=1))]).unlink()
        for contract in employee_id.contract_ids:
            for interval in contract.working_hours.get_working_intervals_of_day(self._cr, self._uid, contract.working_hours.id, start_dt):
                i = interval[0]
                while(i.timedelta(minutes=product.duration) <= interval[1]):
                    # check if spot or booking exists 
                    spot.create({'url': 'hejsan', 'name': 'name','date_start': i, 'date_end': i.timedelta(minutes=product.duration)})
                    i += i.timedelta(minutes=product.duration)
        raise Exception("The record has been deleted or not")
        return [spot.select([('date_start','>=',start_dt),('date_start','<',start_dt.timedelta(days=1))])]

    def search_range(self,start_dt,stop_dt,product):
        return self.search([('date_start','>=',start_dt),('date_start','<',stop_dt),('product_id','=',product.id)])


    def unlink_range(self,start_dt,stop_dt,product):
        self.search_range(start_dt,stop_dt,product).unlink


    @api.v7
    def search(self,cr,uid,domain=None,offset=0,limit=None,order=None,context=None,count=False,extra=None):
        _logger.error('Hello %s %s %s %s' % (domain,offset,limit,order))
        # ['|', '|', '&', ['start', '>=', '2015-09-28'], ['start', '<=', '2015-11-02'], '&', ['start', '<=', '2015-09-28'], ['stop', '>=', '2015-09-28'], '&', ['start', '<=', '2015-11-02'], ['stop', '>=', '2015-09-28']] 0 False False
        if len(domain)>4:
            (_,_,start) = domain[3]
            (_,_,stop)  = domain[4]
            start_date = datetime.datetime.strptime(start, DEFAULT_SERVER_DATE_FORMAT)
            if start_date < datetime.datetime.today():
                start_date = datetime.datetime.today()
            stop_date = datetime.datetime.strptime(stop, DEFAULT_SERVER_DATE_FORMAT)
            product_id = self.pool['product.product'].search(cr,uid,[],limit=1,context=context)[0]
            product = self.pool['product.product'].browse(cr,uid,product_id)
            _logger.error('day %s %s %s ' % (daterange(start_date,stop_date),start_date,stop_date))
            for day in range((stop_date - start_date).days):
                pass
                #~ self.pool['product.booking'].create(cr,uid,{'name': 'booking', 'product_id': 1, 'user_id': 1, 
                #~ 'start_date': start_date + timedelta(days=day),'stop_date': start_date + timedelta(days=day),'active': True,
                #~ 'allday': True},context)
                #_logger.error('day %r %s ' % (product.product_tmpl_id,product.product_tmpl_id.get_free_spots(start_date + timedelta(days=day))))            
        return super(product_free_spot,self).search(cr,uid,domain,offset,limit,order,context,count)
        

        
class product_attendee(models.TransientModel):
    _name = "product.attendee"
    _inherit = 'calendar.attendee'

    @api.v7
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if not vals.get("email") and vals.get("cn"):
            cnval = vals.get("cn").split(':')
            email = filter(lambda x: x.__contains__('@'), cnval)
            vals['email'] = email and email[0] or ''
            vals['cn'] = vals.get("cn")
        res = super(product_attendee, self).create(cr, uid, vals, context=context)
        return res




class DateTime(datetime.datetime):
    def __init__(self):
        self.thisDate = self.today()
        self.day = datetime.timedelta(days=1)

    def get_year(self):
        return self.isocalendar()[0]

    def get_week(self):
        return self.isocalendar()[1]

    def get_weekday(self):
        return self.isocalendar()[2]

    def next_day(self, days=0):
        return self.thisDate + datetime.timedelta(days=days)


class product_template(models.Model):
    _inherit = 'product.template'

    duration = fields.Integer(string='Duration', help='This is duration time in minutes', default=60)
    @api.one
    def _booking_count(self):
        self.booking_count = len(self.booking_ids)
    booking_count = fields.Integer(compute=_booking_count)
    booking_ids = fields.Many2many('calendar.event')
    book_ok = fields.Boolean('Can be booked')
    
    
    @api.multi
    def action_view_booking(self):
        product_ids = []
        for template in self:
            product_ids += [x.id for x in template.product_variant_ids]
        result = self.env['ir.model.data'].xmlid_to_res_id('product_booking.action_view_calendar_event_calendar',raise_if_not_found=True)
        result = self.env['ir.actions.act_window'].read([result])[0]
        result['domain'] = "[('product_id','in',[" + ','.join(map(str, product_ids)) + "])]"
        
        
        return result

    def get_free_spots(self, start_dt, stop_dt):
        """
            Get free spots for all employees at this date-interval
        """
        for day in range((stop_dt - start_dt).days):
            self.create_free_spot(start_date + timedelta(days=day))
        return self.env['product.free_spot'].search_range(start_dt,stop_dt,self)

    def create_free_spot(self, date, employee=None):
        if employee:
            employees = [employee]
        else:
            employees = self.env['hr.employee'].search([])
        for contract in [e.contract_ids for e in employees]:
            for interval in contract.working_hours.get_working_intervals_of_day(self._cr, self._uid, contract.working_hours.id, date):
                i = interval[0]
                while(i.timedelta(minutes=self.duration) <= interval[1]):
                    # check if spot or booking exists 
                    self.env['product.free_spot'].create({'url': 'hejsan', 'name': 'name','start_datetime': i, 'stop_datetime': i.timedelta(minutes=self.duration)})
                    i += i.timedelta(minutes=self.duration)


class calendar_event(models.Model):
    _inherit = "calendar.event"
    
    product_id = fields.Many2one('product.template','Product')
    

#~ class product_spot_time(models.TransientModel):
    #~ _name = "product.spot_time"
    #~ 
    #~ url = fields.Char(string="Url")
    #~ name = fields.Char(string="Name")
    #~ date_start = fields.DateTime(string='Start')
    #~ date_end   = fields.DateTime(string='End')
    #~ 
    #~ 
class hr_employee(models.Model):
    _inherit = "hr.employee"

    def get_free_spots(self, start_dt, product):
        _logger.warning('<<<<<<<<<<<freeeeeee>>>>>>>>>>>: %s' % start_dt.replace(hour=8, minute=8, second=8))
# return if there are spots created
        self.env['product.free_spot'].unlink_range(start_dt,start_dt.timedelta(days=1),product)
        for contract in employee_id.contract_ids:
            for interval in contract.working_hours.get_working_intervals_of_day(self._cr, self._uid, contract.working_hours.id, start_dt):
                i = interval[0]
                while(i.timedelta(minutes=product.duration) <= interval[1]):
                    # check if spot or booking exists check allday
                    self.env['product.free_spot'].create({'url': 'hejsan', 'name': 'name','start_datetime': i, 'stop_datetime': i.timedelta(minutes=product.duration)})
                    i += i.timedelta(minutes=product.duration)
        return self.env['product.free_spot'].select_range(start_dt,start_dt.timedelta(days=1))


