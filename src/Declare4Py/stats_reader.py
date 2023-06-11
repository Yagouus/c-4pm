import pstats
import pm4py

# stats = pstats.Stats("../../result.stats")
# stats.print_stats()


log = pm4py.read_xes('../../output/generated_xes.xes')
# process_model = pm4py.discover_bpmn_inductive(log)
# pm4py.view_bpmn(process_model)

p = pm4py.discover_dfg(log)

# pm4py.view_dfg(p)
# fp_log = pm4py.discover_footprints(log)
# pm4py.save_vis_footprints(fp_log, 'op.svg')
