import pandas as pd
import configuration as config
from logger import logger

def handle_new_vendors(df_vendors:pd.DataFrame, last_assigned_vendor_id):
    logger.log("find new vendor")

    new_vendors_df = df_vendors.loc[df_vendors[config.TOTAL_NUMBER_OF_PROJECTS] <= config.NUMBER_OF_MIN_PROJECTS_FOR_NEW_VENDOR]
    if len(new_vendors_df) == 0:
        return None, pd.DataFrame(), config.CHOSEN_VENDOR_NEW, []

    new_vendors_df_sorted = new_vendors_df.sort_values([config.DATE_ADDED, config.TOTAL_NUMBER_OF_PROJECTS], ascending=[True, True]).reset_index()

    list_vendor_df_sorted = list(new_vendors_df_sorted['Vendor_ID'])
    ## run over the first vendors which are considered as new and check for the first one which hasn't been assigned yet
    ## take the vendor which has been added at the oldest date
    if last_assigned_vendor_id == config.NO_VENDOR_ID:
        return new_vendors_df_sorted.loc[0], new_vendors_df_sorted, config.CHOSEN_VENDOR_NEW, list_vendor_df_sorted

    ## find a raw right after the last_assigned_vendor_id ?
    vendor_df_last_assigned = new_vendors_df_sorted[new_vendors_df_sorted[config.VENDOR_ID] == last_assigned_vendor_id]
    idx = 0
    if len(vendor_df_last_assigned) > 0:
        idx = new_vendors_df_sorted.index.get_loc(vendor_df_last_assigned.index[0])
    if idx >= 0 and idx + 1 < len(new_vendors_df_sorted):
        vib = new_vendors_df_sorted.iloc[idx+1]
        if vib[config.TOTAL_NUMBER_OF_PROJECTS] == 0:
            return vib, new_vendors_df_sorted, config.CHOSEN_VENDOR_NEW, list_vendor_df_sorted
        else:
            return None, new_vendors_df_sorted, config.CHOSEN_VENDOR_NEW, list_vendor_df_sorted
    elif idx + 1 >= len(new_vendors_df_sorted):
        raise Exception("last_assigned_vendor_id " + str(last_assigned_vendor_id) + " is the last vendor in our list")

    raise Exception("last_assigned_vendor_id " + str(last_assigned_vendor_id) + " was not found")
