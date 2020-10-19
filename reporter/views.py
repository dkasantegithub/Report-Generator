from django.shortcuts import render
from sqlalchemy import create_engine, MetaData, Table, select
from django.http import HttpResponse, Http404

# db connection
db = 'hellio'
dbhostname = '116.202.157.137'
dbport = '3327'
dbusername = 'dasante'
dbpassword = 'KOIi0p@@123enbgst2618sja'

# db engine
engine = create_engine('mysql+pymysql://'+str(dbusername)+':'+str(dbpassword)+'@'+str(dbhostname)+':'+str(dbport)+'/'+str(db))
connection = engine.connect()



def index(request):

    # try: 
    #     stmt_username = "SELECT username from users"    
    #     results_username = connection.execute(stmt_username).fetchall()
    # except ObjectDoesNotExist:
    #     return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

    # if request.method == 'POST':
    #     user = str("'") + str(request.POST['username']) + str("'")
    #     startdate =str("'") + str(request.POST['start_date']) + str("'")
    #     enddate = str("'") + str(request.POST['end_date']) + str("'")

    #     #query to get data from db
    #     if user != 'None' and startdate != 'None' and enddate != 'None':
    #         try:
    #             stmt = "SELECT user_jobs.id, user_jobs.name, user_jobs.sender, user_jobs.message, user_jobs.sms_count, task_started_date, user_jobs.total_traffic, sum(case when logs.status='DELIVRD' then 1 else 0 end) AS DELIVERED, sum(case when logs.status='UNDELIV' then 1 else 0 end) AS UNDELIVERED, sum(case when logs.status='ACK/' then 1 else 0 end) AS ACK, sum(case when logs.status='FAILED' then 1 else 0 end) AS FAILED, sum(case when logs.status='EXPIRED' then 1 else 0 end) AS EXPIRED, sum(case when logs.status='PENDING' then 1 else 0 end) AS PENDING, sum(case when logs.status='REJECTED' then 1 else 0 end) AS REJECTED from logs INNER JOIN user_jobs ON logs.job_id=user_jobs.id where logs.username like {} and logs.submit_date BETWEEN {} AND {} AND logs.job_id IN (SELECT id FROM user_jobs where  username like {} and task_started_date between {} AND {} and status = 'done') GROUP BY logs.job_id".format(user, startdate, enddate, user, startdate, enddate)
    #             #Results proxy and results 
    #             results = connection.execute(stmt).fetchall()
    #         except ObjectDoesNotExist:
    #             return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

    #         return render(request, 'reporter/index.html', {'results_username':results_username, 'results':results, } )


    return render(request, 'reporter/index.html', {} )




def api_report(request):
    try:
        query_username = "SELECT username from users"
        username = connection.execute(query_username).fetchall()

    except ObjectDoesNotExist:
        return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

    if request.method == 'POST':
        user = str("'") + str(request.POST['username']) + str("'")
        startdate =str("'") + str(request.POST['start_date']) + str("'")
        enddate =str("'") + str(request.POST['end_date']) + str("'")


        if user != "None" and startdate != "None" and enddate != "None":
            try:
                query_api = "SELECT id, sender, message, sms_count, submit_date, status from logs where username={} and submit_date between {}  and {} and originated='apiuser'".format(user, startdate, enddate)
                query_results = connection.execute(query_api).fetchall()
            except ObjectDoesNotExist:
                return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

            return render(request, 'reporter/api_report.html', {'username': username, 'query_results': query_results,})

    return render(request, 'reporter/api_report.html', {'username': username, 'query_results': '', })



def bulk_report(request):
    
    try: 
        stmt_username = "SELECT username from users"    
        results_username = connection.execute(stmt_username).fetchall()
    except ObjectDoesNotExist:
        return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

    if request.method == 'POST':
        user = str("'") + str(request.POST['username']) + str("'")
        startdate =str("'") + str(request.POST['start_date']) + str("'")
        enddate = str("'") + str(request.POST['end_date']) + str("'")

        #query to get data from db
        if user != 'None' and startdate != 'None' and enddate != 'None':
            try:
                stmt = "SELECT user_jobs.id, user_jobs.name, user_jobs.sender, user_jobs.message, user_jobs.sms_count, task_started_date, user_jobs.total_traffic, sum(case when logs.status='DELIVRD' then 1 else 0 end) AS DELIVERED, sum(case when logs.status='UNDELIV' then 1 else 0 end) AS UNDELIVERED, sum(case when logs.status='ACK/' then 1 else 0 end) AS ACK, sum(case when logs.status='FAILED' then 1 else 0 end) AS FAILED, sum(case when logs.status='EXPIRED' then 1 else 0 end) AS EXPIRED, sum(case when logs.status='PENDING' then 1 else 0 end) AS PENDING, sum(case when logs.status='REJECTED' then 1 else 0 end) AS REJECTED from logs INNER JOIN user_jobs ON logs.job_id=user_jobs.id where logs.username like {} and logs.submit_date BETWEEN {} AND {} AND logs.job_id IN (SELECT id FROM user_jobs where  username like {} and task_started_date between {} AND {} and status = 'done') GROUP BY logs.job_id".format(user, startdate, enddate, user, startdate, enddate)
                #Results proxy and results 
                results = connection.execute(stmt).fetchall()
            except ObjectDoesNotExist:
                return HttpResponse('UNABLE TO CONNECT TO DB, DB CONNECTION ERROR')

            return render(request, 'reporter/bulk_report.html', {'results_username':results_username, 'results':results, } )


    return render(request, 'reporter/bulk_report.html', {'results_username':results_username, 'results':'', } )



def kannel_report(request):

    return render(request, 'reporter/kannel_report.html', {})
    