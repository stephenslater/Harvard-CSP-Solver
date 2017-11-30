# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater
# Helper file to store Q-scores and prerequisites

import csv


# Global variables to avoid typing lots of strings later
strict = 'strict'
recommended = 'recommended'
one_of = 'one of'
all_of = 'all of'

# Q-score, workload, assignments, title
q = 'q'
w = 'w'
a = 'a'
t = 't'

# Dictionary mapping courses to their Q-scores
courses_to_q = dict()

# Dictionary mapping courses to the prereqs required for them
courses_to_prereqs = dict()

# Dictionary mapping courses to which courses should not be taken after
# e.g. Do not take Math 1b after Math 21b, or AM 21a after Math 21a
disable_future = dict()

# Other sets to help us organize classes
fall = set()
spring = set()
unknown = set()
undergrad = set()
grad = set()

# Convert Q-scores to floats, storing None if nonexistent
def q_helper(s):
	# print "S is {}".format(s)
	if len(s) == 0:
		return None
	else:
		return float(s)

# Converting prerequisites to set, returning empty set if nonexistent
def p_helper(s):
	if s:
		return set(s.split(';'))
	else:
		return set()

# Reads and stores Q-scores
def storeQdata(filename):
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter = ",")
		first = True

		for row in reader:
			if first:
				first = False
				continue

			if not row[0]:
				break

			# Stores Q-scores
			course = row[0]
			courses_to_q[course] = dict()
			courses_to_q[course][q] = q_helper(row[2])
			courses_to_q[course][w] = q_helper(row[3])
			courses_to_q[course][a] = q_helper(row[4])
			courses_to_q[course][t] = row[5]

			# Stores Fall or Spring class
			if row[1] == "Fall":
				fall.add(course)
			elif row[1] == "Spring":
				spring.add(course)
			else:
				fall.add(course)
				spring.add(course)

			# Stores Grad versus Undergrad class
			name = course.split()
			if name[1][0] == '2' and len(name[1]) > 2:
				grad.add(course)
			else:
				undergrad.add(course)


		# print "Q-scores for courses are {}".format(courses_to_q)
		# print "Fall classes are {}".format(fall)
		# print "Spring classes are {}".format(spring)
		# print "Unknown semester classes are {}".format(unknown)
		# print "Grad classes are {}".format(grad)
		# print "Undergrad classes are {}".format(undergrad)
	return fall, spring, courses_to_q

# Reads and stores prerequisites
# Does not yet handle 2 special cases that start with SPECIAL
def storePrereqs(filename):
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter = ",")
		first = True

		for row in reader:
			if first:
				first = False
				continue

			if not row[0]:
				break
			
			# Stores first 4 columns in dictionary
			course = row[0]
			courses_to_prereqs[course] = {strict: {one_of: set(), all_of: set()}, recommended: {one_of: set(), all_of: set()}}
			courses_to_prereqs[course][strict][all_of] = p_helper(row[1])
			courses_to_prereqs[course][strict][one_of] = p_helper(row[2])
			courses_to_prereqs[course][recommended][all_of] = p_helper(row[3])
			courses_to_prereqs[course][recommended][one_of] = p_helper(row[4])
			disable_future[course] = p_helper(row[5])

	# print "Prerequisites are {}".format(courses_to_prereqs)
	return courses_to_prereqs, disable_future


# storeQdata('courses_simple.csv')
# storePrereqs('prereqs_simple.csv')
			
