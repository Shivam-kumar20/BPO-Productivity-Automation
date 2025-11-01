import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# Macbook - Local Paths
productivity_path = '/Users/shivamkumar/Documents/Work/APR - Github/dummy_productivity_report.csv'
detail_path = '/Users/shivamkumar/Documents/Work/APR - Github/dummy_detail_report.csv'
mapping_path = '/Users/shivamkumar/Documents/Work/APR - Github/Mapping.xlsx'

def lwr(x):
    a = x.lower()
    return a


def chng_time(time_):
    t_=time_.total_seconds()
    hour_ = int(t_//3600)
    min_ = int((t_%3600)//60)
    sec_ = int(t_%60)
    result = str(hour_) + ":" + str(min_) + ":"  + str(sec_)
    return result

def total_connect(x):
    sum_ = x['Connected Inbound'] + x['Connected Manual Dials'] + x['Connected Auto Preview Dials']
    return sum_

def total_dial(x):
    sum_ = x['Inbound Received'] + x['Manual Dials'] + x['Auto Preview Dials']
    return sum_

def total_calls_(x):
    Total_Dial = x['Auto Preview Dials'] + x['Total_Dial']
    Total_Connect = x['Connected Auto Preview Dials'] + x['Total_Connect']
    return Total_Dial, Total_Connect

print('...Importing Dumps...')

apr_ = pd.read_csv(productivity_path)
cdr_ = pd.read_csv(detail_path)
map_ = pd.read_excel(mapping_path)

map_ = map_[['Email ID','Role','TL','Cluster Head','AGM']]
map_['Email ID'] = map_['Email ID'].apply(lwr)

print('...Working on Files...')

# Outbound Campaign dump
cpg = ['Corporate', 'Inorganic_OB', 'Organic_OB','Tollfree_Outbound']
scrb_ = apr_[apr_['Campaign Name'].isin(cpg)]
scrb_['User ID'] = scrb_['User ID'].apply(lwr)

scrb_['Total Staffed Duration'] = pd.to_timedelta(scrb_['Total Staffed Duration'])
scrb_ = scrb_.sort_values(by='Total Staffed Duration',ascending=False)
scrb_['Total Staffed Duration'] = scrb_['Total Staffed Duration'].apply(chng_time)

scrb_ = scrb_.drop_duplicates(subset = ['User ID'])

print('...Making Neccessary Columns...')

dial_ = apr_.groupby('User ID')[['Inbound Received','Manual Dials','Auto Preview Dials']].sum().reset_index()
dial_['Total_dial'] = dial_.apply(total_dial,axis=1)
dial_ = dial_[['User ID','Total_dial']]
dial_['User ID'] = dial_['User ID'].apply(lwr)

connect_ = apr_.groupby('User ID')[['Connected Inbound','Connected Manual Dials','Connected Auto Preview Dials']].sum().reset_index()
connect_['Total_Connect'] = connect_.apply(total_connect,axis = 1)
connect_ = connect_[['User ID', 'Total_Connect']]
connect_['User ID'] = connect_['User ID'].apply(lwr)

apr_['Total Talk Time in Interval'] = pd.to_timedelta(apr_['Total Talk Time in Interval'])
talk_ = apr_.groupby('User ID')['Total Talk Time in Interval'].sum().reset_index()
talk_['Total Talk Time'] = talk_['Total Talk Time in Interval'].apply(chng_time)
talk_ = talk_[['User ID', 'Total Talk Time']]
talk_['User ID'] = talk_['User ID'].apply(lwr)

cdr_['Customer Ringing Time'] = pd.to_timedelta(cdr_['Customer Ringing Time'])
ring_ = cdr_.groupby('User ID')['Customer Ringing Time'].sum().reset_index()
ring_['Customer Ringing Time'] = ring_['Customer Ringing Time'].apply(chng_time)
ring_['User ID'] = ring_['User ID'].apply(lwr)

print('...Merging All Files...')

scrb_map = (
    pd.merge(
        scrb_ ,
        map_ , 
        how = 'left', left_on = 'User ID', right_on = 'Email ID')
)

scrb_map_ring = pd.merge(scrb_map, ring_, on = 'User ID', how = 'inner')

scrb_map_ring_talk = pd.merge(scrb_map_ring, talk_, on = 'User ID', how = 'left')

scrb_map_ring_talk_dial = pd.merge(scrb_map_ring_talk, dial_, on = 'User ID', how = 'left')

scrb_map_ring_talk_dial_connect = pd.merge(scrb_map_ring_talk_dial, connect_, on = 'User ID', how = 'left')

scrb_map_ring_talk_dial_connect = scrb_map_ring_talk_dial_connect[['Process Name', 'Campaign Name', 'User Name', 'User ID', 
                                                                   'User Name', 'TL', 'Cluster Head', 'AGM', 'Role',
                                                                   'Total Staffed Duration', 'Total Ready Duration',
                                                                   'Total Break Duration', 'Total Idle Time', 'Avg. Ringing Time',
                                                                   'Avg. Talk Time', 'Avg. ACW Duration', 'Total Wrapped Calls',
                                                                   'Avg. Handling Time', 'Total Talk Time',
                                                                   'Total ACW Duration in Interval', 'Auto Call-On Duration',
                                                                   'Auto Call-Off Duration', 'Auto Dials', 'Inbound Received',
                                                                   'Manual Dials', 'Callbacks Received', 'Transfers Received',
                                                                   'Auto Dialer Ring Time', 'Auto Preview Ring Time', 'Inbound Ring Time',
                                                                   'Manual Ring Time', 'Manual Preview Ring Time',
                                                                   'Callback Calls Ring Time', 'Transfer To Campaign Ring Time',
                                                                   'Click To Calls Ring Time', 'Auto Dialer Talk Time',
                                                                   'Inbound Calls Talk Time', 'Manual Calls Talk Time',
                                                                   'Callback calls Talk Time', 'Transfer To Campaign Calls Talk time',
                                                                   'Auto Dialer Calls ACW Duration', 'Inbound Calls ACW Duration',
                                                                   'Manual Calls ACW Duration', 'Callback Calls ACW Duration',
                                                                   'Transfer To Campaign Calls ACW Duration', 'Connected Auto Dials',
                                                                   'Connected Inbound', 'Connected Manual Dials', 'Connected Callbacks',
                                                                   'Connected Transfers', 'Manual Preview Talk Time',
                                                                   'Manual Preview ACW Duration', 'Auto Preview Talk Time',
                                                                   'Auto Preview Calls ACW Duration', 'Click to Call Talk Time',
                                                                   'Click To Calls ACW Duration', 'Total Customer Hold Duration',
                                                                   'Avg. Customer Hold Duration', 'Connected Manual Preview Dials',
                                                                   'Manual Preview Dials','Total_dial',
                                                                   'Total_Connect', 'Click-To-Calls',
                                                                   'Connected Click-To-Calls', 'Total Ring Time', 'Total Preview Time',
                                                                   'Avg. Preview Time','Customer Ringing Time' ]]

scrb_map_ring_talk_dial_connect = scrb_map_ring_talk_dial_connect[scrb_map_ring_talk_dial_connect['Role'].isin(['Sales Executive', 'Assistant Team Leader', 'Intern'])]

export_path = '/Users/shivamkumar/Documents/Work/APR - Github/Scrubbed_APR.csv'

print('...File is Exporting...')
scrb_map_ring_talk_dial_connect.to_csv(export_path,index=False)

