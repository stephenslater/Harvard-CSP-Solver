# File for users to input specifications for the Harvard CS Concentration Solver
# Harvard CS 182, Fall 2017
# Authors: Menaka Narayanan and Stephen Slater

import csp
import load
import copy
import random

# Parse data from Excel files
fall, spring, courses_to_q = load.storeQdata('courses.csv')
courses_to_prereqs, disable_future = load.storePrereqs('prerequisites.csv')

# Initialize parameters of the CSP
variables = (fall, spring)
constraints = courses_to_prereqs, disable_future

#######################################

# Choose what you'd like! We've prepopulated a couple of cases for you.

# Constraints specified by user
# Case 1
# classes_per_semester = 2 # max concentration courses willing to take
# q_score = 3.3 # min average q score of classes in a semester
# workload = 30.0 # max workload in hours/week from concentration courses in a semester
# assignments = 2.0 # min average assignment quality of classes in a semester
# total_solutions = 50 # Number of solutions to generate before returning yours

# history = []
# must_take = [(6, 'CS 124')]
# priors = {'adv_math'} # Only specify this if you are a freshman and need math
# heuristics = {'mrv': False, 'lcv': True, 'fc': True, 'ac': False}

#######################################

# Case 2
classes_per_semester = 2 
q_score = 3.3 
workload = 35.0 
assignments = 2.5 
total_solutions = 50 

history = [(1, 'CS 50'), (1, 'AM 21a'), (2, 'AM 21b'), (2, 'CS 51'), (3, 'Stat 110'), (4, 'CS 124')]
must_take = [(5, 'CS 182')]
priors = {'prior_cs', 'prior_math'} 
heuristics = {'mrv': True, 'lcv': True, 'fc': True, 'ac': True}

#######################################


print "Your history: {}".format(history)
print "Your desired courses: {}".format(must_take)
print "Your priors: {}".format(priors)

test = csp.CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take, priors, total_solutions)

attempts, solutions = test.solve(heuristics)
print "Solution count: {}".format(len(solutions))

if not solutions:
	print "\nOh no! We couldn't find a solution for you."
	print "Suggestions to try:"
	print "1. Higher workload (https://blog.collegevine.com/managing-extracurriculars-a-guide-to-strategic-quitting)"
	print "2. Lower q-score avg (glassdoor.com/List/Highest-Paying-Jobs-LST_KQ0,19.htm)"
	print "3. Lower assignment quality avg."
	print "4. Take prereqs before specifying \'must take\' courses early"
else:
	random.shuffle(solutions)
	k = min(10, len(solutions))
	results = random.sample(solutions, k)
	for count, sol in enumerate(results):
		print "\nSolution {}:".format(count + 1)
		for i in range(1, 9):
			sol[i].print_courses()