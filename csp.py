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
fall, spring, courses_to_q = load.storeQdata('courses_medium.csv')
courses_to_prereqs, disable_future = load.storePrereqs('prereqs_medium.csv')

# Small test domain
# fall, spring, courses_to_q = load.storeQdata('courses_small.csv')
# courses_to_prereqs, disable_future = load.storePrereqs('prereqs_small.csv')

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
		self.tech_non_breadth = 0
		self.technical = 0

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

		# if self.non_breadth


		avg_q = float(sum([courses_to_q[course][q] for course in self.assigned])) / self.course_count
		work = float(sum([courses_to_q[course][w] for course in self.assigned]))
		avg_a = float(sum([courses_to_q[course][a] for course in self.assigned])) / self.course_count

		# self.assigned.remove(potential_course)
		# self.course_count -= 1

		if avg_q < self.min_q or work > self.max_w or avg_a < self.min_a:
			self.assigned.remove(potential_course)
			self.course_count -= 1
			# print "Couldn't add {} to semester {}".format(potential_course, self.semester)
			return False
		# print "Adding {} to semester {}".format(potential_course, self.semester)

		return True

	def add_course(self, assignment, course, heuristics):
		if self.course_count < self.max_courses and \
		   self.csp.check_prereqs(assignment, course, self.semester):

			# reqs = self.prereqs[course]
			# prev_courses = self.csp.get_previous(self.semester)
			# if self.check_prereqs(course):
			
			# theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
			# theory_fulfilled = 'CS 121' in assignment.all and \
			#                    len(theory_reqs & assignment.all) >= 1

			# # If already fulfilled theory, then theory_reqs count for technical,
			# # but don't take more than 2 non-breadth technicals
			# # If already taken courses for theory, then "course" isn't a duplicate
			# if course in theory_reqs and theory_fulfilled: 
			# 	if self.technical_count == 2 or self.technical:
			# 		return False
			# 	self.technical_count += 1

			if heuristics:
				return self.forward_check(course)

			# and self.forward_check(course):
			# 	if self.csp.verify_technicals(assignment, self.semester, course):
			# 		self.assigned.add(course)
			# 		self.course_count += 1	
			# 		return True				

			# if self.csp.verify_technicals(assignment, self.semester, course):
			self.assigned.add(course)
			self.course_count += 1
			return True	




			# if heuristics and self.forward_check(course):
			# 	if self.csp.verify_technicals(assignment, self.semester, course):
			# 		self.assigned.add(course)
			# 		self.course_count += 1	
			# 		return True				

			# if self.csp.verify_technicals(assignment, self.semester, course):
			# 	self.assigned.add(course)
			# 	self.course_count += 1

			# 	return True				

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
	def __init__(self, variables, constraints, num_classes, q_score, workload, assignments, history=[], must_take=[]):
		self.fall, self.spring = variables
		self.prereqs_to_courses, self.disable_future = constraints
		self.n = num_classes
		self.history = history
		self.must_take = must_take
		self.min_q = q_score
		self.max_w = workload
		self.min_a = assignments
		specified = (num_classes, q_score, workload, assignments, constraints[0], self)
		self.all = set()
		self.num_solutions = 0
		self.attempts = 0
		self.seen_plans = set()
		self.latest_sem = 0
		self.state = None
		self.theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
		self.non_breadth_courses = set(['CS 96', 'CS 105', 'CS 108', 'CS 109A', 'CS 109B', \
		    'Stat 110', 'Math 154', 'AM 106', 'AM 107', 'AM 120', 'AM 121', 'ES 153'])
		self.breadth_courses = set(['CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 144R', \
		    'CS 146', 'CS 148', 'CS 152', 'CS 153', 'CS 161', 'CS 165', 'CS 171', 'CS 175', \
		    'CS 179', 'CS 181', 'CS 182', 'CS 189', 'ES 153']) 
		# self.technical_courses = set(['CS 51', 'CS 61', 'CS 96', 'CS 105', 'CS 108', \
		# 	'CS 109A', 'CS 109B', 'CS 124', 'CS 126', 'CS 127', 'CS 134', 'CS 136', \
		# 	'CS 141', 'CS 143', 'CS 144R', 'CS 148', 'CS 152', 'CS 161', 'CS 165', \
		# 	'CS 171', 'CS 175', 'CS 179', 'CS 181', 'CS 182', 'CS 189', 'CS 191', \
		# 	'Stat 110', 'Math 154', 'AM 106', 'AM 107', 'AM 120', 'AM 121', 'ES 153'])
		# self.technical_count = 0
		# self.non_breadth_count = 0
		# self.non_breadth_flag = False
		# self.technical_flag = False

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
		for course, semester in self.history:
			self.latest_sem = max(semester, self.latest_sem)
			start[semester].assigned.add(course)
			self.all.add(course)
			start[semester].course_count += 1
			for s in range(1, 9):
				if course in start[s].available:
					start[s].available.remove(course)
			for j in range(semester, 9):
				for disabled in self.disable_future[course]:
					if n % 2 == 1:
						if disabled in fall:
							start[semester].available.remove(disabled)
					else:
						if disabled in spring:
							start[semester].available.remove(disabled)

		for course, semester in self.must_take:
			if course in spring and course not in fall and semester % 2 == 1:	
				print "\nSorry! {} is not offered in the fall.".format(course)
				return None
			elif course in fall and course not in spring and semester % 2 != 1:
				print "\nSorry! {} is not offered in the spring.".format(course)
				return None
			elif courses_to_q[course][q] > self.max_w:
				print "\nSorry! {} exceeds your max workload of {}.".format(course, self.max_w)
				return None
			start[semester].assigned.add(course)
			self.all.add(course)
			start[semester].course_count += 1
			for s in range(1, 9):
				if course in start[s].available:
					start[s].available.remove(course)
			for j in range(semester, 9):
				for disabled in self.disable_future[course]:
					if j % 2 == 1:
						if disabled in fall:
							start[j].available.remove(disabled)
					else:
						if disabled in spring:
							start[j].available.remove(disabled)	
		print "Starting out:"
		for i in range(1, 9):
			print "Semester {} available: {}".format(i, start[i].available)							

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

		print "Printing potential solution"
		for k in range(1,9):
			assignment.state[k].print_courses()

		# If assignment doesn't meet minimum number of courses, fail-check early
		if len(assignment.all) < 10: 
			print "Too short"
			return False

		if self.must_take != []:
			for course, semester in self.must_take:
				prev_taken = assignment.get_previous(assignment.state, semester)
				if not assignment.check_prereqs(assignment, course, semester, prev_taken):
					return False
				# reqs = self.prereqs_to_courses[course]
			# make sure that courses before must take semester have necessary prereqs

		courses_taken = copy.deepcopy(assignment.all)
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

		math = not (basic_1 - courses_taken) or not (basic_2 - courses_taken) or \
				   (len(multivar & courses_taken) > 0 and len(linalg & courses_taken) > 0)

		if not math: return False

		software = software_1 - courses_taken == set() or software_2 - courses_taken == set() or software_3 - courses_taken == set()
		all_3 = {'CS 50', 'CS 51', 'CS 61'} - courses_taken == set()

		if not software: return False

		theory_courses = theory_1 & courses_taken
		theory = 'CS 121' in courses_taken and len(theory_courses) > 0

		if not theory: return False

		if theory_courses != set():
			theory_course = random.choice(list(theory_courses))
			technical_1 -= set([theory_course])

		# self.theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
		# self.non_breadth_courses = set(['CS 96', 'CS 105', 'CS 108', 'CS 109A', 'CS 109B', \
		#     'Stat 110', 'Math 154', 'AM 106', 'AM 107', 'AM 120', 'AM 121', 'ES 153'])

		# technical_temp = technical_1 - breadth_1
		# technical_a = len(technical_temp.union(set(['ES 50']))) & courses_taken <= 2
		# if not technical_a: return False
		technical_a = not ('ES 50' in courses_taken and 'ES 52' in courses_taken)
		if not technical_a: return False
		technical_b = False

		if all_3:
			# print "\nAll: {}".format(courses_taken)
			technical = (len((technical_1.union(set(['ES 50']))) & courses_taken) == 5 or len((technical_1.union(set(['ES 52']))) & courses_taken) == 5)
			# print "technical_1a: {}".format(technical_1.union({'ES 50'}))
			# print "technical_1b: {}".format(technical_1.union({'ES 52'}))
			# print "Technical: {}".format(technical)
		else:
			if software_2 - courses_taken == set():
				technical_1 -= set(['CS 51', 'CS 61'])
			elif software_1 - courses_taken == set():
				technical_1 -= set(['CS 51'])
			elif software_3 - courses_taken == set():
				technical_1 -= set(['CS 61'])

			if 'ES 50' in courses_taken:
				technical_b = len((technical_1.union(set(['ES 50']))) & courses_taken) == 4 
			elif 'ES 52' in courses_taken:
				technical_b = len((technical_1.union(set(['ES 52']))) & courses_taken) == 4
			else:
				technical_b = len(technical_1 & courses_taken) == 4
		# if all_3 or (software_1 - assignment.all == set()) or (software_3 - assignment.all == set()):
		# 	technical = (len((technical_1.union({'ES 50'})) & assignment.all) == 5 or len((technical_1.union({'ES 52'})) & assignment.all) == 5)
		
		# elif software_2 - assignment.all == set():
		# 	technical = (len((technical_1.union({'ES 50'})) & assignment.all) == 6 or len((technical_1.union({'ES 52'})) & assignment.all) == 6)

		if not technical_b: return False
		technical = technical_a and technical_b

		# Handle special cases where student takes all of CS 50/51/61 or ES 153
		counter = 0
		subject = ''
		if all_3:
			counter += 1
		if 'ES 153' in courses_taken:
			courses_taken.remove('ES 153')
			counter += 1
			subject = '4'
		
		# if self.honors: 6 technical, 4 breadth
		for c in courses_taken:
			# Non honors requires 2 breadth courses of different subjects
			if counter < 2:
				if c in breadth_1 and c[4] != subject:
					counter += 1
					subject = c[4]

		breadth = (counter == 2)

		if not breadth: return False

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

		# If everything else satisfied, make sure we aren't taking too many classes
		# We attempted to forward-check this, but things got messy with recursion and
		# adding and removing from available domains at different semesters
		return math and software and theory and technical and breadth
		# if math and software and theory and technical and breadth:
		# 	all_courses = copy.deepcopy(assignment.all)
		# 	non_breadth_count = 0
		# 	technical_count = 0

		# 	if all_3:
		# 		technical_count += 1

		# 	non_breadth_count += len(theory_courses) - 1

		# 	if non_breadth_count > 2:
		# 		return False

		# 	all_courses -= theory_courses.union('CS 121')

		# 	if 'CS 124' in theory_courses:
		# 		theory_courses.remove('CS 124')
		# 	elif 'CS 126' 
		# 	all_courses -= theory_courses



		# 	software_reqs = set(['CS 51', 'CS 61'])
		# 	# theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
		# 	theory_fulfilled = 'CS 121' in assignment.all and len(self.theory_reqs & assignment.all) >= 1 # or assignment.all

		# 	# If already fulfilled theory, then theory_reqs count for technical,
		# 	# but don't take more than 2 non-breadth technicals or 4 technicals overall
		# 	# If already taken courses for theory, then "course" isn't a duplicate
		# 	for value in assignment.all:

		# 	if (course in self.theory_reqs and theory_fulfilled) or course in assignment.non_breadth_courses:
		# 		# Still room for technical requirements			
		# 		if technical_count < 4 and non_breadth_count < 2:
		# 			# self.non_breadth_flag = True
		# 			non_breadth_count += 1
		# 			technical_count += 1
		# 			if non_breadth_count == 2:
		# 				# get rid of those classes without using disable_future
		# 				for i in range(semester, 9):
		# 					assignment.state[i].available -= self.theory_reqs
		# 				# new = assignment.disable_future[course].union(theory_reqs.union(assignment.non_breadth_courses))
		# 				# assignment.disable_future[course] = new
		# 			if technical_count == 4:
		# 				for i in range(semester, 9):
		# 					assignment.state[i].available -= (self.theory_reqs.union(self.breadth_courses))
		# 				# assignment.disable_future[course] = assignment.disable_future[course].union(assignment.breadth_courses)
		# 		else:
		# 			return False 
		# 	elif course in assignment.breadth_courses or \
		# 		course in software_reqs and (software_reqs.union({'CS 50'}) - assignment.all.union({course}) == set()):
		# 		if assignment.technical_count < 4:
		# 			# self.technical_flag = True
		# 			assignment.technical_count += 1
		# 			if assignment.technical_count == 4:
		# 				for i in range(semester, 9):
		# 					assignment.state[i].available -= (self.theory_reqs.union(self.breadth_courses))
		# 				# assignment.disable_future[course] = assignment.disable_future[course].union(assignment.breadth_courses)
		# 		else:
		# 			return False
		# 	return True

	# def verify_must_take(self):
	# 	self.state



	# Look at all previous semesters when determining prereq satisfaction; no simultaneity allowed
	def get_previous(self, current_state, semester, tuple_version = False):
		if tuple_version:
			final = []
			for i in range(1, semester):
				final.append(tuple(current_state[i].assigned))
			return final

		else:
			prev_courses = set()
			# print "Semester is {}".format(semester)
			for i in range(1, semester):
				prev_courses = prev_courses.union(current_state[i].assigned)
			return prev_courses	

	# Checks if we have already computed this combination given all previous semesters
	def already_computed(self, current_state, semester, current_semester_courses):
		current_plan = self.get_previous(current_state, semester, tuple_version=True)
		# print current_plan
		current_plan.append(current_semester_courses)
		current_plan = tuple(current_plan)
		if current_plan not in self.seen_plans:
			self.seen_plans.add(current_plan)
			return False
		return True

	# After removing a course via backtracking, add back courses that were disabled by this class
	# def settle_disabled(self, assignment, semester, course):

	# 	potential_add_backs = assignment.disable_future[course]

	# 	software_reqs = set(['CS 51', 'CS 61'])
	# 	theory_fulfilled = 'CS 121' in assignment.all and len(self.theory_reqs & assignment.all) >= 1 # or assignment.all
		
	# 	if (course in self.theory_reqs and theory_fulfilled) or course in assignment.non_breadth_courses:
	# 		assignment.non_breadth_count -= 1
	# 		assignment.technical_count -= 1
	# 		potential_add_backs = potential_add_backs.union(self.theory_reqs)

	# 	elif course in assignment.breadth_courses or \
	# 		(course in software_reqs and (software_reqs.union({'CS 50'}) - assignment.all.union({course}) == set())):
	# 		assignment.technical_count -= 1
	# 		potential_add_backs = potential_add_backs.union(self.breadth_courses)
		
	# 	# if assignment.non_breadth_flag:
	# 	# 	assignment.non_breadth_count -= 1
	# 	# 	assignment.technical_count -= 1
	# 	# 	potential_add_backs = potential_add_backs.union(self.theory_reqs)
	# 	# 	assignment.non_breadth_flag = False
	# 	# elif assignment.technical_flag:
	# 	# 	assignment.technical_count -= 1
	# 	# 	potential_add_backs = potential_add_backs.union(self.breadth_courses)
	# 	# 	assignment.technical_flag = False

	# 	still_disabled = set()
	# 	prev_courses = assignment.get_previous(assignment.state, semester)
	# 	prev_courses = prev_courses.union(assignment.state[semester].assigned)

	# 	for prev in prev_courses:
	# 		still_disabled = still_disabled.union(assignment.disable_future[prev])

	# 	for n in range(semester, 9):
	# 		for add_back in potential_add_backs:
	# 			if add_back not in still_disabled:
	# 				if n % 2 == 1:
	# 					if add_back in fall:
	# 						assignment.state[n].available.add(add_back)
	# 				else:
	# 					if add_back in spring:
	# 						assignment.state[n].available.add(add_back)

	# def verify_technicals(self, assignment, semester, course):
	# 	software_reqs = set(['CS 51', 'CS 61'])
	# 	# theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
	# 	theory_fulfilled = 'CS 121' in assignment.all and len(self.theory_reqs & assignment.all) >= 1 # or assignment.all

	# 	# If already fulfilled theory, then theory_reqs count for technical,
	# 	# but don't take more than 2 non-breadth technicals or 4 technicals overall
	# 	# If already taken courses for theory, then "course" isn't a duplicate
	# 	if (course in self.theory_reqs and theory_fulfilled) or course in assignment.non_breadth_courses:
	# 		# Still room for technical requirements			
	# 		if assignment.technical_count < 4 and assignment.non_breadth_count < 2:
	# 			# self.non_breadth_flag = True
	# 			assignment.non_breadth_count += 1
	# 			assignment.technical_count += 1
	# 			if assignment.non_breadth_count == 2:
	# 				# get rid of those classes without using disable_future
	# 				for i in range(semester, 9):
	# 					assignment.state[i].available -= self.theory_reqs
	# 				# new = assignment.disable_future[course].union(theory_reqs.union(assignment.non_breadth_courses))
	# 				# assignment.disable_future[course] = new
	# 			if assignment.technical_count == 4:
	# 				for i in range(semester, 9):
	# 					assignment.state[i].available -= (self.theory_reqs.union(self.breadth_courses))
	# 				# assignment.disable_future[course] = assignment.disable_future[course].union(assignment.breadth_courses)
	# 		else:
	# 			return False 
	# 	elif course in assignment.breadth_courses or \
	# 		course in software_reqs and (software_reqs.union({'CS 50'}) - assignment.all.union({course}) == set()):
	# 		if assignment.technical_count < 4:
	# 			# self.technical_flag = True
	# 			assignment.technical_count += 1
	# 			if assignment.technical_count == 4:
	# 				for i in range(semester, 9):
	# 					assignment.state[i].available -= (self.theory_reqs.union(self.breadth_courses))
	# 				# assignment.disable_future[course] = assignment.disable_future[course].union(assignment.breadth_courses)
	# 		else:
	# 			return False
	# 	return True

	def check_prereqs(self, assignment, course, semester, before_must={}):
		# print "Checking prereqs for {} in semester {}".format(course, semester)

		if before_must != {}:
			prev_courses = before_must
		else:
			prev_courses = assignment.get_previous(assignment.state, semester)

		reqs = assignment.prereqs_to_courses[course]
		if len(reqs[strict][one_of]) == 0 and len(reqs[strict][all_of]) == 0 and \
		   len(reqs[recommended][one_of]) == 0 and len(reqs[recommended][all_of]) == 0:
		   	# print "Yes\n"
		   	return True
		   	# return assignment.verify_technicals(assignment, course)

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
			# return assignment.verify_technicals(assignment, course)
		# print "No\n"
		return False

	# Return the variable with the minimum positive # of remaining values
	def get_mrv(self, assignment):
		# print "\n\n\n\nFinding variables with MRV"
		minimum = float('inf')
		lowest = []

		for i in range(self.latest_sem + 1, 9):
			if assignment.state[i].course_count != assignment.state[i].max_courses:
				valids = set()
				for course in assignment.state[i].available:
					if self.check_prereqs(assignment, course, i):
						valids.add(course)
					
				size = len(valids)
				if assignment.state[i].course_count < assignment.state[i].max_courses:
					if 0 < size < minimum:
						minimum = size
						lowest = [i]

		return lowest

	# Return the least constraining value (course) to be assigned of available
	# This should be called from order_domain_values
	# The purpose is to choose a value from the available set that doesn't
	# constrain other semesters' possibilities
	def get_lcv(self, values):
		# print "values: {}".format(values)
		# answer = self.insertion_sort(values)
		# print answer
		# print "LCV ordering: {}".format(answer)
		return self.insertion_sort(values)
		# def insert_course(value, disabled_count):
		# 	for i in range(len(courses)):
		# 		if disabled_count <= len(self.disable_future[courses[i]]):
		# 			courses.insert(i, value)
		# 			break
		# [key for key, _ in sorted(mapping.iteritems(), key=lambda (k,v): (v,k)):
		#     print "%s: %s" % (key, value)
		# courses = []
		# for course in values:
		# 	disabled_count = len(self.disable_future[course])
		# 	insert_course(course, disabled_count)

		# return courses

		# LCV

	def insertion_sort(self, values):
		def insert_course(value, disabled_count):
			for i in range(len(courses)):
				# print "Disabled count is {} and disabled count for other courses is {}".format(disabled_count, len(self.disable_future[courses[i]]))
				if disabled_count <= len(self.disable_future[courses[i]]):
					courses.insert(i, value)
					# print "inserted! courses: {}".format(courses)
					break
			else:
				courses.append(value)

		start = random.choice(list(values))
		courses = [start]
		values.remove(start)
		for course in values:
			disabled_count = len(self.disable_future[course])
			insert_course(course, disabled_count)

		return courses	

		# def insertion_sort(vals):

		#    for position in range(len(list(values))):

		#      current_value = vals[position]
		#      while position > 0 and vals[position - 1] > currentvalue:
		#          vals[position] = vals[position - 1]
		#          position = position - 1

		#      vals[position] = currentvalue

		# courses = list(values)	

	# If user inputs (Boolean) that they want to optimize on low workload,
	# then we sort the domains by low workload before starting the CSP.
	# This will require us to use lists for the domains instead of sets, which
	# changes *a lot* of code. We could try different methods like getting
	# courses frmo the domain and testing what their semester workload is and
	# only branch out on the lowest semesters
	def order_domain_values(self, values):
		# Depending on heuristics, order vals by lowest workload, LCV, etc.
		# if self.heuristics:
		# 	# print "About to call get_lcv"
		# 	return self.get_lcv(values)
		
		# Identity function		
		return values

	# Use Min Remaining Value and Least Constraining Value heuristics
	# Return multiple semesters from which to branch out: check
	# Stop assigning courses when assignment is complete:
	def get_unassigned_var(self, assignment):

		# MRV
		# if self.heuristics:
		# 	return self.get_mrv(assignment)

		# Choose semesters in order
		for semester in range(self.latest_sem + 1, 9):
			if assignment.state[semester].course_count != assignment.state[semester].max_courses:
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

	# Enforce arc-consistency with AC-3 and propagate constraints
	def AC3(csp, queue=None):
	    if queue == None:
	        queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neighbors[Xi]]
	    while queue:
	        (Xi, Xj) = queue.pop()
	        if remove_inconsistent_values(csp, Xi, Xj):
	            for Xk in csp.neighbors[Xi]:
	                queue.append((Xk, Xi))

	def remove_inconsistent_values(csp, Xi, Xj):
	    "Return true if we remove a value."
	    removed = False
	    for x in csp.curr_domains[Xi][:]:
	        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
	        if every(lambda y: not csp.constraints(Xi, x, Xj, y),
	                csp.curr_domains[Xj]):
	            csp.curr_domains[Xi].remove(x)
	            removed = True
	    return removed

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
				return True
			else:
				# Gets next semesters needing additional courses
				semesters = self.get_unassigned_var(assignment)
				# print "Unassigned semesters are {}".format(semesters)
				if semesters:
					for semester in semesters:
						# Wrapper to avoid key error
						# all_vals = assignment.state[semester].available.union(assignment.state[semester].assigned)
						all_vals = copy.deepcopy(assignment.state[semester].available)

						# count_all_vals = len(all_vals)
						# Iterates through every candidate class
						# temp = assignment.state[semester].assigned

						tries = 0
						count_available = len(assignment.state[semester].available)
						for value in self.order_domain_values(all_vals):
							# Class is available to be assigned
							if value in assignment.state[semester].available:
								tries += 1
								temp_assigned = tuple(assignment.state[semester].assigned.union(set([value])))
								# Checks for duplicate semesters
								if not self.already_computed(assignment.state, semester, temp_assigned):
									if assignment.state[semester].add_course(assignment, value, heuristics):
										assignment.all.add(value)

										# Removes this class from all future semesters
										# if self.technical == 4 or self.non_breadth == 2:
										# 	for s in range(semester, 9):
										# 		if value in assignment.state[s].available:
										# 			assignment.state[s].available.remove(value)
										# 		assignment.state[s].available
										# else:
										for s in range(1, 9):
											if value in assignment.state[s].available:
												assignment.state[s].available.remove(value)
											# remove non_breadth courses if reached 2 or if technical is 4



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
										# if result:
										# 	return

										# print "All: {}".format(self.all)
										# self.state[semester].print_courses()
										# print "Course to remove is {}".format(value)
										assignment.state[semester].remove_course(value)

										# Added this conditional to fix key error
										# if value in self.all:
										assignment.all.remove(value)

										# assignment.settle_disabled(assignment, semester, value)
										# Free up the course for other semesters since we removed it
										for n in range(1, 9):
											if n % 2 == 1:
												if value in fall:
													assignment.state[n].available.add(value)
											else:
												if value in spring:
													assignment.state[n].available.add(value)
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
										# 				assignment.state[n].available.add(prev_disabled)
										# 		else:
										# 			if prev_disabled in spring:
										# 				assignment.state[n].available.add(prev_disabled)
						
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

		if self.state == None:
			return []
		
		print "\nHistory: {}".format(self.history)
		print "Must take: {}".format(self.must_take)
		print "Fall: {}".format(self.fall)
		print "Spring: {}".format(self.spring)
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
workload = 35.0
assignments = 2.0
history = [] # [('CS 50', 1)] #[('CS 61', 1)] #[('CS 50', 1)] #, ('Stat 110', 3)]
must_take = [('CS 161', 8)]
optimizations = 'workload'

csp = CSP_Solver(variables, constraints, classes_per_semester, q_score, workload, assignments, history, must_take)

# t0 = time.time()
# study_cards = csp.solve()
# t1 = time.time()
# print "\nNo heuristics:\nTotal runtime = {}\nSolutions: {}\nAttempts: {}".format(t1 - t0, len(study_cards), csp.attempts)
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

# overlaps = []
# different = []
# for j in study_cards_with_H:
# 	shared = False
# 	for i in study_cards:
# 		shared = compare_plans(j, i)
# 		if shared:
# 			overlaps.append(j)
# 			break
# 	if not shared:
# 		different.append(j)
# 		print "Non-heuristic version never found:"
# 		for k in range(1,9):
# 			j[k].print_courses()

# for count, d in enumerate(different):
# 	print "\nUnfound Solution {}:".format(count + 1)
# 	for m in range(1,9):
# 		d[m].print_courses()

# Number of random solutions to generate
k = 10
# if not study_cards:
# 	print "No solutions found w/o heuristics. Try higher workload or lower q-score avg?"
# else:
# 	print "*** Printing random solutions for user w/o heuristics ***"
# 	random.shuffle(study_cards)
# 	solutions = random.sample(study_cards, k)

for sol, plan in enumerate(study_cards_with_H):
	print "\nSolution {}:".format(sol + 1)
	for j in plan:
		plan[j].print_courses()

if not study_cards_with_H:
	print "No solutions found w/ heuristics. Try higher workload or lower q-score avg?"
else:
	print "*** Printing random solutions for user w/ heuristics ***"
	random.shuffle(study_cards_with_H)
	solutions_H = random.sample(study_cards_with_H, k)

	for sol, plan in enumerate(solutions_H):
		print "\nSolution {}:".format(sol + 1)
		for j in plan:
			plan[j].print_courses()

# for num, sol in enumerate(study_cards):
# 	print "Non-heuristic solution {}:".format(num)
# 	for r in range(1, 9):
# 		sol[r].print_courses()
		
# print "Solutions w/o FC/MRV: {}".format(len(study_cards))
print "Solutions w/  FC/MRV: {}".format(len(study_cards_with_H))
# print "Overlaps should be: {}".format(len(study_cards))
# print "Total overlap is: {}".format(len(overlaps))
# print "Difference should be: {}".format(len(study_cards_with_H) - len(study_cards))
# print "Difference is: {}".format(len(different))

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

