from dateutil import rrule
from openerp import models, fields, api, _
import datetime
from openerp import http
from openerp.http import request
import logging

_logger = logging.getLogger(__name__)


class Booking(models.Model):
    _name = 'booking.booking'

    # bookings = fields.One2many(compute='booking')

    @api.model
    def now_week(self):
        year = datetime.datetime.today().strftime("%Y")
        week = datetime.datetime.today().strftime("%V")
        _logger.warning('%s %s' % (year, week))
        return self.week_days(year, week)

    @api.model
    def week_days(self, year, week):
        if datetime.date(int(year), 1, 1).isocalendar()[2] <= 4:
            week = str(int(week) - 1)
        year_week = year + '-W' + week
        one_day = datetime.datetime.strptime(year_week + '-1', "%Y-W%W-%w")
        weekday_dates = [day.replace(hour=0, minute=0, second=0) for day in rrule.rrule(rrule.DAILY, dtstart=one_day, until=(one_day + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0))]
        # weekday_dates.append(DateTime.strptime(year_week + '-1', "%Y-W%W-%w"))
        # for i in range(0, 7):
        #     weekday_dates.append(datetime.timedelta.__init__(DateTime, days=1))

        _logger.warning('<<<<<<<<<<<weekday>>>>>>>>>>>: %s' % weekday_dates[0].replace(hour=9, minute=9, second=9))
        return weekday_dates

    def booking(self, calendar_time, planned_time, booked_time):
        available_time = []
        return available_time


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


class product_product(models.Model):
    _inherit = 'product.product'

    duration = fields.Integer(string='Duration', help='This is duration time in minutes', default=60)

    def get_free_spots(self, start_dt, product=False, calendar=False):
        _logger.warning('<<<<<<<<<<<freeeeeee>>>>>>>>>>>: %s' % start_dt.replace(hour=8, minute=8, second=8))
        employee_id = self.env['hr.employee'].search([('name', '=', 'Gilles Gravie')])[0]

        for contact in employee_id.contract_ids:
            for interval in contact.working_hours.get_working_intervals_of_day(self._cr, self._uid, contact.working_hours.id, start_dt):
                spot = (interval[0], interval[0].timedelta(minutes=self.duration))

        return [spot]

    # def get_free_spots(self, product=False, calendar=False):
    #     return [('url', 'string'), ('url', 'string')]


class BookingController(http.Controller):
    @http.route(['/booking/<string:year>/<string:week>', ], type='http', auth="public", website=True)
    def search_week(self, year, week):
        return self.week_days(year, week)

    @http.route(['/booking/now', ], type='http', auth="public", website=True)
    def now_week_http(self):
        _logger.warning('<<<<<<<<<<<<<<<<< this is my calendar >>>>>>>>>>>>>>>>>: %s' % request.env['booking.booking'].now_week())
        return request.render('website_sale_booking.website_calendar', {'now_week': request.env['booking.booking'].now_week(),
                                                                        'product': request.env['product.product'].search([])[0]})

    def week_days(self, year, week):
        pass
