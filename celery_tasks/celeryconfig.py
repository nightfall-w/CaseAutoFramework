from kombu import Queue, Exchange
from automation.settings import REDIS_SERVER, TIME_ZONE

# CELERY STUFF
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
BROKER_URL = 'amqp://admin:admin@127.0.0.1:5672//'
CELERY_BROKER_URL = 'amqp://admin:admin@127.0.0.1:5672//'
CELERY_RESULT_BACKEND = 'redis://%s:6379/2' % REDIS_SERVER
CELERY_ACCEPT_CONTENT = ['application/json']
timezone = TIME_ZONE
enable_utc = False

DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
task_default_exchange = 'default'
CELERY_IMPORTS = (
    "celery_tasks.tasks"
)

# CELERY_ENABLE_UTC = False
# CELERY_TIMEZONE = TIME_ZONE
# DJANGO_CELERY_BEAT_TZ_AWARE = False
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

task_queues = (
    Queue(
        "default",
        Exchange("default"),
        routing_key="default"),
    Queue(
        "api_testplan_executor",
        Exchange("api_testplan_executor"),
        routing_key="api_testplan_executor"),
    Queue(
        "case_test_job_executor",
        Exchange("case_test_job_executor"),
        routing_key="case_test_job_executor"),
    Queue(
        "case_test_task_executor",
        Exchange("case_test_task_executor"),
        routing_key="case_test_task_executor"),
    Queue(
        "case_test_task_timing_executor",
        Exchange("case_test_task_timing_executor"),
        routing_key="case_test_task_timing_executor"),
    Queue(
        "branch_pull",
        Exchange("branch_pull"),
        routing_key="branch_pull"),
)
# Queue的路由
task_routes = {
    'api_testplan_executor': {"queue": "api_testplan_executor",
                              "routing_key": "api_testplan_executor"},
    'branch_pull': {"queue": "branch_pull",
                    "routing_key": "branch_pull"},
    'case_test_job_executor': {"queue": "case_test_job_executor",
                               "routing_key": "case_test_job_executor"},
    'case_test_task_executor': {"queue": "case_test_task_executor",
                                "routing_key": "case_test_task_executor"},
    'case_test_task_timing_executor': {"queue": "case_test_task_timing_executor",
                                "routing_key": "case_test_task_timing_executor"},
}
