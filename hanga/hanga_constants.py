__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


# AWS CLI 
DEFAULT_PROFILE = 'default' # Default profile
REGION_PROFILE = 'region' # Default region


# Stack fields and values - summary 
STACKS = 'Stacks'
STACK_SUMMARIES = 'StackSummaries'
STACK_NAME = 'StackName'
STACK_ID = 'StackId'
CHANGESET_ID = 'Id'
CREATION_TIME = 'CreationTime'
LAST_UPDATD_TIME = 'LastUpdatedTime'
DELETION_TIME = 'DeletionTime'
STACK_STATUS = 'StackStatus'
STACK_STATUS_REASON = 'StackStatusReason'
PARENT_ID = 'ParentId'
ROOT_ID = 'RootId'
DRIFT_INFORMATION ='DriftInformation'
ENABLE_TERMINATION_PROTECTION = 'EnableTerminationProtection'

# More stack fields
DESCRIPTION = 'Description'
TIMEOUT_IN_MINUTES = 'TimeoutInMinutes'
ROLE_ARN = 'RoleARN'
PARAMETERS = 'Parameters'
TAGS = 'Tags'
ENABLE_TERMINATION_PROTECTION= 'EnableTerminationProtection'
OUTPUTS = 'Outputs'
CAPABILITIES = 'Capabilities'
NOTIFICATION_ARNS = 'NotificationARNs'
DISABLE_ROLLBACK = 'DisableRollback'
ROLLBACK_CONFIGURATION = 'RollbackConfiguration'


STACK_SUMMARY_FILEDS = [STACK_NAME,
                    STACK_ID, 
                    CREATION_TIME,
                    LAST_UPDATD_TIME,
                    DELETION_TIME,
                    STACK_STATUS,
                    STACK_STATUS_REASON,
                    PARENT_ID,
                    ROOT_ID,
                    DRIFT_INFORMATION]

STACK_DETAIL_FILEDS = STACK_SUMMARY_FILEDS + [DESCRIPTION,
                                        TIMEOUT_IN_MINUTES,
                                        ROLE_ARN,
                                        PARAMETERS,
                                        TAGS,
                                        ENABLE_TERMINATION_PROTECTION,
                                        OUTPUTS,
                                        CAPABILITIES,
                                        NOTIFICATION_ARNS,
                                        DISABLE_ROLLBACK,
                                        ROLLBACK_CONFIGURATION]

# Stack status filters
CREATE_IN_PROGRESS = 'CREATE_IN_PROGRESS'
CREATE_FAILED = 'CREATE_FAILED'
CREATE_COMPLETE = 'CREATE_COMPLETE'
ROLLBACK_IN_PROGRESS = 'ROLLBACK_IN_PROGRESS'
ROLLBACK_FAILED = 'ROLLBACK_FAILED'
ROLLBACK_COMPLETE = 'ROLLBACK_COMPLETE'
DELETE_IN_PROGRESS = 'DELETE_IN_PROGRESS'
DELETE_FAILED = 'DELETE_FAILED'
DELETE_COMPLETE = 'DELETE_COMPLETE'
UPDATE_IN_PROGRESS = 'UPDATE_IN_PROGRESS'
UPDATE_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_COMPLETE = 'UPDATE_COMPLETE'
UPDATE_ROLLBACK_IN_PROGRESS = 'UPDATE_ROLLBACK_IN_PROGRESS'
UPDATE_ROLLBACK_FAILED = 'UPDATE_ROLLBACK_FAILED'
UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS = 'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'
UPDATE_ROLLBACK_COMPLETE = 'UPDATE_ROLLBACK_COMPLETE'
REVIEW_IN_PROGRESS = 'REVIEW_IN_PROGRESS'
IMPORT_IN_PROGRESS = 'IMPORT_IN_PROGRESS'
IMPORT_COMPLETE = 'IMPORT_COMPLETE'
IMPORT_ROLLBACK_IN_PROGRESS = 'IMPORT_ROLLBACK_IN_PROGRESS'
IMPORT_ROLLBACK_FAILED = 'IMPORT_ROLLBACK_FAILED'
IMPORT_ROLLBACK_COMPLETE = 'IMPORT_ROLLBACK_COMPLETE'

STACK_STATUS_FILTERS = [
    CREATE_IN_PROGRESS,
    CREATE_FAILED,
    CREATE_COMPLETE,
    ROLLBACK_IN_PROGRESS,
    ROLLBACK_FAILED,
    ROLLBACK_COMPLETE,
    DELETE_IN_PROGRESS,
    DELETE_FAILED,
    DELETE_COMPLETE,
    UPDATE_IN_PROGRESS,
    UPDATE_COMPLETE_CLEANUP_IN_PROGRESS,
    UPDATE_COMPLETE,
    UPDATE_ROLLBACK_IN_PROGRESS,
    UPDATE_ROLLBACK_FAILED,
    UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS,
    UPDATE_ROLLBACK_COMPLETE,
    REVIEW_IN_PROGRESS,
    IMPORT_IN_PROGRESS,
    IMPORT_COMPLETE,
    IMPORT_ROLLBACK_IN_PROGRESS,
    IMPORT_ROLLBACK_FAILED,
    IMPORT_ROLLBACK_COMPLETE
]

STACK_STATUS_FILTERS_NO_DELETE_COMPLETE = STACK_STATUS_FILTERS[:]
STACK_STATUS_FILTERS_NO_DELETE_COMPLETE.remove(DELETE_COMPLETE)

# Filter types
EXACTLY = 'exactly'
CONTAINS = "contains"
STARTS_WITH = "startswith"
ENDS_WITH = "endswith"

STRING_MATCH_CONDITIONS = [
                        EXACTLY,
                        CONTAINS,
                        STARTS_WITH,
                        ENDS_WITH]

# change set fields
CS_STATUS = 'Status'
CS_EXECUTION_STATUS = 'ExecutionStatus'
CS_CREATE_COMPLETE = 'CREATE_COMPLETE'
CS_FAILED = 'FAILED'

# Errror codes
ERC_PROFILE_NOTFOUND = 1
ERC_FILE_NOTFOUND = 2
ERC_JSON_INVALID = 3
ERC_S3_INVALID = 5
ERC_OTHERS = 100

# Error message
ERM_PROFILE_NOTFOUND = "Profile not found or invalid endpoint/region."
ERM_FILE_NOTFOUND = "Local file not found"
ERM_JSON_INVALID = "Invalid JSON"
ERM_S3_INVALID = "S3 not found or not accessible"
ERM_OTHERS = "Error catched!"

# Informatio messages

INF_NOTHING_TO_CHANGE = 'Nothing to change.'

# Colors
FG_WARN = 'red'
FG_ERROR = 'red'
BG_ERROR = 'black'
FG_INF = 'green'

# Others
ALL = '*'
DELIM = ','
NULL = 'NULL'
ANIM_STRING = '|/-\\'
ANIM_LEN = len(ANIM_STRING)

DELAY_TIME_FOR_DESCRIBE_CHANGE_SET = 5
DELAY_TIME_FOR_ANIMATION = 1