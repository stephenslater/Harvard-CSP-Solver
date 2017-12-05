# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater

import random
import load
import time
import copy
import matplotlib.pyplot as plt

# Full course domain
# fall, spring, courses_to_q = load.storeQdata('courses.csv')
# courses_to_prereqs, disable_future = load.storePrereqs('prerequisites.csv')

# Medium test domain
# fall, spring, courses_to_q = load.storeQdata('courses_medium.csv')
# courses_to_prereqs, disable_future = load.storePrereqs('prereqs_medium.csv')

# Small test domain
fall, spring, courses_to_q = load.storeQdata('courses_small.csv')
courses_to_prereqs, disable_future = load.storePrereqs('prereqs_small.csv')

# If we use model where we free future courses after prereqs
# prereqs_to_courses = {} 

strict = 'strict'
recommended = 'recommended'
one_of = 'one of'
all_of = 'all of'
multivar = set(['AM 21a', 'Math 21a', 'Math 23b', 'Math 25b', 'Math 55b'])
linalg = set(['AM 21b', 'Math 21b', 'Math 23a', 'Math 25a', 'Math 55a'])

# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

class Semester(object):
	def __init__(self, domain, semester, specified):
		self.semester = semester
		self.max_courses, self.min_q, self.max_w, self.min_a, self.prereqs, self.csp = specified
		self.course_count = 0
		self.assigned = set()
		self.available = set(domain)

		# If we decide to free future courses based on previous ones first
		# self.unavailable = set()

		# Variables we probably won't need
		# self.course_qs = []
		# self.avg_q = 0.
		# self.w = 0.
		# self.course_as = []
		# self.avg_a = 0.

	# When trying to add course, make sure it doesn't violate q-scores, etc.
	def forward_check(self, potential_course):
		self.assigned.add(potential_course)
		self.course_count += 1
		avg_q = float(sum([courses_to_q[course][q] for course in self.assigned])) / self.course_count
		work = float(sum([courses_to_q[course][w] for course in self.assigned]))
		avg_a = float(sum([courses_to_q[course][a] for course in self.assigned])) / self.course_count

		if avg_q < self.min_q or work > self.max_w or avg_a < self.min_a:
			self.assigned.remove(potential_course)
			self.course_count -= 1
			# print "Couldn't add {} to semester {}".format(potential_course, self.semester)
			return False
		# print "Adding {} to semester {}".format(potential_course, self.semester)

		return True

	def add_course(self, current_state, course, heuristics=False):
		if self.course_count < self.max_courses and self.csp.check_prereqs(current_state, course, self.semester):
			# reqs = self.prereqs[course]
			# prev_courses = self.csp.get_previous(self.semester)
			# if self.check_prereqs(course):
			if heuristics:
				return self.forward_check(course)

			self.assigned.add(course)
			self.course_count += 1
			return True				

			# No forward checking in this version. If there aren't prereqs, add it
			# if self.check_prereqs():
			# if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
			#    len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
			# 	self.assigned.add(course)
			# 	self.course_count += 1
			# 	return True

			# # If there are prereqs, we need to fulfill them and account for different math series
			# else:
			# 	maths = {'Math 21a', 'Math 21b'}
			# 	recommended_all = (reqs[recommended][all_of] - prev_courses == set())
			# 	if 'Math 21a' in reqs[recommended][all_of]:
			# 		if len(prev_courses & multivar) > 0:
			# 			if 'Math 21b' in reqs[recommended][all_of]:
			# 				if len(prev_courses & linalg) > 0:
			# 					recommended_all = (reqs[recommended][all_of] - maths - prev_courses == set())
			# 			else:
			# 				recommended_all = (reqs[recommended][all_of] - {'Math 21a'} - prev_courses == set())
			# 	elif 'Math 21b' in reqs[recommended][all_of]:
			# 		if len(prev_courses & linalg) > 0:	
			# 			recommended_all = (reqs[recommended][all_of] - {'Math 21b'} - prev_courses == set())	

			# 	# Now that we've defined all the ways to fulfill math, make sure we fulfill reqs
			# 	if ((len(reqs[strict][one_of]) == 0) or (len(reqs[strict][one_of] & prev_courses) > 0)) and \
			# 	   reqs[strict][all_of] - prev_courses == set() and \
			# 	   ((len(reqs[recommended][one_of]) == 0) or (len(reqs[recommended][one_of] & prev_courses) > 0)) and \
			# 	   recommended_all:
			# 		self.assigned.add(course)
			# 		self.course_count += 1
			# 		return True
		return False

	# def add_course_FC(self, course):
	# 	# reqs = self.prereqs[course]
	# 	if self.course_count < self.max_courses and self.csp.check_prereqs(course, self.semester):
	# 		# prev_courses = self.csp.get_previous(self.semester)
	# 		# if self.check_prereqs():
	# 		return self.forward_check(course)

	# 		# TODO: combine this if-else block
	# 		# There are no prereqs, so make sure that adding it is okay
	# 		# if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
	# 		#    len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
	# 		# 	return self.forward_check(course)

	# 		# # If there are prereqs, we need to fulfill them and account for different math series
	# 		# else:
	# 		# 	maths = {'Math 21a', 'Math 21b'}
	# 		# 	recommended_all = (reqs[recommended][all_of] - prev_courses == set())
	# 		# 	if 'Math 21a' in reqs[recommended][all_of]:
	# 		# 		if len(prev_courses & multivar) > 0:
	# 		# 			if 'Math 21b' in reqs[recommended][all_of]:
	# 		# 				if len(prev_courses & linalg) > 0:
	# 		# 					recommended_all = (reqs[recommended][all_of] - maths - prev_courses == set())
	# 		# 			else:
	# 		# 				recommended_all = (reqs[recommended][all_of] - {'Math 21a'} - prev_courses == set())
	# 		# 	elif 'Math 21b' in reqs[recommended][all_of]:
	# 		# 		if len(prev_courses & linalg) > 0:	
	# 		# 			recommended_all = (reqs[recommended][all_of] - {'Math 21b'} - prev_courses == set())	

	# 		# 	# Now that we've defined all the ways to fulfill math, make sure we fulfill reqs
	# 		# 	if ((len(reqs[strict][one_of]) == 0) or (len(reqs[strict][one_of] & prev_courses) > 0)) and \
	# 		# 	   reqs[strict][all_of] - prev_courses == set() and \
	# 		# 	   ((len(reqs[recommended][one_of]) == 0) or (len(reqs[recommended][one_of] & prev_courses) > 0)) and \
	# 		# 	   recommended_all:
	# 		# 	    return self.forward_check(course)
	# 	return False

	# I added these conditionals because we were getting a key error, but have commented them out -m
	def remove_course(self, course):
		#if course in self.assigned:
		self.assigned.remove(course)
		#if course not in self.available:
		self.available.add(course)
		self.course_count -= 1
		return None

	def print_courses(self):
		print "Semester {}: {}".format(self.semester, self.assigned)

	# def open_course(course):
	# 	# Consider case when a course has multiple prereqs and we can't free it yet
	# 	if course in self.unavailable:
	# 		# Check if all prereqs fulfilled for course
	# 		self.unavailable.remove(course)
	# 		self.available.add(course)

	# 	return True

#
# SUGGESTION: Define Semester class as a class within CSP_Solver so that
# we can avoid repetition like "Semester(__, __, specified)" and just access
# data from CSP_Solver directly.
# See: https://stackoverflow.com/questions/1765677/nested-classes-scope
#
class CSP_Solver(object):
	def __init__(self, variables, constraints, num_classes, q_score, workload, assignments, history, heuristics=False):
		self.fall, self.spring = variables
		self.prereqs_to_courses, self.disable_future = constraints
		self.n = num_classes
		self.history = history
		self.min_q = q_score
		self.max_w = workload
		self.min_a = assignments
		specified = (num_classes, q_score, workload, assignments, constraints[0], self)
		self.all = set()
		self.num_solutions = 0
		self.attempts = 0
		self.seen_plans = set()
		self.latest_sem = 0

		# A plan of study for 8 semesters
		# Each semester has max n concentration courses
		# In each semester, we store sets of assigned, available, and unavailable courses
		start = {1: Semester(fall, 1, (2, q_score, workload, assignments, constraints[0], self)), 
				 2: Semester(spring, 2, specified),
				 3: Semester(fall, 3, specified), 
				 4: Semester(spring, 4, specified),
				 5: Semester(fall, 5, specified), 
				 6: Semester(spring, 6, specified),
				 7: Semester(fall, 7, specified), 
				 8: Semester(spring, 8, specified) 
			}

		# Populate state with classes user has already taken; remove them from future
		# latest_sem = 0
		for course, semester in history:
			self.latest_sem = max(semester, self.latest_sem)
			start[semester].assigned.add(course)
			self.all.add(course)
			start[semester].course_count += 1
			for s in range(1, 9):
				if course in start[s].available:
					start[s].available.remove(course)

		# print "Latest sem is {}".format(latest_sem)
		# for sem in range(latest_sem):
		# 	start[sem+1].max_courses = start[semester].course_count

		# for i in range(1, 9):
		# 	if start[semester].course_count > 0:
		# 		start[semester].max_courses = start[semester].course_count


			# Model where we free courses after taking their prereqs instead of looking back
			# Still have future semester to fulfil prereqs for
			# 	if semester < 8:

			# 		# Remove from unassigned domains in future semesters anything that
			# 		# we have fulfilled the prereq for
			# 		if course in prereqs_to_courses:
			# 			for class_enabled in prereqs_to_courses[course]:
			# 				for i in range(semester, 9):
			# 					start[semester].open_course(class_enabled)

		self.state = start

	# Check if all concentration requirements (e.g. theory, breadth, depth) fulfilled
	# Check if all prerequisites satisfied before taking a given class
	# If not using forward checking,
		# Check that average q, workload, and average a meet requirements
	def is_complete(self, assignment): #, forward=False):

		# If we've already seen this assignment at this semester given previous semester
		# Then don't count it as a new solution in this function
		# If we haven't seen it, then add it to some solutions seen set
		# We can handle this by just adding every assignment to a visited set
		# And never try again if we've already seen a combination of (A, B, C)
		# Regardless of whether (A, B, C) is a solution
		# I.e. if we've seen it before, return false on is_complete, and somehow we 
		# don't want to do more recursive calls for anything after, since we will have 
		# done them already

		# print "assignment: {}".format(assignment)
		# print "assignment.all: {}".format(assignment.all)
		# print "assgnment state: {}".format(assignment.state)

		# print "Printing potential solution"
		# for k in range(1,9):
		# 	assignment.state[k].print_courses()

		basic_1 = set(['Math 1a', 'Math 1b', 'CS 20', 'Math 21b'])
		basic_2 = set(['Math 1a', 'Math 1b', 'CS 20', 'AM 21b'])
		multivar = set(['AM 21a', 'Math 21a', 'Math 23b', 'Math 25b', 'Math 55b'])
		linalg = set(['AM 21b', 'Math 21b', 'Math 23a', 'Math 25a', 'Math 55a'])
		software_1 = set(['CS 50', 'CS 51'])
		software_2 = set(['CS 51', 'CS 61'])
		software_3 = set(['CS 50', 'CS 61'])
		theory_1 = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
		technical_1 = set(['CS 51', 'CS 61',
		               'CS 96', 'CS 105', 'CS 108', 'CS 109A', 'CS 109B', 
		               'CS 124', 'CS 126', 'CS 127', 'CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 144R', 
		               'CS 148', 'CS 152', 'CS 161', 'CS 165', 'CS 171', 'CS 175',
		               'CS 179', 'CS 181', 'CS 182', 'CS 189', 'CS 191', 'Stat 110', 'Math 154', 'AM 106',
		               'AM 107', 'AM 120', 'AM 121', 'ES 153'])
		breadth_1 = set(['CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 144R', 
		               'CS 146', 'CS 148', 'CS 152', 'CS 153', 'CS 161', 'CS 165', 'CS 171', 'CS 175', 
		               'CS 179', 'CS 181', 'CS 182', 'CS 189', 'ES 153']) 

		math = not (basic_1 - assignment.all) or not (basic_2 - assignment.all) or \
				   (len(multivar & assignment.all) > 0 and len(linalg & assignment.all) > 0)

		software = software_1 - assignment.all == set() or software_2 - assignment.all == set() or software_3 - assignment.all == set()
		all_3 = {'CS 50', 'CS 51', 'CS 61'} - assignment.all == set()


		theory_courses = theory_1 & assignment.all
		theory = 'CS 121' in assignment.all and len(theory_courses) > 0

		if theory_courses != set():
			theory_course = random.choice(list(theory_courses))
			technical_1 -= set([theory_course])

		if all_3 or (software_1 - assignment.all == set()) or (software_3 - assignment.all == set()):
			technical = (len((technical_1.union({'ES 50'})) & assignment.all) >= 5 or len((technical_1.union({'ES 52'})) & assignment.all) >= 5)
		
		elif software_2 - assignment.all == set():
			technical = (len((technical_1.union({'ES 50'})) & assignment.all) >= 6 or len((technical_1.union({'ES 52'})) & assignment.all) >= 6)

		# Handle special cases where student takes all of CS 50/51/61 or ES 153
		counter = 0
		subject = ''
		if all_3:
			counter += 1
		if 'ES 153' in assignment.all:
			counter += 1
			subject = '4'
		
		# if self.honors: 6 technical, 4 breadth
		for c in assignment.all:
			# Non honors requires 2 breadth courses of different subjects
			if counter < 2:
				if c in breadth_1 and c[4] != subject:
					counter += 1
					subject = c[4]

		breadth = (counter == 2)

		# Only do this computation if we didn't forward check these constraints
		if not assignment.heuristics:
			#print "Not using forward checking"
			for semester in range(1,9):
				course_count = assignment.state[semester].course_count

				course_qs = [courses_to_q[course][q] for course in assignment.state[semester].assigned]
				workloads = [courses_to_q[course][w] for course in assignment.state[semester].assigned]
				course_as = [courses_to_q[course][a] for course in assignment.state[semester].assigned]

				if course_count > 0:
					avg_q = float(sum(course_qs)) / course_count
					work = float(sum(workloads))
					avg_a = float(sum(course_as)) / course_count
					if avg_q < assignment.min_q or work > assignment.max_w or avg_a < assignment.min_a:
						return False

		return math and software and theory and technical and breadth

	# Look at all previous semesters when determining prereq satisfaction; no simultaneity allowed
	def get_previous(self, current_state, semester, tuple_version = False):
		if tuple_version:
			final = []
			for i in range(1, semester):
				final.append(tuple(current_state[i].assigned))
			return final

		else:
			prev_courses = set()
			for i in range(1, semester):
				prev_courses = prev_courses.union(current_state[i].assigned)
			return prev_courses	

	# Checks if we have already computed this combination given all previous semester
	# Another way to do this would be to store the current_plan thru prev semesters
	# instead of computing it every time, but would have to deal with resetting it
	def already_computed(self, current_state, semester, current_semester):
		current_plan = self.get_previous(current_state, semester, tuple_version=True)
		# print current_plan
		current_plan.append(current_semester)
		current_plan = tuple(current_plan)
		if current_plan not in self.seen_plans:
			self.seen_plans.add(current_plan)
			return False
		return True

	def check_prereqs(self, current_state, course, semester):
		# print "Checking prereqs for {} in semester {}".format(course, semester)
		reqs = self.prereqs_to_courses[course]
		if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
		   len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
		   	# print "Yes\n"
		   	return True

		prev_courses = self.get_previous(current_state, semester)

		maths = {'Math 21a', 'Math 21b'}
		recommended_all = (reqs[recommended][all_of] - prev_courses == set())

		if 'Math 21a' in reqs[recommended][all_of]:
			if len(prev_courses & multivar) > 0:
				if 'Math 21b' in reqs[recommended][all_of]:
					if len(prev_courses & linalg) > 0:
						recommended_all = (reqs[recommended][all_of] - maths - prev_courses == set())
				else:
					recommended_all = (reqs[recommended][all_of] - {'Math 21a'} - prev_courses == set())
		elif 'Math 21b' in reqs[recommended][all_of]:
			if len(prev_courses & linalg) > 0:	
				recommended_all = (reqs[recommended][all_of] - {'Math 21b'} - prev_courses == set()) 

		# Now that we've defined all the ways to fulfill math, make sure we fulfill reqs
		if ((len(reqs[strict][one_of]) == 0) or (len(reqs[strict][one_of] & prev_courses) > 0)) and \
		   reqs[strict][all_of] - prev_courses == set() and \
		   ((len(reqs[recommended][one_of]) == 0) or (len(reqs[recommended][one_of] & prev_courses) > 0)) and \
		   recommended_all:
		   	# print "Yes\n"
			return True
		# print "No\n"
		return False

	# Return the variable with the minimum positive # of remaining values
	def get_mrv(self, current_state):
		# print "\n\n\n\nFinding variables with MRV"
		minimum = float('inf')
		lowest = []

		for i in range(self.latest_sem + 1, 9):
			if current_state[i].course_count != current_state[i].max_courses:
				valids = set()
				for course in current_state[i].available:
					if self.check_prereqs(current_state, course, i):
						valids.add(course)
					
				size = len(valids)
				if current_state[i].course_count < current_state[i].max_courses:
					if 0 < size < minimum:
						minimum = size
						lowest = [i]

		return lowest

	# Return the least constraining value (course) to be assigned of available
	# This should be called from order_domain_values
	# The purpose is to choose a value from the available set that doesn't
	# constrain other semesters' possibilities
	def get_lcv(self):
		pass
		# LCV

	# Use Min Remaining Value and Least Constraining Value heuristics
	# Return multiple semesters from which to branch out: check
	# Stop assigning courses when assignment is complete:
	def get_unassigned_var(self, current_state):

		# MRV
		if self.heuristics:
			return self.get_mrv(current_state)

		# Choose semesters in order
		for semester in range(self.latest_sem + 1, 9):
			if current_state[semester].course_count != current_state[semester].max_courses:
				return [semester]
		return None

		# Choose a semester randomly

		# Double branching
		# for semester in range(self.latest_sem + 1, 9):
		# 	if self.state[semester].course_count != self.state[semester].max_courses:
		# 		if semester < 8:
		# 			if self.state[semester + 1].course_count != self.state[semester + 1].max_courses:
		# 				return [semester, semester + 1]
		# 			return [semester]
		# 		return [semester]
			
		# return None

		# Triple branching
		# for semester in range(1, 9):
		# 	if self.state[semester].course_count < self.state[semester].max_courses:
		# 		if semester < 8:
		# 			if self.state[semester+1].course_count < self.state[semester+1].max_courses:
		# 				if semester != 7:
		# 					if self.state[semester+2].course_count < self.state[semester+2].max_courses:
		# 						return [semester, semester + 1, semester + 2]
		# 				else:
		# 					return [semester, semester + 1]				
		# 		return [semester]
		# return None

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object can take n courses
	def solve(self, heuristics=False):
		def rec_backtrack(assignment):
			# Number of function calls, used to compare algorithms

			self.attempts += 1
			if self.is_complete(assignment):
				self.num_solutions += 1
				solutions.append(assignment.state)
			else:
				# Gets next semesters needing additional courses
				semesters = self.get_unassigned_var(assignment.state)
				#print "Unassigned semesters are {}".format(semesters)
				if semesters:
					for semester in semesters:
						# Wrapper to avoid key error
						all_vals = assignment.state[semester].available.union(assignment.state[semester].assigned)
						# all_vals = assignment.state[semester].available

						count_all_vals = len(all_vals)
						# Iterates through every candidate class
						# temp = assignment.state[semester].assigned

						tries = 0
						count_available = len(assignment.state[semester].available)
						for value in all_vals:
							# Class is available to be assigned
							if value in assignment.state[semester].available:
								tries += 1
								temp_assigned = tuple(assignment.state[semester].assigned.union(set([value])))
								# Checks for duplicate semesters
								if not self.already_computed(assignment.state, semester, temp_assigned):
									if assignment.state[semester].add_course(assignment.state, value, heuristics):
										assignment.all.add(value)
										# Removes this class from all future semesters
										for s in range(semester, 9):
											if value in assignment.state[s].available:
												assignment.state[s].available.remove(value)

										# Don't want to allow for taking courses simultaneously?
										# I.e. if Math 21a disabled AM 21a in the future,
										# We want to disable AM21a from right now as well
										# So we can maybe change this to be in range(semester, 9) --> CHANGE MADE -m
										
										# NEW VERSION: Remove disabled courses from this and future semesters
										# for n in range(semester, 9):
										# 	for to_disable in disable_future[value]:
										# 		if to_disable in self.state[n].available:
										# 			self.state[n].available.remove(to_disable)
										
										# OLD VERSION
										for q in range(semester, 9):
											for j in assignment.disable_future[value]:
												if j in assignment.state[q].available:
													assignment.state[q].available.remove(j)													

										new_version = copy.deepcopy(assignment)
										result = rec_backtrack(new_version)
										# print "All: {}".format(self.all)
										# self.state[semester].print_courses()
										# print "Course to remove is {}".format(value)
										assignment.state[semester].remove_course(value)

										# Added this conditional to fix key error
										# if value in self.all:
										assignment.all.remove(value)

										# Add the course back for future options
										# Only add it back to its valid semester(s),
										# since some courses are offered fall and spring
										# In addition to adding back "value", we should
										# add back courses that we had disabled by taking value
										# I think this should be range(semester, 9) instead?

										# NEW VERSION: UPDATE: This breaks things
										# for n in range(semester, 9):
										# 	for prev_disabled in disable_future[value]:
										# 		if n % 2 == 1:
										# 			if prev_disabled in fall:
										# 				self.state[n].available.add(prev_disabled)
										# 		else:
										# 			if prev_disabled in spring:
										# 				self.state[n].available.add(prev_disabled)

										# OLD VERSION
										for n in range(1, 9):
											if n % 2 == 1:
												if value in fall:
													assignment.state[n].available.add(value)
											else:
												if value in spring:
													assignment.state[n].available.add(value)
						
									# print "Before calls: {}".format(temp)
									# print "After calls: {}".format(assignment.state[semester].assigned)
									else:
										# if count == count_all_vals - 1:
										if tries == count_available:
											if len(assignment.state[semester].assigned) < assignment.state[semester].max_courses:
												new_version = copy.deepcopy(assignment)
												new_version.state[semester].max_courses = new_version.state[semester].course_count
												rec_backtrack(new_version)

						# here
					return False

		self.heuristics = heuristics
		self.seen_plans = set()
		self.num_solutions = 0
		self.attempts = 0
		solutions = []

		# Begin recursive calls to DFS over possible assignments
		begin = copy.deepcopy(self)
		rec_backtrack(begin)

		# After exhausting all possible assignments
		if len(solutions) != 0:
			# Choose best solutions based on user's desired optimizations
			return solutions

		return []

	# If user inputs (Boolean) that they want to optimize on low workload,
	# then we sort the domains by low workload before starting the CSP.
	# This will require us to use lists for the domains instead of sets, which
	# changes *a lot* of code. We could try different methods like getting
	# courses frmo the domain and testing what their semester workload is and
	# only branch out on the lowest semesters
	def order_domain_values(self):

		# Depending on heuristics, order vals by lowest workload, LCV, etc.
		return self.get_lcv()
		# pass

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object has n classes
	# def solve_with_FC(self):
	# 	def rec_backtrack_with_FC(assignment):
	# 		self.attempts += 1

	# 		print "Attempt: {}".format(self.attempts)
	# 		for o in range(1, 9):
	# 			self.state[o].print_courses()


	# 		# print "inside rec call"
	# 		if self.is_complete(assignment) #, self.heuristics)#forward = True):
	# 			self.num_solutions += 1
	# 			solutions.append(assignment)

	# 		else:
	# 			semesters = self.get_unassigned_var(self.state)
	# 			if semesters:
	# 				for semester in semesters:
	# 					all_vals = self.state[semester].available.union(self.state[semester].assigned)

	# 					for value in all_vals:
	# 						if value in self.state[semester].available:
	# 							temp_assigned = tuple(self.state[semester].assigned.union(set([value])))#
	# 							if not self.already_computed(semester, temp_assigned):
	# 								if self.state[semester].add_course_FC(value):
	# 									self.all.add(value)
	# 									for s in range(1, 9):
	# 										if value in self.state[s].available:
	# 											self.state[s].available.remove(value)

	# 									new_version = copy.deepcopy(self.state)
	# 									for q in range(semester, 9): # or semester
	# 										for j in self.disable_future[value]:
	# 											if j in new_version[q].available:
	# 												new_version[q].available.remove(j)
											
	# 									# old version
	# 									# for q in range(semester, 9): # or semester
	# 									# 	for j in disable_future[value]:
	# 									# 		if j in self.state[q].available:
	# 									# 			self.state[q].available.remove(j)
	# 									# new_version = copy.deepcopy(self.state)
										
	# 									# print "Printing current status"
	# 									# for l in range(1,9):
	# 									# 	new_version[l].print_courses()
	# 									result = rec_backtrack_with_FC(new_version)

	# 									# self.state[semester].print_courses()
	# 									# print "Course to remove is {}".format(value)										
	# 									self.state[semester].remove_course(value)
	# 									self.all.remove(value)


	# 									# NEW VERSION: 
	# 									# for n in range(semester, 9):
	# 									# 	for prev_disabled in disable_future[value]:
	# 									# 		if n % 2 == 1:
	# 									# 			if prev_disabled in fall:
	# 									# 				self.state[n].available.add(prev_disabled)
	# 									# 		else:
	# 									# 			if prev_disabled in spring:
	# 									# 				self.state[n].available.add(prev_disabled)


	# 									# See notes in non-FC add_course method
	# 									for n in range(1, 9):
	# 										if n % 2 == 1:
	# 											if value in fall:
	# 												self.state[n].available.add(value)
	# 										else:
	# 											if value in spring:
	# 												self.state[n].available.add(value)

	# 				return False

	# 	self.seen_plans = set()
	# 	self.num_solutions = 0
	# 	self.attempts = 0
	# 	solutions = []

	# 	# Begin recursive calls to DFS over possible assignments
	# 	current_state = copy.deepcopy(self.state)
	# 	rec_backtrack_with_FC(current_state)

	# 	# After exhausting all possible assignments
	# 	if len(solutions) != 0:
	# 		# Choose best solutions based on user's desired optimizations
	# 		return solutions

	# 	return []

variables = (fall, spring)
constraints = courses_to_prereqs, disable_future
classes_per_semester = 2
q_score = 3.0
workload = 25.0
assignments = 2.0
history = [('CS 50', 1)] #, ('Stat 110', 3)]

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, heuristics=True)

print "\nHistory: {}".format(history)
print "Fall: {}".format(fall)
print "Spring: {}".format(spring)
t0 = time.time()
study_cards = csp.solve()
t1 = time.time()
print "\nNo heuristics:\nTotal runtime = {}\nSolutions: {}\nAttempts: {}".format(t1 - t0, len(study_cards), csp.attempts)
t2 = time.time()
study_cards_with_H = csp.solve(heuristics=True)
t3 = time.time()
print "\nWith heuristics:\nTotal runtime = {}\nSolutions: {}\nAttempts: {}".format(t3 - t2, len(study_cards_with_H), csp.attempts)

def compare_plans(plan_a, plan_b):
	# print "\n**********"
	for s in range(1, 9):	
		if plan_a[s].assigned != plan_b[s].assigned:
			# print "Not equivalent! Compare schedules."
			# print "FC:"
			# for j in range(1,9):
			# 	plan_a[j].print_courses()

			# print "BT:"
			# for k in range(1,9):
			# # print "FC:" 
			# # plan_a[s].print_courses()
			# # print "BT:" 
			# 	plan_b[k].print_courses()
			return False
	# print "Equivalent"
	# print "FC:"
	# for j in range(1,9):
	# 	plan_a[j].print_courses()

	# print "BT:"
	# for k in range(1,9):
	# 	plan_b[k].print_courses()

	return True

overlaps = []
different = []
for j in study_cards_with_H:
	shared = False
	for i in study_cards:
		shared = compare_plans(j, i)
		if shared:
			overlaps.append(j)
			break
	if not shared:
		different.append(j)
		print "Non-heuristic version never found:"
		for k in range(1,9):
			j[k].print_courses()

# for count, d in enumerate(different):
# 	print "\nUnfound Solution {}:".format(count + 1)
# 	for m in range(1,9):
# 		d[m].print_courses()

if not study_cards_with_H:
	print "No solutions found. Try higher workload or lower q-score avg?"
# else:
# 	print "*** Printing random solutions for user ***"
# 	k = len(study_cards) # Number of options to show user
# 	random.shuffle(study_cards)
# 	solutions = random.sample(study_cards, k)

# 	for sol, plan in enumerate(solutions):
# 		print "\nSolution {}:".format(sol + 1)
# 		for j in plan:
# 			plan[j].print_courses()

for num, sol in enumerate(study_cards):
	print "Non-heuristic solution {}:".format(num)
	for r in range(1, 9):
		sol[r].print_courses()
		
print "Solutions w/o FC/MRV: {}".format(len(study_cards))
print "Solutions w/  FC/MRV: {}".format(len(study_cards_with_H))
# print "Overlaps should be: {}".format(len(study_cards))
print "Total overlap is: {}".format(len(overlaps))
# print "Difference should be: {}".format(len(study_cards_with_H) - len(study_cards))
print "Difference is: {}".format(len(different))

print "*********"


#print csp.seen_plans
#print "Total seen plans: {}".format(len(csp.seen_plans))

# PLOTS
# Plot number of courses in domain against total solutions found
# Plot number of courses in domain against time for FC vs. non FC
# Plot number of courses in domain against time for MRV, LCV, and neither
# Plot number of courses in domain against time for backtracking vs. local vs. AC
# plt.plot([1,2,3,4], [1,4,9,16], 'ro')
# plt.axis([0, 6, 0, 20])
# plt.show()

