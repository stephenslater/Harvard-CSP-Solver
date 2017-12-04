# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater

import random
import load
import time
import copy

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
		if self.course_count > 0:
			avg_q = float(sum([courses_to_q[course][q] for course in self.assigned])) / self.course_count
			work = float(sum([courses_to_q[course][w] for course in self.assigned]))
			avg_a = float(sum([courses_to_q[course][a] for course in self.assigned])) / self.course_count

			if avg_q < self.min_q or work > self.max_w or avg_a < self.min_a:
				self.assigned.remove(potential_course)
				self.course_count -= 1
				return False
		return True

	def add_course(self, course):
		reqs = self.prereqs[course]
		if self.course_count < self.max_courses:
			prev_courses = self.csp.get_previous(self.semester)

			# No forward checking in this version. If there aren't prereqs, add it
			if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
			   len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
				self.assigned.add(course)
				self.course_count += 1
				return True

			# If there are prereqs, we need to fulfill them and account for different math series
			else:
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
					self.assigned.add(course)
					self.course_count += 1
					return True
		return False

	def add_course_FC(self, course):
		reqs = self.prereqs[course]
		if self.course_count < self.max_courses:
			prev_courses = self.csp.get_previous(self.semester)

			# TODO: combine this if-else block
			# There are no prereqs, so make sure that adding it is okay
			if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
			   len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
				return self.forward_check(course)

			# If there are prereqs, we need to fulfill them and account for different math series
			else:
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
				    return self.forward_check(course)
		return False

	def remove_course(self, course):
		self.assigned.remove(course)
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
	def __init__(self, variables, constraints, num_classes, q_score, workload, assignments, history):
		self.fall, self.spring = variables
		self.constraints = constraints
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
		latest_sem = 0
		for course, semester in history:
			if semester > latest_sem:
				latest_sem = semester
			start[semester].assigned.add(course)
			self.all.add(course)
			start[semester].course_count += 1
			for s in range(1, 9):
				if course in start[s].available:
					start[s].available.remove(course)

		# print "Latest sem is {}".format(latest_sem)
		for sem in range(latest_sem):
			start[sem+1].max_courses = 0

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
	def is_complete(self, assignment, forward=False):

		# If we've already seen this assignment at this semester given previous semester
		# Then don't count it as a new solution in this function
		# If we haven't seen it, then add it to some solutions seen set
		# We can handle this by just adding every assignment to a visited set
		# And never try again if we've already seen a combination of (A, B, C)
		# Regardless of whether (A, B, C) is a solution
		# I.e. if we've seen it before, return false on is_complete, and somehow we 
		# don't want to do more recursive calls for anything after, since we will have 
		# done them already

		# print "Printing potential solution"
		# for k in range(1,9):
		# 	assignment[k].print_courses()

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
		               'CS 179', 'CS 181', 'CS 182', 'CS 189', 'ES 153']) # ES 153 counts for 140s

		math = not (basic_1 - self.all) or not (basic_2 - self.all) or \
				   (len(multivar & self.all) > 0 and len(linalg & self.all) > 0)

		software = software_1 - self.all == set() or software_2 - self.all == set() or software_3 - self.all == set()
		all_3 = {'CS 50', 'CS 51', 'CS 61'} - self.all == set()

		theory = 'CS 121' in self.all and len(theory_1 & self.all) > 0

		technical = (len((technical_1.union({'ES 50'})) & self.all) >= 4 or len((technical_1.union({'ES 52'})) & self.all) >= 4)

		counter = 0
		subject = ''
		if all_3:
			counter += 1
		
		for c in self.all:
			# Non honors requires 2 breadth courses of different subjects
			if counter < 2:
				if c in breadth_1 and c[4] != subject:
					counter += 1
					subject = c[4]

		breadth = (counter == 2)

		# Don't check this here if we are using forward checking
		if not forward:
			#print "Not using forward checking"
			for semester in range(1,9):
				course_count = self.state[semester].course_count

				course_qs = [courses_to_q[course][q] for course in self.state[semester].assigned]
				workloads = [courses_to_q[course][w] for course in self.state[semester].assigned]
				course_as = [courses_to_q[course][a] for course in self.state[semester].assigned]

				if course_count > 0:
					avg_q = float(sum(course_qs)) / course_count
					work = float(sum(workloads))
					avg_a = float(sum(course_as)) / course_count
					if avg_q < self.min_q or work > self.max_w or avg_a < self.min_a:
						return False

		# Add the semester combo as an already-recorded solution before returning
		return math and software and theory and technical and breadth

	# Look at all previous semesters when determining prereq satisfaction; no simultaneity allowed
	def get_previous(self, semester, tuple_version = False):
		if tuple_version:
			final = tuple()
			for i in range(1, semester):
				final += tuple(self.state[i].assigned,)
			return final

		else:
			prev_courses = set()
			for i in range(1, semester):
				prev_courses = prev_courses.union(self.state[i].assigned)
			return prev_courses	

	# Checks if we have already computed this combination given all previous semester
	# Another way to do this would be to store the current_plan thru prev semesters
	# instead of computing it every time, but would have to deal with resetting it
	def already_computed(self, semester, current_semester):
		current_plan = self.get_previous(semester, tuple_version=True)
		current_plan += (current_semester,)
		if current_plan not in self.seen_plans:
			self.seen_plans.add(current_plan)
			return False
		return True

	# Use Min Constraining Value and Least Values Remaining heuristics
	# Return multiple semesters from which to branch out
	def get_unassigned_var(self, state):
		for semester in range(1, 9):
			if self.state[semester].course_count < self.state[semester].max_courses:
				if semester < 8:
					if self.state[semester+1].course_count < self.state[semester+1].max_courses:
						if semester != 7:
							if self.state[semester+2].course_count < self.state[semester+2].max_courses:
								return [semester, semester + 1, semester + 2]
						else:
							return [semester, semester + 1]				
				return [semester]
		return None

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object can take n courses
	def solve(self):
		def rec_backtrack(assignment):
			# Number of function calls, used to compare algorithms
			self.attempts += 1
			if self.is_complete(assignment):
				self.num_solutions += 1
				solutions.append(assignment)
			else:
				semesters = self.get_unassigned_var(self.state)
				#print "Unassigned semesters are {}".format(semesters)
				if semesters:
					for semester in semesters:
						all_vals = self.state[semester].available.union(self.state[semester].assigned)

						for value in all_vals:
							if value in self.state[semester].available:
								temp_assigned = tuple(self.state[semester].assigned.union(value))
								if not self.already_computed(semester, temp_assigned):
									if self.state[semester].add_course(value):
										self.all.add(value)
										for s in range(1, 9):
											if value in self.state[s].available:
												self.state[s].available.remove(value)

										# Don't want to allow for taking courses simultaneously?
										# I.e. if Math 21a disabled AM 21a in the future,
										# We want to disable AM21a from right now as well
										# So we can maybe change this to be in range(semester, 9)
										# Remove disabled courses from future semesters
										for q in range(semester + 1, 9):
											for j in disable_future[value]:
												if j in self.state[q].available:
													self.state[q].available.remove(j)

										new_version = copy.deepcopy(self.state)
										result = rec_backtrack(new_version)

										self.state[semester].remove_course(value)
										self.all.remove(value)

										# Add the course back for future options
										# Only add it back to its valid semester(s),
										# since some courses are offered fall and spring
										# In addition to adding back "value", we should
										# add back courses that we had disabled by taking value

										# I think this should be range(semester, 9) instead?
										for n in range(1, 9):
											if n % 2 == 1:
												if value in fall:
													self.state[n].available.add(value)
											else:
												if value in spring:
													self.state[n].available.add(value)

					return False

		self.seen_plans = set()
		self.num_solutions = 0
		self.attempts = 0
		solutions = []

		# Begin recursive calls to DFS over possible assignments
		current_state = copy.deepcopy(self.state)
		rec_backtrack(current_state)

		# After exhausting all possible assignments
		if len(solutions) != 0:
			# Choose best solutions based on user's desired optimizations
			return solutions

		return []

	def order_domain_values():
		pass

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object has n classes
	def solve_with_FC(self):
		def rec_backtrack_with_FC(assignment):
			self.attempts += 1
			# print "inside rec call"
			if self.is_complete(assignment, forward = True):
				self.num_solutions += 1
				solutions.append(assignment)

			else:
				semesters = self.get_unassigned_var(self.state)
				if semesters:
					for semester in semesters:
						all_vals = self.state[semester].available.union(self.state[semester].assigned)

						for value in all_vals:
							if value in self.state[semester].available:
								temp_assigned = tuple(self.state[semester].assigned.union(value))
								if not self.already_computed(semester, temp_assigned):
									if self.state[semester].add_course_FC(value):
										self.all.add(value)
										for s in range(1, 9):
											if value in self.state[s].available:
												self.state[s].available.remove(value)
										for q in range(semester + 1, 9):
											for j in disable_future[value]:
												if j in self.state[q].available:
													self.state[q].available.remove(j)
										new_version = copy.deepcopy(self.state)
										# print "Printing current status"
										# for l in range(1,9):
										# 	new_version[l].print_courses()
										result = rec_backtrack_with_FC(new_version)
										self.state[semester].remove_course(value)
										self.all.remove(value)

										# See notes in non-FC add_course method
										for n in range(1, 9):
											if n % 2 == 1:
												if value in fall:
													self.state[n].available.add(value)
											else:
												if value in spring:
													self.state[n].available.add(value)

					return False

		self.seen_plans = set()
		self.num_solutions = 0
		self.attempts = 0
		solutions = []

		# Begin recursive calls to DFS over possible assignments
		current_state = copy.deepcopy(self.state)
		rec_backtrack_with_FC(current_state)

		# After exhausting all possible assignments
		if len(solutions) != 0:
			# Choose best solutions based on user's desired optimizations
			return solutions

		return []

variables = (fall, spring)
constraints = courses_to_prereqs, disable_future
classes_per_semester = 2
q_score = 3.0
workload = 25.0
assignments = 2.0
history = [('CS 51', 2), ('CS 20', 2)]

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history)

print "\nHistory: {}".format(history)
print "Fall: {}".format(fall)
print "Spring: {}".format(spring)
t0 = time.time()
study_cards = csp.solve()
t1 = time.time()
print "\nNo forward checking:\nTotal runtime = {}\nSolutions: {}\nAttempts: {}".format(t1 - t0, len(study_cards), csp.attempts)
t2 = time.time()
study_cards_with_FC = csp.solve_with_FC()
t3 = time.time()
print "\nWith forward checking:\nTotal runtime = {}\nSolutions: {}\nAttempts: {}".format(t3 - t2, len(study_cards_with_FC), csp.attempts)

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

# overlaps = []
# different = []
# for j in study_cards_with_FC:
# 	shared = False
# 	for i in study_cards:
# 		shared = compare_plans(j, i)
# 		if shared:
# 			overlaps.append(j)
# 			break
# 	if not shared:
# 		different.append(j)
# 		print "Non FC never found:"
# 		for k in range(1,9):
# 			j[k].print_courses()

# for count, d in enumerate(different):
# 	print "\nUnfound Solution {}:".format(count + 1)
# 	for m in range(1,9):
# 		d[m].print_courses()

print "Solutions w/o FC: {}".format(len(study_cards))
print "Solutions w/  FC: {}".format(len(study_cards_with_FC))
# print "Overlaps should be: {}".format(len(study_cards))
# print "Total overlap is: {}".format(len(overlaps))
# print "Difference should be: {}".format(len(study_cards_with_FC) - len(study_cards))
# print "Difference is: {}".format(len(different))

print "*********"
for sol, plan in enumerate(study_cards_with_FC):
	print "\nSolution {}:".format(sol + 1)
	for j in plan:
		plan[j].print_courses()

