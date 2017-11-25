# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater

# Read CSV file in python, generate fall courses, spring courses, and q-guide data
# Instead of manually inputting these
# Example
courses_to_q = {
	'CS 50': {'q': 3.6, 'w': 12.6, 'a': 3.6, 't': 'Introduction to Computer Science I'}

	}
# Typed all of these, but will generate them from reading CSV instead
fall = set(['CS 50', 'CS 61', 'CS 105', 'CS 108', 'CS 109A', 'CS 121', \
			'CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 171' 'CS 175', \
			'CS 182', ])
spring = set(['CS 1', 'CS 20', 'CS 51', 'CS 109B', 'CS 124', 'CS 152', \
			  'CS 161', 'CS 165', 'CS 179', 'CS 181', 'CS 189', 'CS 191'])


# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

# dictionary mapping courses to the prereqs required for them
courses_to_prereqs = {} 

# dictionary mapping courses to the classes they enable later
prereqs_to_courses = {} 

from copy import deepcopy

class Semester(object):
	def __init__(self, domain, max_courses, semester, specified):
		self.semester = semester
		self.max_courses, self.min_q, self.max_w, self.min_a = specified
		self.course_count = 0
		self.course_qs = []
		self.avg_q = 0
		self.w = 0
		self.course_as = []
		self.avg_a = 0
		self.assigned = set()
		self.available = set(domain)
		self.unavailable = set()

	def add_course(course):
		# if self.course_count == max_courses:
		# 	print "Tried to take too many courses in one semester"
		# 	return
		if course in self.available:
			self.assigned.add(course)
			self.course_count += 1
			self.course_qs.append(courses_to_q[course][q])
			self.avg_q = float(sum(self.course_qs)) / self.course_count
			self.w += courses_to_q[course][w]

			# We could modify this to care about min assignment quality, not avgs
			self.course_as.append(courses_to_q[course][a])
			self.avg_q = float(sum(self.course_as)) / self.course_count

			# Check constraints on a given semester
			if self.check():
				print "Added {} to semester {}".format(course, self.semester)

				# Remove courses from available or unassigned
				self.assigned.add(course)
				self.available.remove(course)
				return True
		else:
			print "Cannot assign {} to semester {} because it is not available".format(course, self.semester)
			return False

	def open_course(course):
		if course in self.unavailable:
			self.unavailable.remove(course)
			self.available.add(course)

	def check():
		if self.avg_q < self.min_q:
			print "Assignment does not meet minimum q-score avg of {} in semester {}".format(self.min_q, self.semester)
			return False
		if self.w > self.max_w:
			print "Assignment exceeds maximum workload of {} in semester {}".format(self.max_q, self.semester)
			return False
		if self.avg_a < self.min_a:
			print "Assignment does not meet minimum assignment quality avg of {} in semester {}".format(self.min_a, self.semester)
			return False

		# Check constraints

		return True


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

		# A plan of study for 8 semesters
		# Each semester has max n concentration courses
		# In each semester, we store sets of assigned, available, and unavailable
		start = {1: Semester(fall, 1, specified), 
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

	# Use Min Constraining Value and Least Values Remaining heuristics
	def get_unassigned_var(semester):
		pass

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object has n classes
	def solve():
		def rec_backtrack(assignment):
			if is_complete(assignment):
				solutions.append(assignment)
			else:
				var = get_unassigned_var(variables)
			


			# Complete pseudocode from lecture slide for basic backtracking algorithm





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
history = [('CS 50', 1), ('CS 51', 2), ('CS 20', 2)]

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history)

solutions = csp.solve()
for solution in solutions:
	print solution

