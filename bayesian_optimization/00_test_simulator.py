# %%
from pathlib import Path

from helpers import *

# %%
# base_path = '..'
# base_path = '.'
base_path = "/home/bench/Gitsrcs/origin_destination_bayes_opt"

# %%

od_duration_seconds = 5*60 

# duration of sample time for simulation output statistics
simulation_stat_freq_sec = od_duration_seconds
sim_end_time = od_duration_seconds

# begin="54000" end="57600"
# simulation_stat_freq_sec = 54000
# sim_end_time = 57600
# od_duration_seconds = sim_end_time - simulation_stat_freq_sec

# TODO : use SFO network
# gt_version_str = 'v4'
# taz2edge_xml = 'taz_new.xml'
# net_xml = 'SFO.net.xml'
# fixed_routes_xml = f'{base_path}/5hr_route_choice_set.csv'
# od_xml = f'gt_od_{gt_version_str}.xml'
# file_gt = f'{base_path}/gt_od_{gt_version_str}.xml'
# file_gt_edges = f'{base_path}/gt_edges_{gt_version_str}.csv'
# prefix_output = f'gt_{gt_version_str}'
# additional_xml = f'additional.add_statfreq{od_duration_seconds}.xml'
# EDGE_OUT_STR = 'edge_data_SFO.xml'

# TODO : currently using quickstart network for testing
# gt_version_str = 'qs'
# taz2edge_xml = 'network/quickstart/quickstart.taz.xml'
# net_xml = 'network/quickstart/quickstart.net.xml'
# fixed_routes_xml = f'{base_path}/quickstart_route.csv'
# od_xml = "network/quickstart/iter_quickstart.current_od.xml"
# file_gt = f"{base_path}/network/quickstart/iter_quickstart.current_od.xml"
# # file_gt_edges = "network/quickstart/quickstart.gt_edges.csv"
# additional_xml = f'network/quickstart/quickstart.additional.xml'
# prefix_output = "quickstart"
# EDGE_OUT_STR = f'edge_data_{prefix_output}.xml'

# TODO : currently using quickstart network for testing (quickstart2)
# network_name = "SFO"
from pathlib import Path

od_duration_seconds = 30*60 

# duration of sample time for simulation output statistics
simulation_stat_freq_sec = od_duration_seconds
sim_end_time = od_duration_seconds


network_name = "quickstart2"
model_name = "test_sim"

network_path = f"network/{network_name}"
taz2edge_xml = f"{base_path}/{network_path}/taz.xml"
net_xml = f"{base_path}/{network_path}/net.xml"
fixed_routes_xml = f"{base_path}/{network_path}/routes.csv"
od_xml = f"{network_path}/od.xml"       ## TODO : need to check if this is correct
file_gt = f"{base_path}/{network_path}/od.xml"      ## TODO : need to check if this is correct
# file_gt_edges                         ## TODO : need to check if this is necessary (not being used below)
additional_xml = f"{base_path}/{network_path}/additional.xml"
out_path = f"output/{network_name}_{model_name}"
prefix_output = f"output/{network_name}_{model_name}/"       ## TODO : need to check if this is correct
# prefix_output = f"{out_path}/out"     ## TODO : need to check if this is correct
gt_version_str = network_name           ## TODO : need to check if this is correct

EDGE_OUT_STR = f'edge_data_{network_name}.xml'
# suffix of simulation output edge file
TRIPS2ODS_OUT_STR = 'trips.xml'
# SUMO_PATH = '/usr/local/opt/sumo/share/sumo'
SUMO_PATH = "/usr/share/sumo"

Path(out_path).mkdir(parents=True, exist_ok=True)

# %%

# # gt v5:
# mean_od_val = 100
# num_ods = 100

# gt v4:
mean_od_val = 100
num_ods = 10

# # gt v3:
# mean_od_val = 0.05

# # gt v2:
# mean_od_val = 0.5
#num_ods = routes_df.shape[0]

# # gt v1:
# mean_od_val = 100
#num_ods = routes_df.shape[0]

print('if you want to optimize them all (~86k) set num_ods as defined in commented line below')
#num_ods = routes_df.shape[0]

# %%
# od_xml = f'gt_od_{gt_version_str}.xml'
# file_gt = f'{base_path}/gt_od_{gt_version_str}.xml'
# file_gt_edges = f'{base_path}/gt_edges_{gt_version_str}.csv'
# prefix_output = f'gt_{gt_version_str}'


# od_xml = "network/quickstart/quickstart.gt_od.xml"
# file_gt = f"{base_path}/network/quickstart/quickstart.gt_od.xml"
# file_gt_edges = "network/quickstart/quickstart.gt_edges.csv"
# prefix_output = "quickstart_gt"

# %%
# Get GT OD
print("Reading:",file_gt)
tree = ET.parse(file_gt)
root = tree.getroot()
gt_od_df =  xml2df_str(root, 'tazRelation')

gt_od_df.head()

# %%
print("Reading:",fixed_routes_xml)
routes_df = pd.read_csv(fixed_routes_xml, index_col=0)
print(routes_df)

# %%
od_xml

# %%
prefix_output

# %%
# simulate gt od
simulate_od(od_xml, 
            prefix_output, 
            base_path, 
            net_xml, 
            taz2edge_xml, 
            additional_xml,
            routes_df,
            sim_end_time,
            TRIPS2ODS_OUT_STR)

# %%
def od_xml_to_df(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()
    gt_od_df =  xml2df_str(root, 'tazRelation')
    
    gt_od_vals = gt_od_df['count'].astype(float)
    print('total GT demand: ',gt_od_vals.sum())

    return gt_od_df

# %%
gt_od_df = od_xml_to_df(file_gt)

# %% [markdown]
# ## Vary OD values adding Gaussian noise

# %%
gt_od_df['count'].astype(float).to_numpy()

# %%
num_epsilon_iter = 10
ods_epsilon = []

# Base OD which we will update their count entries
base_od = gt_od_df.copy()
gt_od_vals = gt_od_df['count'].astype(float).to_numpy()

for o1 in range(num_epsilon_iter):
    print(f"########### Epsilon {o1} ###########")

    file_od_epsilon_xml = f'{prefix_output}_gt_od_{gt_version_str}_epsilon{o1}.xml'
    # prefix_output = f'epsilon{o1}'
    prefix_output_eps = f'{prefix_output}_epsilon{o1}'
    # prefix_output = f"output/{network_name}/{network_name}"       ## TODO : need to check if this is correct

    # Generate OD
    curr_od = gt_od_vals.copy()
    curr_od = np.random.normal(gt_od_vals, gt_od_vals/30)

    print(f'total expected GT demand: {np.sum(curr_od)}')

    ###
    # create OD xml file 
    ###
    base_od['count'] = curr_od
    # round to 1 decimal point
    base_od['count'] = [round(elem, 1) for elem in base_od['count']]     
    base_od = base_od.rename(columns={'fromTaz':'from', 'toTaz':'to'})        
    create_taz_xml(file_od_epsilon_xml, base_od, od_duration_seconds, base_path)
    ods_epsilon.append(curr_od)
    
    # simulate gt od
    simulate_od(file_od_epsilon_xml, 
                prefix_output_eps, 
                base_path, 
                net_xml, 
                taz2edge_xml, 
                additional_xml, 
                routes_df,
                sim_end_time,
                TRIPS2ODS_OUT_STR)

# %%
num_gt_edges = 10
sim_edge_out = f'{base_path}/{prefix_output_eps}_{EDGE_OUT_STR}' # TODO : change this to read from output
df_edge_gt, _, _ = parse_loop_data_xml_to_pandas(base_path, sim_edge_out, prefix_output,SUMO_PATH)

df_edge_gt.head()

# %%
gt_edge_data = df_edge_gt\
        .sort_values(by=['interval_nVehContrib'], ascending=False)\
        .iloc[:num_gt_edges]

# %%
edge_epsilon_all = []
num_epsilon_iter = 10
for o1 in range(num_epsilon_iter):
    # curr_prefix = f'epsilon{o1}'
    curr_prefix = f'{prefix_output}_epsilon{o1}'

    sim_edge_out = f'{base_path}/{prefix_output_eps}_{EDGE_OUT_STR}'
    curr_loop_stats, _, _ = parse_loop_data_xml_to_pandas(base_path, sim_edge_out, curr_prefix,SUMO_PATH)
    edge_epsilon_all.append(curr_loop_stats)

# %%
loss_all = []
for o1 in range(num_epsilon_iter):
    curr_loss = compute_nrmse_counts_all_edges(gt_edge_data, edge_epsilon_all[o1])
    print(curr_loss)
    loss_all.append(curr_loss)


# %%
print("Number of ODs:",num_ods)
gt_od_df = routes_df[['fromTaz', 'toTaz']].drop_duplicates().iloc[:num_ods]

# %%



