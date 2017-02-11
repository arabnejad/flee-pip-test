import flee
import handle_refugee_data
import InputGeography
#handle_refugee_data.subtract_dates()
import numpy as np
import analysis as a
import sys

def AddInitialRefugees(e, d, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = int(d.get_field(loc.name, 0, FullInterpolation=True))
  for i in range(0, num_refugees):
    e.addAgent(location=loc)

def date_to_sim_days(date):
  return handle_refugee_data.subtract_dates(date,"2012-02-29")


if __name__ == "__main__":

  if len(sys.argv)>1:
    end_time = int(sys.argv[1])
    last_physical_day = int(sys.argv[1])
  else:
    end_time = 300
    last_physical_day = 300

  RetroFitting = False
  if len(sys.argv)>2:
    if "-r" in sys.argv[2]:
      RetroFitting = True
      end_time *= 10

  e = flee.Ecosystem()

  ig = InputGeography.InputGeography()

  ig.ReadLocationsFromCSV("iraq/iraq-locations.csv")

  ig.ReadLinksFromCSV("iraq/iraq-links.csv")

  lm = ig.StoreInputGeographyInEcosystem(e)

  camp_movechance = 0.001

  print("Network data loaded")


  #d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="mali2012/")


  print("Day,Mbera sim,Mbera data,Mbera error,Mentao sim,Mentao data,Mentao error,Bobo-Dioulasso sim,Bobo-Dioulasso data,Bobo-Dioulasso error,Abala sim,Abala data,Abala error,Mangaize sim,Mangaize data,Mangaize error,Niamey sim,Niamey data,Niamey error,Tabareybarey sim,Tabareybarey data,Tabareybarey error,Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),refugee_debt,Total error (retrofitted)")

  # Set up a mechanism to incorporate temporary decreases in refugees 
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.
 
  e.add_conflict_zone("Baghdad")

  # Start with a refugee debt to account for the mismatch between camp aggregates and total UNHCR data.
  #refugee_debt = e.numAgents()

  for t in range(0,end_time):

    e.refresh_conflict_weights()

    t_data = t
   
    new_refs = 100 
    """
    # Determine number of new refugees to insert into the system.
    new_refs = d.get_daily_difference(t, FullInterpolation=True, ZeroOnDayZero=False) - refugee_debt
    refugees_raw += d.get_daily_difference(t, FullInterpolation=True, ZeroOnDayZero=False)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0
    """

    # Here we use the random choice to make a weighted choice between the source locations.
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

    e.evolve()

    e.printInfo()

    """
    # Validation / data comparison
    camps = [m1,b1,b2,n1,n2,n3,n4]
    camp_names = ["Mbera", "Mentao", "Bobo-Dioulasso", "Abala", "Mangaize", "Niamey", "Tabareybarey"]
    # TODO: refactor camp_names using list comprehension.
 
    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents

    # calculate error terms.
    camp_pops = []
    errors = []
    abs_errors = []
    camp_pops_retrofitted = []
    errors_retrofitted = []
    abs_errors_retrofitted = []
    for i in range(0, len(camp_names)):
      # normal 1 step = 1 day errors.
      camp_pops += [d.get_field(camp_names[i], t, FullInterpolation=True)]
      errors += [a.rel_error(camps[i].numAgents, camp_pops[-1])]
      abs_errors += [a.abs_error(camps[i].numAgents, camp_pops[-1])]

      # errors when using retrofitted time stepping.
      camp_pops_retrofitted += [d.get_field(camp_names[i], t_retrofitted, FullInterpolation=True)]
      errors_retrofitted += [a.rel_error(camps[i].numAgents, camp_pops_retrofitted[-1])]
      abs_errors_retrofitted += [a.abs_error(camps[i].numAgents, camp_pops_retrofitted[-1])]

    # Total error is calculated using float(np.sum(abs_errors))/float(refugees_raw))

    locations = camps
    loc_data = camp_pops 

    #if e.numAgents()>0:
    #  print "Total error: ", float(np.sum(abs_errors))/float(e.numAgents())

    # write output (one line per time step taken.
    output = "%s" % (t)
    for i in range(0,len(locations)):
      output += ",%s,%s,%s" % (locations[i].numAgents, loc_data[i], errors[i])

    if float(sum(loc_data))>0:
      # Reminder: Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),Total error (retrofitted)
      output += ",%s,%s,%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, t_retrofitted, refugees_in_camps_sim, refugee_debt, float(np.sum(abs_errors_retrofitted))/float(refugees_raw))
    else:
      output += ",0,0,0,0,0,0,0"

    print(output)
    """    
   