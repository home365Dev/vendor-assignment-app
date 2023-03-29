import math

import pandas as pd
import configuration as config
from logger import logger


def _normalize_values(df_old_vendors:pd.DataFrame):
    ## avg_response_time
    df_old_vendors[config.FIXED_AVG_RESPONSE_TIME] = df_old_vendors.apply(
        lambda row: 1 - (row[config.AVG_RESPONSE_TIME] - df_old_vendors[[config.AVG_RESPONSE_TIME]].min()) /
                    (df_old_vendors[[config.AVG_RESPONSE_TIME]].max() - df_old_vendors[
                        [config.AVG_RESPONSE_TIME]].min()) if row[config.AVG_RESPONSE_TIME] > config.NO_DATA else config.NO_DATA, axis=1)
    ## avg_rating
    df_old_vendors[config.FIXED_AVG_RATING] = df_old_vendors.apply(
        lambda row: (row[config.AVG_RATING] - df_old_vendors[[config.AVG_RATING]].min()) /
                    (df_old_vendors[[config.AVG_RATING]].max() - df_old_vendors[[config.AVG_RATING]].min()) if row[config.AVG_RATING] > config.NO_DATA else config.NO_DATA, axis=1)

    ## active projects ratio
    df_old_vendors[config.FIXED_NUMBER_OF_ACTIVE] = df_old_vendors.apply(
        lambda row: 1 - (row[config.NUMBER_OF_ACTIVE] / row[config.TOTAL_NUMBER_OF_PROJECTS]) if row[config.TOTAL_NUMBER_OF_PROJECTS] > config.NO_DATA else config.NO_DATA, axis=1)

    ## rejected_projects_ratio
    df_old_vendors[config.FIXED_REJECTED] = df_old_vendors.apply(
        lambda row: 1 - row[config.NUMBER_OF_REJECTED] / row[config.TOTAL_NUMBER_OF_PROJECTS] if row[config.TOTAL_NUMBER_OF_PROJECTS] > config.NO_DATA else config.NO_DATA, axis=1)

    ## reassigned_projects_ratio
    df_old_vendors[config.FIXED_REASSIGNED] = df_old_vendors.apply(
        lambda row: 1 - row[config.NUMBER_OF_REASSIGNED] / row[config.TOTAL_NUMBER_OF_PROJECTS] if row[config.TOTAL_NUMBER_OF_PROJECTS] > config.NO_DATA else config.NO_DATA, axis=1)

    return df_old_vendors


def handler_old_vendors(df_vendors:pd.DataFrame, last_assigned_vendor_id):
    logger.info("handle old vendors")

    ## filter out the new vendors
    df_old_vendors = df_vendors.loc[df_vendors[config.TOTAL_NUMBER_OF_PROJECTS] > config.NUMBER_OF_MIN_PROJECTS_FOR_NEW_VENDOR]
    if len(df_old_vendors) == 0:
        return None, pd.DataFrame(), config.CHOSEN_VENDOR_OLD, []

    ## normalize parameters
    df_old_vendors = _normalize_values(df_old_vendors)

    df_old_vendors[config.VALUE] = df_old_vendors.apply(_calc_vendor_value, axis=1)
    df_old_vendors = df_old_vendors.sort_values(config.VALUE, ascending=False).reset_index()

    ## if the vendor is reassigned
    if last_assigned_vendor_id == config.NO_VENDOR_ID:
        logger.info("vendor chosen: " + str(df_old_vendors.loc[0]))
        chosen_vendor = df_old_vendors.loc[0]
    else:
        winning_vendor =_get_vendor_by_queue(df_old_vendors, last_assigned_vendor_id)
        logger.info("vendor chosen: " + str(winning_vendor))
        chosen_vendor = winning_vendor

    chosen_vendor = chosen_vendor.fillna('')
    return chosen_vendor, df_old_vendors, config.CHOSEN_VENDOR_OLD, list(df_old_vendors['Vendor_ID'])



def _get_vendor_by_queue(df_old_vendors, last_assigned_vendor_id):
    if len(df_old_vendors[df_old_vendors[config.VENDOR_ID] == last_assigned_vendor_id]) > 0:
        idx = df_old_vendors.index.get_loc(
            df_old_vendors[df_old_vendors[config.VENDOR_ID] == last_assigned_vendor_id].index[0])
        if idx >= 0 and idx + 1 < len(df_old_vendors):
            vib = df_old_vendors.iloc[idx + 1]
            return vib
        else:
            raise Exception("no winning vendor was found")
    else:
        vib = df_old_vendors.iloc[0]
        return vib



def _calc_vendor_value(row):
    distance = 0
    if (0 if math.isnan(row[config.FIXED_NUMBER_OF_ACTIVE] or row[config.FIXED_NUMBER_OF_ACTIVE] > config.NO_DATA) else row[config.FIXED_NUMBER_OF_ACTIVE]) > (1- config.active_threshold):
        distance = config.w_avg_rating * (0 if math.isnan(row[config.FIXED_AVG_RATING] or row[config.FIXED_AVG_RATING] > config.NO_DATA) else row[config.FIXED_AVG_RATING]) + \
                   config.w_active * (0 if math.isnan(row[config.FIXED_NUMBER_OF_ACTIVE] or row[config.FIXED_NUMBER_OF_ACTIVE] > config.NO_DATA) else row[config.FIXED_NUMBER_OF_ACTIVE]) + \
                   config.w_rejected * (0 if math.isnan(row[config.FIXED_REJECTED] or row[config.FIXED_REJECTED] > config.NO_DATA) else row[config.FIXED_REJECTED]) + \
                   config.w_avg_response_time * (0 if math.isnan(row[config.FIXED_AVG_RESPONSE_TIME] or row[config.FIXED_AVG_RESPONSE_TIME] > config.NO_DATA) else row[config.FIXED_AVG_RESPONSE_TIME])  + \
                   config.w_reassigned * (0 if math.isnan(row[config.FIXED_REASSIGNED] or row[config.FIXED_REASSIGNED] > config.NO_DATA) else row[config.FIXED_REASSIGNED])
    return distance
