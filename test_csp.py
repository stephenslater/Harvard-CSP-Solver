# Test file for CS-P: The Personal CS Concentration Solver
# CS 182 Final Project, Fall 2017
# Authors: Menaka Narayanan and Stephen Slater
# Important: Change the graph output file names at end of file to avoid file loss

import csp
import load
import time
import copy
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

# Parse data from Excel files
fall, spring, courses_to_q = load.storeQdata('courses.csv')
courses_to_prereqs, disable_future = load.storePrereqs('prerequisites.csv')

# Initialize parameters of the CSP
variables = (fall, spring)
constraints = courses_to_prereqs, disable_future

# Constraints specified by user
classes_per_semester = 2
q_score = 3.3
workload = 30.0
assignments = 2.0

# Variables for plot generation and analysis, including number of solutions to generate
total_solutions = 50
data = {}
all_attempts = []
all_times = []
titles = []

# Binary representations of which heuristics are active
heuristic_flags = ['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
# heuristic_flags = ['1111']

def test_cases():

	# User should not be able to specify a "must take" in the past, since history is greater 
	history = [(5, 'CS 182')]
	must_take = [(4, 'CS 124')]
	priors = {'prior_math'}
	heuristics = {'mrv': True, 'lcv': True, 'fc': True, 'ac': True}
	test = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take, priors, total_solutions)
	attempts, solutions = test.solve(heuristics)
	assert (attempts == 0) and (solutions == []) 

	# User should get error message when trying to guarantee the same course twice
	history = []
	must_take = [(3, 'CS 121'), (7, 'CS 121')]
	priors = {'prior_cs'}
	heuristics = {'mrv': True, 'lcv': True, 'fc': True, 'ac': False}
	test = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take, priors, total_solutions)
	attempts, solutions = test.solve(heuristics)
	assert (attempts == 0) and (solutions == []) 	

	# User should receive error message when trying to guarantee a course in an invalid semester
	history = []
	must_take = [(4, 'CS 182')]
	priors = {'adv_math'}
	heuristics = {'mrv': False, 'lcv': True, 'fc': True, 'ac': False}
	test = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take, priors, total_solutions)
	attempts, solutions = test.solve(heuristics)
	assert (attempts == 0) and (solutions == []) 	

	# We could generate solutions and check that they are valid, but is_complete does that within CSP_Solver.
	print "\nAll tests passed! And we know all solutions are valid from CSP_Solver.is_complete."

# Generate graphs/data of heuristic-combination comparisons based on chosen history, etc.
def generate_graphs():
	# Uncomment the desired scenario for testing and generating graphs
	# Scenario 1
	history = []
	must_take = []
	priors = {'prior_cs', 'adv_math'}

	# Scenario 2
	# history = [(1, 'CS 50'), (1, 'AM 21a')]
	# must_take = [(7, 'CS 182')]
	# priors = {'prior_math'}

	# Scenario 3
	# history = [(1, 'CS 50'), (1, 'Math 21a'), (2, 'CS 51'), (2, 'AM 21b'), (3, 'CS 121')]
	# must_take = [(4, 'CS 124')]
	# priors = {'prior_cs', 'prior_math'}

	problem = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take, priors, total_solutions)

	print "\nProblem 1"
	for combo in heuristic_flags:
		# problem_1 = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history_1, must_take_1, priors_1, total_solutions)
		mrv = bool(int(combo[0]))
		lcv = bool(int(combo[1]))
		fc = bool(int(combo[2]))
		ac = bool(int(combo[3]))
		print "Heuristics: {}".format(combo)
		print "MRV: {}, LCV: {}, FC: {}, AC: {}".format(mrv, lcv, fc, ac)
		heuristics = {'mrv': mrv, 'lcv': lcv, 'fc': fc, 'ac': ac}
		test = copy.deepcopy(problem)

		start = time.time()
		attempts, solutions = test.solve(heuristics)
		end = time.time()

		time_taken = end - start

		# Group results for a given heuristic combination and extract later
		data[combo] = {'a': attempts, 's': solutions, 't': time_taken}

		title = []
		if mrv:
			title.append('M')
		if lcv:
			title.append('L')
		if fc:
			title.append('F')
		if ac:
			title.append('A')
		title = '/'.join(title)
		if title == '':
			title = 'None'
		titles.append(title)

		print "\nCombo: {}. Story: history: {}, must_take: {}".format(combo, history, must_take)
		print "Time: {}".format(time_taken)
		print "Attempts: {}".format(attempts)
		print "Solutions: {}".format(len(solutions))
		if len(solutions) == 0:
			print "\nNo solutions found. Suggestions to try:"
			print "- Higher workload (https://blog.collegevine.com/managing-extracurriculars-a-guide-to-strategic-quitting)"
			print "- Lower q-score avg (glassdoor.com/List/Highest-Paying-Jobs-LST_KQ0,19.htm)"
			print "- Lower assignment quality avg."
			print "- Take prereqs before specifying \'must take\' courses early"

	# Compile data
	for combo in heuristic_flags:
		all_attempts.append(data[combo]['a'])
		all_times.append(data[combo]['t'])	

	# Width of plot based on how many combinations we have (16)
	y_pos = np.arange(len(titles))

	print "Story 3"

	for i in range(len(heuristic_flags)):
		print "\nCombo: {}, Title: {}, Attempts: {}, Time: {}, Solutions: {}".format(heuristic_flags[i], titles[i], data[heuristic_flags[i]]['a'], data[heuristic_flags[i]]['t'], len(data[heuristic_flags[i]]['s']))

	# Plot the results (# of rec. calls and runtime to reach 50 solutions per combination)
	plt.figure(1)
	plt.barh(y_pos, all_attempts, align='center', color='tab:blue', alpha=0.5)
	plt.yticks(y_pos, titles)
	plt.xlabel('Recursive Calls (number)')
	plt.ylabel('Combination of Backtracking Heuristics')
	plt.title('Recursive Calls vs. Backtracking Heuristics')
	 
	# IMPORTANT: Change file name below on each execution
	plt.figure(2)
	plt.barh(y_pos, all_times, align='center', color='tab:green', alpha=0.5)
	plt.yticks(y_pos, titles)
	plt.xlabel('Runtime (s)')
	plt.ylabel('Combination of Backtracking Heuristics')
	plt.title('Runtime (n = 50 solutions) vs. Backtracking Heuristics')
	 
	# IMPORTANT: Change file name below on each execution
	plt.show()

# generate_graphs()
test_cases()
