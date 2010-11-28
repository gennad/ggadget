'''
Created on 28.11.2010

@author: gennad
'''
try:
  from xml.etree import ElementTree # for Python 2.5 users
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

def GetAuthSubUrl():
    next = 'http://www.coolcalendarsite.com/welcome.pyc'
    scope = 'https://www.google.com/calendar/feeds/'
    secure = False
    session = True
    calendar_service = gdata.calendar.service.CalendarService()
    return calendar_service.GenerateAuthSubURL(next, scope, secure, session);
"""
authSubUrl = GetAuthSubUrl();
print '<a href="%s">Login to your Google account</a>' % authSubUrl
"""

def getSessionToken(authsub_token):
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.auth_token = authsub_token
    calendar_service.UpgradeToSessionToken()
    feed = calendar_service.GetCalendarListFeed()
    for i, a_calendar in enumerate(feed.entry):
        print '\t%s. %s' % (i, a_calendar.title.text,)
        
def PrintUserCalendars(calendar_service):
    feed = calendar_service.GetAllCalendarsFeed()
    print feed.title.text
    for i, a_calendar in enumerate(feed.entry):
        print '\t%s. %s' % (i, a_calendar.title.text,)
    
def PrintOwnCalendars(calendar_service):
    feed = calendar_service.GetOwnCalendarsFeed()
    print feed.title.text
    for i, a_calendar in enumerate(feed.entry):
        print '\t%s. %s' % (i, a_calendar.title.text,)
    
def PrintAllEventsOnDefaultCalendar(calendar_service):
    feed = calendar_service.GetCalendarEventFeed()
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)
        for p, a_participant in enumerate(an_event.who):
            print '\t\t%s. %s' % (p, a_participant.email,)
            print '\t\t\t%s' % (a_participant.name,)
            print '\t\t\t%s' % (a_participant.attendee_status.value,)
      
def DateRangeQuery(calendar_service, start_date='2007-01-01', end_date='2007-07-01'):
    print 'Date range query for events on Primary Calendar: %s to %s' % (start_date, end_date,)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full')
    query.start_min = start_date
    query.start_max = end_date 
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)
        for a_when in an_event.when:
            print '\t\tStart time: %s' % (a_when.start_time,)
            print '\t\tEnd time:   %s' % (a_when.end_time,)
      
def FullTextQuery(calendar_service, text_query='Tennis'):
    print 'Full text query for events on Primary Calendar: \'%s\'' % ( text_query,)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', text_query)
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)
        print '\t\t%s. %s' % (i, an_event.content.text,)
        for a_when in an_event.when:
            print '\t\tStart time: %s' % (a_when.start_time,)
            print '\t\tEnd time:   %s' % (a_when.end_time,)
      
def InsertSingleEvent(calendar_service, title='One-time Tennis with Beth', 
                      content='Meet for a quick lesson', where='On the courts', 
                      start_time=None, end_time=None):
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gdata.calendar.Where(value_string=where))

    if start_time is None:
        # Use current time for the start_time and have the event last 1 hour
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
    event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')
    
    print 'New single event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
    
    return new_event

def InsertRecurringEvent(calender_service, title='Weekly Tennis with Beth',
                         content='Meet for a quick lesson', where='On the courts',
                         recurrence_data=None):
    if recurrence_data is None:
      recurrence_data = ('DTSTART;VALUE=DATE:20070501\r\n'
        + 'DTEND;VALUE=DATE:20070502\r\n'
        + 'RRULE:FREQ=WEEKLY;BYDAY=Tu;UNTIL=20070904\r\n')

    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gdata.calendar.Where(value_string=where))

    # Set a recurring event
    event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')
    
    print 'New recurring event inserted: %s' % (new_event.id.text,)
    print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
    return new_event

def UpdateTitle(calendar_service, event, new_title='Updated event title'):
    previous_title = event.title.text
    event.title.text = new_title
    print 'Updating title of event from:\'%s\' to:\'%s\'' % (previous_title, event.title.text,) 
    return calendar_service.UpdateEvent(event.GetEditLink().href, event)

"""
def batchRequest():  
    # feed that holds all the batch rquest entries
    request_feed = gdata.calendar.CalendarEventFeed()
    # creating an event entry to insert
    insertEntry = gdata.calendar.CalendarEventEntry()
    insertEntry.title = atom.Title(text='Python: batch insert')
    insertEntry.content = atom.Content(text='my content')
    start_time = '2008-06-01T09:00:00.000-07:00'
    end_time = '2008-06-01T10:00:00.000-07:00'
    insertEntry.when.append(gdata.calendar.When(start_time=start_time,
                                                end_time=end_time))
    insertEntry.batch_id = gdata.BatchId(text='insert-request')

    # add the insert entry to the batch feed
    request_feed.AddInsert(entry=insertEntry)

    updateEntry = getOneEvent('Python')
    if updateEntry:
        updateEntry.batch_id = gdata.BatchId(text='update-request')
        updateEntry.title = atom.Title(text='Python: batch update')
        # add the update entry to the batch feed
        request_feed.AddUpdate(entry=updateEntry)
  
    queryEntry = getOneEvent('Python')
    if queryEntry:
        queryEntry.batch_id = gdata.BatchId(text='query-request')
        # add the query entry to the batch feed
        request_feed.AddQuery(entry=queryEntry)
  
    deleteEntry = getOneEvent('Python')
    if deleteEntry:
        deleteEntry.batch_id = gdata.BatchId(text='delete-request')
        # add the delete entry to the batch feed
        request_feed.AddDelete(entry=deleteEntry)

    # submit the batch request to the server
    response_feed = calendar_service.ExecuteBatch(request_feed, 
        gdata.calendar.service.DEFAULT_BATCH_URL)

    # iterate the response feed to get the operation status
    for entry in response_feed.entry:
        print 'batch id: %s' % (entry.batch_id.text,)
        print 'status: %s' % (entry.batch_status.code,)
        print 'reason: %s' % (entry.batch_status.reason,)

def getOneEvent(text):
    username = 'default'
    visibility = 'private'
    projection = 'full'
    query = gdata.calendar.service.CalendarEventQuery(username, visibility, projection)
    query['q'] = text
    query['max-results'] = '1'

    feed = calendar_service.CalendarQuery(query)

    if len(feed.entry) > 0:
        return feed.entry[0]
    else:
        return None
"""











