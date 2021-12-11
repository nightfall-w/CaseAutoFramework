from kombu import Queue, Exchange

from automation.settings import REDIS_SERVER, RABBITMQ, TIME_ZONE

# CELERY STUFF
broker_url = 'amqp://admin:admin@%s:5672//' % RABBITMQ
result_backend = 'redis://%s:6379/2' % REDIS_SERVER
accept_content = ['application/json']
timezone = TIME_ZONE
# enable_utc = False
task_serializer = 'json'
result_serializer = 'json'
task_default_exchange = 'default'
imports = (
    "celery_tasks.tasks"
)

enable_utc = False

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
