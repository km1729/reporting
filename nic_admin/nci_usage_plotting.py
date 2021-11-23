import numpy as np
import re
import sys
import glob
import datetime as dt
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pytz
from dateutil.relativedelta import relativedelta
import configparser
import argparse

# Logs directory
logDir = ""
#lquotaDir = "/g/data/dp9/slc548/nci_usage/reports/"
logDateFormat = "%Y%m%d"
dateTimeFormat = "%Y%m%d %H%MZ"
#plotDir = "/g/data/dp9/slc548/nci_usage/"

# Project
#proj = "dp9"

# Log file format templates
#suFileTemplate = proj + "_{dateStr}.rpt"
#lquotaFileTemplate = "lquota_{dateStr}.rpt"


# Reference date UTC for extrapolation calulation (arbitrary)
refdate = dt.datetime(1970,1,1,1,0)


def currentQuarter(date):
    # Determine current quarter then the start/end dates of quater.
    quarter = round( (date.month - 1) // 3 + 1)
    start = dt.datetime(date.year, 3 * quarter -2, 1)
    end_month = (3 * quarter +1)
    if end_month < 12:
        end = dt.datetime(date.year, end_month, 1) + dt.timedelta(days=-1)
    else:
        end = dt.datetime(date.year + 1, end_month % 12, 1) + dt.timedelta(days=-1)

    return start, end


def extractSUValue(fin, pattern):
    # Open file and get the value for the given pattern
    pattern = pattern.split()[0] + ":"
    with open(fin, 'r') as f:
        match = []
        for line in f:
            if pattern in line:
                match.append(line)

    # If there was an error generating the report, there will be no matches
    if len(match) == 0:
        value = np.NaN
    else:
        string=match[0].split(pattern)[1].strip()
        units=string.split()[1]
        value=float(string.split()[0])

        # Convert units if need be
        if units == "KSU":
            value /= 1000.0
        if units == "SU":
            value /= 1000000.0
    return value


def extractDataValue(fin, pattern, proj = 'dp9'):
    # Open file and get the value for the given pattern
    with open(fin, 'r') as f:
        match = []
        for line in f:
            if (pattern in line) and (proj in line.split()):
                match.append(line)

    usage=match[0].split(pattern)[1].split()[0]
    quota=match[0].split(pattern)[1].split()[1]

    usageUnits=usage[-2:]
    usageValue=float(usage[:len(usage)-2])

    quotaValue=float(quota[:len(quota)-2])

    if pattern == "scratch":
    # Convert units to PB
        if usageUnits == "TB":
            usageValue /= 1000.0
        if usageUnits == "GB":
            usageValue /= 1000000.0
        if usageUnits == "MB":
            usageValue /= 1000000000.0
    if pattern == "gdata":
    # Convert units to TB
        if usageUnits == "GB":
            usageValue /= 1000.0
        if usageUnits == "MB":
            usageValue /= 1000000.0

    return usageValue, quotaValue


def extrapolateUsage(SUdf, endDate, extrapDayWindow='all'):
    # Extrapolate the current usage to the end of the quarter
    # https://stackoverflow.com/questions/34159342/extrapolate-pandas-dataframe
    # Extropolate values: https://stackoverflow.com/questions/22491628/extrapolate-values-in-pandas-dataframe/35959909#35959909

    guess = (1, 0)
    df = SUdf.copy()

    di = df.index
    df1 = df.reset_index().drop('index',1)
    df1.index = pd.Series(df.index - refdate)

    # How much data to use in extrap?
    if (extrapDayWindow == 'all'):
        #use all entries in extrapolation
        fit_df = df1.dropna()
    else:
        # only use those within the window
        fit_df = df1.dropna()
        fit_df = fit_df[-(extrapDayWindow+1):-1]

    # Pace to store function parameters in each column
    col_params = {}

    for col in fit_df.columns:
        # Get x & y
        x = fit_df.index.total_seconds().astype(float)
        y = fit_df[col].astype(float).values

        params = curve_fit(lin_func, x, y, guess)
        # Store optimized parameters
        col_params[col] = params[0]

        # For the Grant extrapolation, just extrapolate latest Grant quota value (this can change throughout a quarter).
        if 'grant' in col.lower():
            col_params[col][0] = 0
            col_params[col][1] = y[-1]

    # Extrapolate each column
    x = (endDate - refdate)
    add_dict = {}
    for col in df.columns:
        add_dict[col] = lin_func(x.total_seconds(), *col_params[col])
    df2 = pd.DataFrame(data = add_dict, index = [pd.to_datetime(x + refdate)], columns = df.columns)

    return df.append(df2), col_params


def fillSUdf(fin, date, df):
    # Extract the Grant, Used and Avail values.
    for pattern in list(df.columns):
        value = extractSUValue(fin, pattern)
        df.loc[[date.date()], [pattern]] = value


def fillDatadf(fin, date, df, name):
    # Extract the Grant, Used and Avail values.
    usage, quota = extractDataValue(fin, name)
    df.loc[[date.date()], ["Usage"]] = usage
    df.loc[[date.date()], ["Quota"]] = quota


def filePath(template, date, rootDir=logDir):
    # Create the log filename path
    dateStr = date.strftime(logDateFormat)
    path = os.path.join(rootDir, template.format(dateStr=dateStr))

    return path


def lin_func(x, a, b):
    return a * x + b


def parse_args():
    """
    Parse user inputs
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--config",
                        nargs='?',
                        required=True,
                        type=str,
                        help="Configuation file.")

    return parser.parse_args()


def parse_config(conf):
    """
    Parse the config file.
    """

    config = configparser.ConfigParser()
    config.read(conf)

    proj = parseConfigSectionMap(config, "project")["proj"]

    IODict = parseConfigSectionMap(config, "IO")

    logDir = IODict["logdir"]
    lquotaDir = IODict["lquotadir"]
    plotDir = IODict["plotdir"]

    return proj, logDir, lquotaDir, plotDir


def parseConfigSectionMap(config, section):
    """
    Get options for the given section.
    """

    sec_dict = {}
    options = config.options(section)

    for option in options:
        try:
            sec_dict[option] = config.get(section, option)
        except:
            print("Exception on %s" % option)
            sec_dict[option] = None

    return sec_dict


def plotStorage(extraps, df, exp_str, now, plotDir, name):

    columns = ['Quota','Usage']
    cols = ['blue','green']
    lines = ['dashed','dashdot','dotted']
    lbl = ['quarter', 'week', 'fortnight']

    # Use quota values to set ylim
    ymax = 1.2 * df['Quota'].max()
    axlims = [0, ymax]

    fig, ax = plt.subplots(figsize=(10,8))

    if name == "scratch":
        ax.set_ylabel("PB")
    if name == "gdata":
        ax.set_ylabel("TB")

    for i in range(0, len(extraps)):
        extrap = extraps[i]['df']
        extrap.dropna(inplace=True)
        for c in range(0, len(cols)):
            if c == 0 and i==0:
                df[columns[c]].plot(ax=ax, ylim=axlims, color=cols[c], lw =2, label = columns[c] + " data")
                extrap.dropna()[columns[c]].plot(ax=ax,color=cols[c],ls=lines[i], label = columns[c] + " extrap.")
            elif c != 0:
                if i == 0:
                    df[columns[c]].plot(ax=ax,ylim=axlims, color=cols[c], lw = 2, label = columns[c] + " data")
                extrap[columns[c]].plot(ax=ax,color=cols[c],ls=lines[i], label = columns[c] + " extrap. " + lbl[i])

    TextDate = extrap.index[-1] + dt.timedelta(days=6) # x position for text
    ax.text( TextDate, axlims[-1]*1.0200, "Est. Exp. (LST)")
    ax.text( TextDate, axlims[-1]*0.9450, "%s" %(exp_str[0]))
    ax.text( TextDate, axlims[-1]*0.8950, "%s" %(exp_str[1]))
    ax.text( TextDate, axlims[-1]*0.8450, "%s" %(exp_str[2]))

    ax.legend(loc=2,ncol = 2, fontsize = 10)
    fig.suptitle("NCI project {} {} storage usage; updated {} AEST".format(proj, name, \
                dt.datetime.now().strftime('%Y-%m-%d %H:%M') ) )
    fig.tight_layout(rect=[0,0,0.85,0.97])

    print("Writing to {}/plots/Storage_{}_{}.png".format(plotDir, name, now.strftime(logDateFormat)))
    plt.savefig("{}/plots/Storage_{}_{}.png".format(plotDir, name, now.strftime(logDateFormat)))
    plt.close()


def plotSU(extraps, SUdf, exp_str, now, plotDir):

    columns = ['Grant','Used']
    cols = ['blue','green']
    lines = ['dashed','dashdot','dotted']
    lbl = ['quarter', 'week', 'fortnight']
    axlims = [0, 22]

    fig, ax = plt.subplots(figsize=(10,8))
    for i in range(0, len(extraps)):
        extrap = extraps[i]['df']
        extrap.dropna(inplace=True)
        for c in range(0, len(cols)):
            if c == 0 and i==0:
                SUdf[columns[c]].plot(ax=ax, ylim=axlims, color=cols[c], lw =2, label = columns[c] + " data")
                extrap.dropna()[columns[c]].plot(ax=ax,color=cols[c],ls=lines[i], label = columns[c] + " extrap.")
            elif c != 0:
                if i == 0:
                    SUdf[columns[c]].plot(ax=ax,ylim=axlims, color=cols[c], lw = 2, label = columns[c] + " data")
                extrap[columns[c]].plot(ax=ax,color=cols[c],ls=lines[i], label = columns[c] + " extrap. " + lbl[i])

    TextDate = extrap.index[-1] + dt.timedelta(days=6) # x position for text
    ax.text( TextDate, axlims[-1]*1.0100, "%s" %(exp_str[3]))

    ax.text( TextDate, axlims[-1]*0.9450, "Est. Exp. (LST)")
    ax.text( TextDate, axlims[-1]*0.8950, "%s" %(exp_str[0]))
    ax.text( TextDate, axlims[-1]*0.8450, "%s" %(exp_str[1]))
    ax.text( TextDate, axlims[-1]*0.7950, "%s" %(exp_str[2]))

    ax.set_ylabel("MSU")
    ax.legend(loc=2,ncol = 2, fontsize = 10)
    fig.suptitle("NCI project {} compute usage; updated {} AEST".format(proj, \
                dt.datetime.now().strftime('%Y-%m-%d %H:%M') ) )
    fig.tight_layout(rect=[0,0,0.85,0.97])

    print("Writing to {}/plots/SUUsage_{}.png".format(plotDir, now.strftime(logDateFormat)))
    plt.savefig("{}/plots/SUUsage_{}.png".format(plotDir, now.strftime(logDateFormat)))
    plt.close()


def main(args, runSU = True, runStorage = True):

    global suFileTemplate, lquotaFileTemplate, logDir, proj

    proj, logDir, lquotaDir, plotDir = parse_config(args.config)

    # Log file format templates
    suFileTemplate = proj + "_{dateStr}.rpt"
    lquotaFileTemplate = "lquota_{dateStr}.rpt"

    # Get current date/time
    #now = dt.datetime.utcnow()
    now = dt.datetime.now()
    nowStr = now.strftime(dateTimeFormat)

    # Start and end date of current quarter
    startDate, endDate = currentQuarter(now)

    if runSU:
        # 1. SU Usage
        # Create data frame for SU
        SUIndex = pd.date_range(startDate, endDate)
        columns = ["Grant", "Used", "Avail"]
        SUdf = pd.DataFrame( index=SUIndex, columns=columns)

        loopDate = startDate
        while loopDate <= now:
            suFileIn = filePath(suFileTemplate, loopDate, rootDir=logDir)

            # If file exists, extract date
            if os.path.exists(suFileIn) and os.stat(suFileIn).st_size > 0:
                fillSUdf(suFileIn, loopDate, SUdf)

            loopDate += dt.timedelta(days=1)

        # Now do the extrapolation and plotting
        extraps = []
        for arg in ['all', 7, 14]:
            df, col_dict = extrapolateUsage(SUdf, endDate, extrapDayWindow = arg)
            extraps.append({'df':df, 'col_params':col_dict})

        exp_str = []
        for extrap in extraps:
            if (extrap['df']['Used'][-1] > extrap['df']['Grant'][-1]):
                expDate = dt.timedelta(seconds = (extrap['df']['Grant'][-1] - extrap['col_params']['Used'][1])/extrap['col_params']['Used'][0]) + refdate
                exp_str.append( expDate.astimezone( pytz.timezone('Australia/Melbourne') ).strftime(logDateFormat) )
            else:
                per_quota = 100.0 * ((extrap['df']['Used'][-1] / extrap['df']['Grant'][-1] ))
                Within_str = "Pred. Usage (" + str(round(per_quota, 1)) + "%)"
                exp_str.append(Within_str)

        quota_used =100.0 * (SUdf.dropna()['Used'][-1] / SUdf.dropna()['Grant'][-1] )

        exp_str_context = []
        for arg, string in zip(['Quarter extrap.: ', '7 day extrap: ', '14 day extrap: '], exp_str):
            exp_str_context.append( arg + string)

        exp_str_context.append("Currently used %.01f%% of quota." %(quota_used) )

        plotSU(extraps, SUdf, exp_str_context, now, plotDir)
    else:
        print("INFO: runSU set to false")

    # 2. Look at gdata and scratch now
    if runStorage:
        # For these plots, plot last 2 months, project forward 1 month.
        startDate = now - relativedelta(months=+2)
        endDate = now + relativedelta(months=+1)

        # Reset loopDate
        loopDate = startDate

        dataIndex = pd.date_range(startDate.date(), endDate.date())
        columns = ["Usage", "Quota"]
        storageGdatadf = pd.DataFrame( index=dataIndex, columns=columns)
        storageScratchdf = pd.DataFrame( index=dataIndex, columns=columns)

        while loopDate <= now:
            dataFileIn = filePath(lquotaFileTemplate, loopDate, rootDir=lquotaDir)

            # If file exists, extract date
            if os.path.exists(dataFileIn):
                fillDatadf(dataFileIn, loopDate, storageGdatadf, "gdata")
                fillDatadf(dataFileIn, loopDate, storageScratchdf, "scratch")

            loopDate += dt.timedelta(days=1)

        for datadf, name in zip([storageGdatadf, storageScratchdf], ["gdata", "scratch"]):
            # Now do the extrapolation and plotting
            extraps = []
            for arg in ['all', 7, 14]:
                df, col_dict = extrapolateUsage(datadf, endDate, extrapDayWindow = arg)
                extraps.append({'df':df, 'col_params':col_dict})

            exp_str = []
            for extrap in extraps:
                if (extrap['df']['Usage'][-1] > extrap['df']['Quota'][-1]):
                    expDate = dt.timedelta(seconds = (extrap['df']['Quota'][-1] - extrap['col_params']['Usage'][1])/extrap['col_params']['Usage'][0]) + refdate
                    exp_str.append( expDate.astimezone( pytz.timezone('Australia/Melbourne') ).strftime(logDateFormat) )
                else:
                    per_quota = 100.0 * ((extrap['df']['Usage'][-1] / extrap['df']['Quota'][-1] ))
                    Within_str = "Pred. Usage (" + str(round(per_quota, 1)) + "%)"
                    exp_str.append(Within_str)

            exp_str_context = []
            for arg, string in zip(['Two month extrap.: ', '7 day extrap: ', '14 day extrap: '], exp_str):
                exp_str_context.append( arg + string)

            plotStorage(extraps, datadf, exp_str_context, now, plotDir, name)
    else:
        print("INFO: runStorage set to false")


if __name__ == '__main__':
    args = parse_args()
    main(args)
