class ApiTestPlanTaskState:
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISH = "FINISH"


class ApiJobState:
    WAITING = "WAITING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class CaseJobState:
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISH = "FINISH"
    FAILED = "FAILED"


class CaseTestPlanTaskState:
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISH = "FINISH"


class BranchState:
    PULLING = "PULLING"
    DONE = "DONE"
    FAILED = "FAILED"
