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


import load
fall, spring, courses_to_q = load.storeQdata('courses.csv')
courses_to_prereqs = load.storePrereqs('prerequisites.csv')

# dictionary mapping courses to the classes they enable later
# prereqs_to_courses = {} 

strict = 'strict'
recommended = 'recommended'
one_of = 'one of'
all_of = 'all of'

# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

from copy import deepcopy

class Semester(object):
	def __init__(self, domain, semester, specified):
		self.semester = semester
		self.max_courses, self.min_q, self.max_w, self.min_a = specified
		self.course_count = 0
		self.course_qs = []
		self.avg_q = 0.
		self.w = 0.
		self.course_as = []
		self.avg_a = 0.
		self.assigned = set()
		self.available = set(domain)
		# self.unavailable = set()

	def add_course(course):
		# if self.course_count == max_courses:
		# 	print "Tried to take too many courses in one semester"
		# 	return
		reqs = courses_to_prereqs[course]
		if self.course_count < self.max_courses:

			# is consistent with
			if reqs[strict][one_of] - prev_courses != reqs[strict][one_of] and
			   reqs[strict][all_of] - prev_courses == set() and
			   reqs[recommended][one_of] - prev_courses != reqs[recommended][one_of] and
			   reqs[recommended][all_of] - prev_courses == set():

				self.assigned.add(course)
				self.course_count += 1
				# self.available.remove(course)
				print "Added {} to semester {}".format(course, self.semester)
				return True
		return False
		# self.course_count += 1
		# self.course_qs.append(courses_to_q[course][q])
		# self.avg_q = float(sum(self.course_qs)) / self.course_count
		# self.w += courses_to_q[course][w]

		# # We could modify this to care about min assignment quality, not avgs
		# self.course_as.append(courses_to_q[course][a])
		# self.avg_q = float(sum(self.course_as)) / self.course_count

		# Check constraints on a given semester
		# if self.check():
			

			# # Remove courses from available or unassigned
			# self.assigned.add(course)
			# self.available.remove(course)
			# return True

		# else:
		# 	print "Cannot assign {} to semester {} because it is not available".format(course, self.semester)
		# 	return False

	def remove_course(course):
		self.assigned.remove(course)
		self.available.add(course)
		return None


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
		self.specified = (num_classes, q_score, workload, assignments)
		self.all = set()

		# A plan of study for 8 semesters
		# Each semester has max n concentration courses
		# In each semester, we store sets of assigned, available, and unavailable
		start = {1: Semester(fall, 1, (2, q_score, workload, assignments)), 
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
			if start_state[semester].add_course(course):

				# Still have future semester to fulfil prereqs for
				if semester < 8:

					# Remove from unassigned domains in future semesters anything that
					# we have fulfilled the prereq for
					if course in prereqs_to_courses:
						for class_enabled in prereqs_to_courses[course]:
							for i in range(semester, 9):
								start[semester].open_course(class_enabled)

			else:
				print "Could not add {} to semester {}".format(course, semester)

		self.state = start

	# Check if all concentration requirements (e.g. theory, breadth, depth) fulfilled
	# Check if all prerequisites satisfied before taking a given class
	# Check if average q score and assingment quality per semester meet criteria
	# Check if workload in each semester does not exceed max allowed
	def is_complete(assignment):
		basic_1 = set(['Math 1a'; 'Math 1b'; 'CS 20'; 'Math 21b'])
		basic_2 = set(['Math 1a'; 'Math 1b'; 'CS 20'; 'AM 21b'])
		multivar = set(['AM 21a'; 'Math 21a'; 'Math 23b'; 'Math 25b'; 'Math 55b'])
		linalg = set(['AM 21b'; 'Math 21b'; 'Math 23a'; 'Math 25a'; 'Math 55a'])
		software_1 = set(['CS 50'; 'CS 51'])
		software_2 = set(['CS 51'; 'CS 61'])
		software_3 = set(['CS 50'; 'CS 61'])
		theory_1 = set(['CS 124'; 'CS 126'; 'CS 127'; 'AM 106'; 'AM 107'])
		technical_1 = set(['CS 1'; 'CS 2'; 'CS 20'; 'CS 50'; 'CS 51'; 'CS 61'; 'CS 90na'; 'CS 90NAR'; 
		               'CS 90NBR'; 'CS 91R'; 'CS 96'; 'CS 105'; 'CS 108'; 'CS 109A'; 'CS 109B'; 'CS 121'; 
		               'CS 124'; 'CS 125'; 'CS 126'; 'CS 127'; 'CS 134'; 'CS 136'; 'CS 141'; 'CS 143'; 'CS 144R'; 
		               'CS 146'; 'CS 148'; 'CS 152'; 'CS 153'; 'CS 161'; 'CS 164'; 'CS 165'; 'CS 171'; 'CS 175'; 
		               'CS 179'; 'CS 181'; 'CS 182'; 'CS 187'; 'CS 189'; 'CS 191'; 'Stat 110'; 'Math 154'; 'AM 106';
		               'AM 107'; 'AM 120'; 'AM 121'])
		breadth_1 = set(['CS 134'; 'CS 136'; 'CS 141'; 'CS 143'; 'CS 144R'; 
		               'CS 146'; 'CS 148'; 'CS 152'; 'CS 153'; 'CS 161'; 'CS 164'; 'CS 165'; 'CS 171'; 'CS 175'; 
		               'CS 179'; 'CS 181'; 'CS 182'; 'CS 187'; 'CS 189'])

		math = not (basic_1 - self.all) or not (basic_2 - self.all) or 
				   (multivar - self.all != multivar and linalg - self.all != linalg)

		software = software_1 - self.all == set() or software_2 - self.all == set() or software_3 - self.all == set()
		all_3 = {'CS 50'; 'CS 51'; 'CS 61'} - self.all == set()

		theory = 'CS 121' in self.all and theory_1 - self.all != theory_1

		technical = (len((technical_1 + {'ES 50'}) & self.all) >= 4 or len((technical_1 + {'ES 52'}) & self.all) >= 4) and

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

		course_qs = []
		workloads = []
		course_as = []

		for semester in range(1,9):
			course_count = self.state[semester].course_count
			for course in self.state[semester].assigned:
				course_qs.append(courses_to_q[course][q])
				workloads.append(courses_to_q[course][w])
				course_as.append(courses_to_q[course][a])

			avg_q = float(sum(course_qs)) / course_count
			avg_work = float(sum(workloads)) / course_count
			avg_a = float(sum(course_as)) / course_count
			if avg_q < self.min_q or avg_work > self.max_w or avg_a < self.min_a:
				return False

		return math and software and theory and technical and breadth

	# Use Min Constraining Value and Least Values Remaining heuristics
	def get_unassigned_var(state):
		for semester in range(1, 9):
			if self.state[semester].course_count != self.state[semester].max_courses:
				return semester
		return None

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object has n classes
	def solve():
		def rec_backtrack(assignment):
			if self.is_complete(assignment):
				# solutions.append(assignment)
				return assignment
			else:
				semester = self.get_unassigned_var(self.state)
				prev_courses = set()
				for i in range(1, semester + 1):
					for j in self.state[i].assigned:
						prev_courses.add(j)
				for value in self.state[semester].available:
					if self.state[semester].add_course(value):
						self.all.add(value)
						for s in range(1, 9):
							if value in self.state[s].available:
								self.state[s].available.remove(value)
						new_version = copy.deepcopy(self.state)
						result = rec_backtrack(new_version)
						if result:
							solutions.append(result)
							return result
						self.state[semester].assigned.remove_course(value)
						self.all.remove(value)
						for n in range(1, 9):
							self.state[s].available.add(value)
				return False

			solutions = []

			# Begin recursive calls to DFS over possible assignments
			current_state = copy.deepcopy(self.state)
			rec_backtrack(current_state)

			# After exhausting all possibile assignments
			if len(solutions) != 0:
				# Choose best solutions based on users' optimizations
				return solutions

			return "No satisfying assignment found. Try a lower Q or higher workload?"

variables = (fall, spring)
constraints = (courses_to_prereqs, prereqs_to_courses)
classes_per_semester = 3
q_score = 3.0
workload = 30.0
assignments = 3.0
history = [('CS 50', 1), ('CS 51', 2), ('CS 20', 2), ('CS 121', 3)]

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history)

solutions = csp.solve()
for solution in solutions:
	print solution

