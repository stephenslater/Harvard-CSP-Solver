# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater

# Read CSV file in python, generate fall courses, spring courses, and q-guide data
# Instead of manually inputting these
# Example
# courses_to_q = {
	# 'CS 50': {'q': 3.6, 'w': 12.6, 'a': 3.6, 't': 'Introduction to Computer Science I'}

	# }
# Typed all of these, but will generate them from reading CSV instead

import random
import load
fall, spring, courses_to_q = load.storeQdata('courses.csv')
# fall.remove('Math 23a')
courses_to_prereqs, disable_future = load.storePrereqs('prerequisites.csv')
# print disable_future

# dictionary mapping courses to the classes they enable later
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

import copy

class Semester(object):
	def __init__(self, domain, semester, specified):
		self.semester = semester
		self.max_courses, self.min_q, self.max_w, self.min_a, self.prereqs, self.csp = specified
		self.course_count = 0
		self.course_qs = []
		self.avg_q = 0.
		self.w = 0.
		self.course_as = []
		self.avg_a = 0.
		self.assigned = set()
		self.available = set(domain)
		# self.unavailable = set()

	def add_course(self, course):
		# if self.course_count == max_courses:
		# 	print "Tried to take too many courses in one semester"
		# 	return
		# print "TRYING TO ADD COURSE: {} to semester {}".format(course, self.semester)

		reqs = self.prereqs[course]
		# print "{} reqs: {}\n".format(course, reqs)
		if self.course_count < self.max_courses:
			# print "room in the semester"
			prev_courses = set()
			for i in range(1, self.semester):
				assigned_courses = self.csp.state[i].assigned
				# print "Assigned courses for semester {}: {}".format(i, assigned_courses)
				for j in assigned_courses:
					prev_courses.add(j)

			if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
			   len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
				self.assigned.add(course)
				self.course_count += 1
				# self.available.remove(course)
				# print "Added {} to semester {}".format(course, self.semester)
				# print "SCHOOL IS IN SESSION"
				return True
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

				# is consistent with
				# print "now checking prereqs"
				# print "reqs: {}, prev_courses: {}".format(reqs, prev_courses)
				# print "************************"
				# print "overlap: {}".format(reqs[recommended][one_of] & prev_courses)
				if ((len(reqs[strict][one_of]) == 0) or (len(reqs[strict][one_of] & prev_courses) > 0)) and \
				   reqs[strict][all_of] - prev_courses == set() and \
				   ((len(reqs[recommended][one_of]) == 0) or (len(reqs[recommended][one_of] & prev_courses) > 0)) and \
				   recommended_all:

					self.assigned.add(course)
					self.course_count += 1
					# self.available.remove(course)
					# print "Added {} to semester {}".format(course, self.semester)
					# print "SCHOOL IS IN SESSION"
					return True
		return False

		# Check constraints on a given semester
		# if self.check():
			

			# # Remove courses from available or unassigned
			# self.assigned.add(course)
			# self.available.remove(course)
			# return True

		# else:
		# 	print "Cannot assign {} to semester {} because it is not available".format(course, self.semester)
		# 	return False

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

	# def check():
	# 	# if self.avg_q < self.min_q:
	# 	# 	print "Assignment does not meet minimum q-score avg of {} in semester {}".format(self.min_q, self.semester)
	# 	# 	return False
	# 	# if self.w > self.max_w:
	# 	# 	print "Assignment exceeds maximum workload of {} in semester {}".format(self.max_q, self.semester)
	# 	# 	return False
	# 	# if self.avg_a < self.min_a:
	# 	# 	print "Assignment does not meet minimum assignment quality avg of {} in semester {}".format(self.min_a, self.semester)
	# 	# 	return False

	# 	# Check constraints

	# 	return True


	# Move courses that are unavailable out of the available set


#
# SUGGESTION: Define Semester class as a class within CSP_Solver so that
# we can avoid repetition like "Semester(__, __, specified)" and just access
# data from CSP_Solver directly.
# See: https://stackoverflow.com/questions/1765677/nested-classes-scope
#
class CSP_Solver(object):
	# type history: [(string, int)] e.g. [('CS 50', 1), ('CS 51', 2)]
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

		# A plan of study for 8 semesters
		# Each semester has max n concentration courses
		# In each semester, we store sets of assigned, available, and unavailable
		start = {1: Semester(fall, 1, (2, q_score, workload, assignments, constraints[0], self)), 
				 2: Semester(spring, 2, specified),
				 3: Semester(fall, 3, specified), 
				 4: Semester(spring, 4, specified),
				 5: Semester(fall, 5, specified), 
				 6: Semester(spring, 6, specified),
				 7: Semester(fall, 7, specified), 
				 8: Semester(spring, 8, specified) 
			}

		# Populate state with classes user has already taken
		for course, semester in history:
			start[semester].assigned.add(course)
			self.all.add(course)
			start[semester].course_count += 1
			for s in range(1, 9):
				if course in start[s].available:
					start[s].available.remove(course)


			# if start_state[semester].add_course(course):

			# 	# Still have future semester to fulfil prereqs for
			# 	if semester < 8:

			# 		# Remove from unassigned domains in future semesters anything that
			# 		# we have fulfilled the prereq for
			# 		if course in prereqs_to_courses:
			# 			for class_enabled in prereqs_to_courses[course]:
			# 				for i in range(semester, 9):
			# 					start[semester].open_course(class_enabled)

			# else:
			# 	print "Could not add {} to semester {}".format(course, semester)

		self.state = start

	# Check if all concentration requirements (e.g. theory, breadth, depth) fulfilled
	# Check if all prerequisites satisfied before taking a given class
	# Check if average q score and assingment quality per semester meet criteria
	# Check if workload in each semester does not exceed max allowed
	def is_complete(self, assignment):
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
		# print "self.all is {}".format(self.all)
		# print "all_3 is {}".format(all_3)

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

		# for s in range(1,9):
		# 	assignment[s].print_courses()
		# print "math: {}, software: {}, theory: {}, technical: {}, breadth: {}".format(math, software, theory, technical, breadth)
		
		for semester in range(1,9):
			course_count = self.state[semester].course_count
			course_qs = []
			workloads = []
			course_as = []
			for course in self.state[semester].assigned:
				course_qs.append(courses_to_q[course][q])
				workloads.append(courses_to_q[course][w])
				course_as.append(courses_to_q[course][a])

			if course_count > 0:
				avg_q = float(sum(course_qs)) / course_count
				avg_work = float(sum(workloads)) / course_count
				avg_a = float(sum(course_as)) / course_count
				if avg_q < self.min_q or avg_work > self.max_w or avg_a < self.min_a:
					# print "avg_q: {}, min_q: {}, avg_work: {}, max_w: {}, avg_a: {}, min_a: {}".format(avg_q, self.min_q, avg_work, self.max_w, avg_a, self.min_a)
					return False

		# print "math: {}, software: {}, theory: {}, technical: {}, breadth: {}".format(math, software, theory, technical, breadth)
		return math and software and theory and technical and breadth

	# Use Min Constraining Value and Least Values Remaining heuristics
	def get_unassigned_var(self, state):
		for semester in range(1, 9):
			if self.state[semester].course_count != self.state[semester].max_courses:
				# print semester
				return semester
		return None

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object has n classes
	def solve(self):
		def rec_backtrack(assignment):
			# print "inside rec call"
			if self.is_complete(assignment):
				# print "New complete assignment:\n"
				# for s in range(1,9):
				# 	assignment[s].print_courses()
				# self.num_solutions += 1
				if self.num_solutions > 500000:
					print "just reached 500k solutions"
				elif self.num_solutions > 250000:
					print "just reached 250k solutions" 
				elif self.num_solutions > 100000:
					print "just reached 100k solutions"
				elif self.num_solutions > 50000:
					print "just reached 50k solutions"

				# print "$$$$$$$$$$$$$$"
				# print self.num_solutions
				solutions.append(assignment)
				# print "COMPLETE ASSIGNMENT!"
				# return assignment
			else:
				semester = self.get_unassigned_var(self.state)
				if semester:
					# self.state[semester].print_courses()
					# prev_courses = set()
					# for i in range(1, semester + 1):
					# 	for j in self.state[i].assigned:
					# 		prev_courses.add(j)
					all_vals = self.state[semester].available.union(self.state[semester].assigned)

					for value in all_vals:
						# print "found available classes: {}".format(self.state[semester].available)

						if value in self.state[semester].available:
							# print "Trying to add {} to semester {}".format(value, semester)
							if self.state[semester].add_course(value):
								# print "added a course successfully: {} to semester {}".format(value, semester)

								self.all.add(value)
								for s in range(1, 9):
									if value in self.state[s].available:
										self.state[s].available.remove(value)
								for q in range(semester + 1, 9):
									for j in disable_future[value]:
										if j in self.state[q].available:
											self.state[q].available.remove(j)
								new_version = copy.deepcopy(self.state)
								# print "\nCurrent status: ".format(new_version)
								# self.state[semester].print_courses()
								# print "\n"
								result = rec_backtrack(new_version)
								# if result:
								# 	# solutions.append(result)
								# 	return result
								self.state[semester].remove_course(value)
								self.all.remove(value)
								for n in range(1, 9):
									self.state[n].available.add(value)
								# self.state[semester].available.remove(value)
					return False
				# print "Filled up study card"

		solutions = []

		# Begin recursive calls to DFS over possible assignments
		current_state = copy.deepcopy(self.state)
		# print "Starting recursive calls"
		rec_backtrack(current_state)

		# After exhausting all possible assignments
		if len(solutions) != 0:
			# Choose best solutions based on users' optimizations
			print "SOLUTIONS COUNT: {}".format(len(solutions))
			return solutions

		# for i in range(1, 9):
		# 	self.state[i].print_courses()
		# print "No satisfying assignment found. Try a lower Q or higher workload?"
		return []

variables = (fall, spring)
constraints = courses_to_prereqs, disable_future
classes_per_semester = 3
q_score = 2.0
workload = 50.0
assignments = 2.0
history = [('CS 50', 1), ('AM 21a', 1), ('CS 51', 2), ('CS 20', 2), ('Math 21b', 2), ('CS 121', 3)]

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history)

study_cards = csp.solve()
# print "*********"
# for study_card in study_cards:
# 	print "\nPrinting new solution:"
# 	for j in study_card:
# 		study_card[j].print_courses()

