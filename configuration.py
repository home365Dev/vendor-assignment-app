import os

ENV_PREFIX = os.environ.get("ENV_PREFIX", "Test")
IS_TEST = (ENV_PREFIX.lower() == "test")

#### json keys
JSON_CATEGORY = 'category'
JSON_LAST_ASSIGNED = 'last_assigned_vendor_id'
JSON_POSSIBLE_VENDORS = 'possible_vendors'

#### column names

VENDOR_ID = "Vendor_ID"
VENDOR_NAME = "Vendor"
EMAIL = "Email"
CATEGORY_ID = "Category ID"
CATEGORY_NAME = "category_name"
DATE_ADDED = "date_added"
TOTAL_NUMBER_OF_PROJECTS = "num_of_projects"
AVG_RATING = "avg_rating"
FIXED_AVG_RATING = "fixed_avg_rating"
AVG_RESPONSE_TIME = "avg_response_time"
FIXED_AVG_RESPONSE_TIME = "fixed_avg_response_time"
NUMBER_OF_REJECTED = "number_of_rejected"
FIXED_REJECTED = "fixed_rejected"
NUMBER_OF_ACTIVE = "number_of_active"
FIXED_NUMBER_OF_ACTIVE = "fixed_number_of_active"
NUMBER_OF_REASSIGNED = "number_of_reassigned"
FIXED_REASSIGNED = "fixed_reassigned"
VALUE = "value"

NO_VENDOR_ID = "-1"
NO_DATA = -1
NUMBER_OF_MIN_PROJECTS_FOR_NEW_VENDOR = 5

## weights
w_avg_response_time = 10
w_avg_rating = 5
w_rejected = 4
w_reassigned = 4
w_active = 3
active_threshold = 0.7

## chosen_vendor_state
CHOSEN_VENDOR_NEW = "New"
CHOSEN_VENDOR_OLD = "Old"
