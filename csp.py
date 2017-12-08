# CS 182 Final Project, Fall 2017
# CS-P: CS Concentration Solver
# Menaka Narayanan and Stephen Slater

import random
import load
import time
import copy
import matplotlib.pyplot as plt

# Full course domain
fall, spring, courses_to_q = load.storeQdata('courses.csv')
courses_to_prereqs, disable_future = load.storePrereqs('prerequisites.csv')

# Medium test domain
# fall, spring, courses_to_q = load.storeQdata('courses_medium.csv')
# courses_to_prereqs, disable_future = load.storePrereqs('prereqs_medium.csv')

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

class Semester(object):
	def __init__(self, domain, semester, specified):
		self.semester = semester
		self.max_courses, self.min_q, self.max_w, self.min_a, self.prereqs, self.csp = specified
		self.course_count = 0
		self.assigned = set()
		self.available = set(domain)
		self.tech_non_breadth = 0
		self.technical = 0

	# When trying to add course, make sure it doesn't violate q-scores, etc.
	def forward_check(self, potential_course):
		self.assigned.add(potential_course)
		self.course_count += 1

		avg_q = float(sum([courses_to_q[course]['q'] for course in self.assigned])) / self.course_count
		work = float(sum([courses_to_q[course]['w'] for course in self.assigned]))
		avg_a = float(sum([courses_to_q[course]['a'] for course in self.assigned])) / self.course_count

		if avg_q < self.min_q or work > self.max_w or avg_a < self.min_a:
			self.assigned.remove(potential_course)
			self.course_count -= 1
			return False

		return True

	def neighbors(self):
		return [k for k in range(1,9) if k != self.semester]

	def add_course(self, assignment, course, heuristics=None):
		# print "\nTrying to add {} to semester {}".format(course, self.semester)
		if self.course_count < self.max_courses and \
		   self.csp.check_prereqs(assignment, course, self.semester):
		   	math_reqs = set(['Math 1a', 'Math 1b', 'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b', \
		   		'Math 23a', 'Math 23b', 'Math 25a', 'Math 25b', 'Math 55a', 'Math 55b'])
			theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
			non_breadth_courses = set(['CS 96', 'CS 105', 'CS 108', 'CS 109A', 'CS 109B', \
			    'Stat 110', 'Math 154', 'AM 120', 'AM 121', 'CS 191'])
			breadth_courses = set(['CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 144R', \
			    'CS 146', 'CS 148', 'CS 152', 'CS 153', 'CS 161', 'CS 165', 'CS 171', 'CS 175', \
			    'CS 179', 'CS 181', 'CS 182', 'CS 189', 'ES 153']) 

			courses_taken_a = copy.deepcopy(assignment.all)
			courses_taken_b = copy.deepcopy(assignment.all)

			theory_taken = theory_reqs & courses_taken_a
			theory_fulfilled = 'CS 121' in courses_taken_a and len(theory_taken) >= 1

			if theory_fulfilled:
				to_remove = random.choice(list(theory_taken))
				courses_taken_a -= set([to_remove])
				courses_taken_b -= set([to_remove])

			if 'ES 50' in courses_taken_a:
				non_breadth_courses = non_breadth_courses.union({'ES 50'})
			elif 'ES 52' in courses_taken_a:
				non_breadth_courses = non_breadth_courses.union({'ES 52'})	

			### ADDING NEW CODE
			non_breadth = len(courses_taken_a & non_breadth_courses.union(theory_reqs))
			# Find out how many penultimate digits we've taken
			# If we've seen a breadth penultimate digit more than twice, do not add

			if course is not 'CS 121' and course not in math_reqs:

				if not theory_fulfilled and course in theory_reqs:
					# continue as normal with adding

					# Pasting in code from below
					if heuristics:
						if heuristics['fc'] and heuristics['ac']:
							# Prune values in self.semester's domain that aren't consistent
							assignment.ac3(assignment, [(Xk, self.semester) for Xk in self.neighbors()])
							return self.forward_check(course)

						# If only doing FC, then ensure course can be added
						elif heuristics['fc']:
							return self.forward_check(course)

						# If only doing AC, then prune from domain in this assignment
						# any values that are inconsistent with other semesters
						elif heuristics['ac']:
							assignment.ac3(assignment, [(Xk, self.semester) for Xk in self.neighbors()])		

					# if self.csp.verify_technicals(assignment, self.semester, course):
					self.assigned.add(course)
					self.course_count += 1
					return True	


				# We don't want to take more than 2 non-breadth non-theory-counting courses
				if non_breadth >= 2 and course in non_breadth_courses:
					# print "Too many non-breadth"
					return False

				# Handle special cases where student takes all of CS 50/51/61 or ES 153
				# We start with the count of our non-breadth technical courses
				counter_a = non_breadth
				counter_b = non_breadth
				breadth_count_a = 0
				breadth_count_b = 0
				subjects_a = set()
				subjects_b = set()
				if 'ES 153' in courses_taken_a:
					courses_taken_a.remove('ES 153')
					courses_taken_b.remove('ES 153')
					counter_a += 1
					counter_b += 1
					breadth_count_a += 1
					breadth_count_b += 1
					subjects_a.add('4')
					subjects_b.add('4')

				# One of 51/61 counts for breadth if taken 50/51/61
				all_3 = (({'CS 50', 'CS 51', 'CS 61'} - assignment.all) == set())
				taken = False
				if all_3:
					counter_a += 1
					counter_b += 1
					courses_taken_a.remove('CS 51')
					courses_taken_b.remove('CS 61')
					breadth_count_a += 1
					breadth_count_b += 1
					subjects_a.add('5')
					subjects_b.add('6')
					# Future implementation: if self.honors: 6 technical, 4 breadth
					# Check if fulfilled breadth given many ways to do so (51 vs. 61)
					for c in courses_taken_a:
						# Non honors requires 2 breadth courses of different subjects
						# if counter < 2:
						if c in breadth_courses:
							breadth_count_a += 1
							if c[4] not in subjects_a:
								counter_a += 1
								subjects_a.add(c[4])
							else:
								taken = True

					for d in courses_taken_b:
						if d in breadth_courses:
							breadth_count_b += 1
							if d[4] not in subjects_b:
								counter_b += 1
								subjects_b.add(d[4])
							else:
								taken = True

					if (counter_a - non_breadth < 2 and course in breadth_courses and course[4] in subjects_a) or \
					(counter_b - non_breadth < 2 and course in breadth_courses and course[4] in subjects_b):
						# print "this case here 2"
						return False

					if counter_a >= 4 or counter_b >= 4: #and not theory_fulfilled: 
						# print "returning False here 1"
						return False

				else:
					for c in courses_taken_a:
						# Non honors requires 2 breadth courses of different subjects
						# if counter < 2:
						if c in breadth_courses:
							breadth_count_a += 1
							if c[4] not in subjects_a:
								counter_a += 1
								subjects_a.add(c[4])

					# if self.csp.heuristics['mrv'] and course in breadth_courses and course[4] in subjects_a:
					# 	return False

					if counter_a - non_breadth < 2 and course in breadth_courses and course[4] in subjects_a:
						# print "this case here 2"
						return False

					# Don't add another breadth course if we already have 4 technical
					if counter_a >= 4 or (len(courses_taken_a.union({'ES 153'}) & breadth_courses) >= 4): #and \
					#theory_fulfilled: 
						return False

			if heuristics:
				if heuristics['fc'] and heuristics['ac']:
					# Prune values in self.semester's domain that aren't consistent
					assignment.ac3(assignment, [(Xk, self.semester) for Xk in self.neighbors()])
					return self.forward_check(course)

				# If only doing FC, then ensure course can be added
				elif heuristics['fc']:
					return self.forward_check(course)

				# If only doing AC, then prune from domain in this assignment
				# any values that are inconsistent with other semesters
				elif heuristics['ac']:
					assignment.ac3(assignment, [(Xk, self.semester) for Xk in self.neighbors()])
					
			# if self.csp.verify_technicals(assignment, self.semester, course):
			self.assigned.add(course)
			self.course_count += 1
			return True	

		return False

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
	def __init__(self, variables, constraints, num_classes, q_score, workload, assignments, history=[], must_take=[], priors=set(), total=100):
		self.fall, self.spring = variables
		self.courses_to_prereqs, self.disable_future = constraints
		self.n = num_classes
		self.history = history
		self.must_take = must_take
		self.min_q = q_score
		self.max_w = workload
		self.min_a = assignments
		specified = (num_classes, q_score, workload, assignments, constraints[0], self)
		self.all = set()
		self.priors = priors
		self.initialized = False
		self.num_solutions = 0
		self.total = total
		self.attempts = 0
		self.seen_plans = set()
		self.latest_sem = 0
		self.state = None
		self.planned_121 = False # A flag denoting whether the user inputted a semester to take 121
		self.theory_reqs = set(['CS 124', 'CS 126', 'CS 127', 'AM 106', 'AM 107'])
		self.non_breadth_courses = set(['CS 96', 'CS 105', 'CS 108', 'CS 109A', 'CS 109B', \
		    'Stat 110', 'Math 154', 'AM 106', 'AM 107', 'AM 120', 'AM 121', 'ES 153'])
		self.breadth_courses = set(['CS 134', 'CS 136', 'CS 141', 'CS 143', 'CS 144R', \
		    'CS 146', 'CS 148', 'CS 152', 'CS 153', 'CS 161', 'CS 165', 'CS 171', 'CS 175', \
		    'CS 179', 'CS 181', 'CS 182', 'CS 189', 'ES 153'])
		maths = {'Math 1a', 'Math 1b', 'Math 23a', 'Math 23b', 'Math 25a', 'Math 25b', 'Math 55a', 'Math 55b'} 
		mid_maths = {'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'}
		adv_maths = {'Math 23a', 'Math 23b', 'Math 25a', 'Math 25b', 'Math 55a', 'Math 55b'}
		self.all_maths = maths.union(mid_maths)


		# print "Pruning the domains based on prior math experience"
		# Student must take Math 23ab or 25ab or 55ab in first year
		print "Priors: {}".format(self.priors)
		if 'adv_math' in self.priors:
			chosen_a = random.choice(['Math 23a', 'Math 25a', 'Math 55a'])
			chosen_b = chosen_a[:-1] + 'b'
			print "chosen_a, chosen_b: {}, {}".format(chosen_a, chosen_b)
			self.fall -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'})
			self.spring -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'})
			self.must_take.extend([(1, chosen_a), (2, chosen_b)])

		# Student may not take regular math courses below or above 21ab
		elif 'prior_math' in self.priors:
			self.fall -= maths
			self.spring -= maths
			for level in mid_maths:
				self.courses_to_prereqs[level] = {strict: {one_of: set(), all_of: set()}, recommended: {one_of: set(), all_of: set()}}

		# Student must take Math 1ab in the first year
		elif not 'prior_math' in self.priors and not 'adv_math' in self.priors:
			self.fall -= adv_maths
			self.spring -= adv_maths
			self.must_take.extend([(1, 'Math 1a'), (2, 'Math 1b')])

		self.state = {1: Semester((self.fall - {'CS 191', 'CS 121'} - self.breadth_courses - self.non_breadth_courses).union({'Stat 110'}), 1, (2, q_score, workload, assignments, constraints[0], self)), 
				 2: Semester((self.spring - {'CS 191'} - self.breadth_courses - self.non_breadth_courses), 2, specified),
				 3: Semester(self.fall - maths - {'CS 191'}, 3, specified), 
				 4: Semester(self.spring - maths - {'CS 191'}, 4, specified),
				 5: Semester(self.fall - maths, 5, specified), 
				 6: Semester(self.spring - maths, 6, specified),
				 7: Semester(self.fall - maths, 7, specified), 
				 8: Semester(self.spring - maths, 8, specified) 
			}

		for semester, course in self.history:
			if semester not in range(1, 9):
				print "\nSorry! Please choose a semester between 1 and 8 for {}.".format(course)
				return None

		for i in range(len(self.must_take)):
			for j in range(i + 1, len(self.must_take)):
				A, a = self.must_take[i][0], self.must_take[i][1]
				B, b = self.must_take[j][0], self.must_take[j][1]
				if self.conflicts(A, a, B, b):
					print "\nSorry! Your history is impossible."
					return None

		for semester, course in self.history:
			self.latest_sem = max(semester, self.latest_sem)
			self.state[semester].assigned.add(course)
			self.all.add(course)
			self.state[semester].course_count += 1
			for s in range(1, 9):
				if course in self.state[s].available:
					self.state[s].available.remove(course)
			for j in range(semester, 9):
				for disabled in self.disable_future[course]:
					if j % 2 == 1:
						if disabled in fall and disabled in self.state[j].available:
							self.state[j].available.remove(disabled)
					else:
						if disabled in spring and disabled in self.state[j].available:
							self.state[j].available.remove(disabled)
		for i in range(1, 9):
			if self.state[i].assigned != set():
				count = len(self.state[i].assigned)
				self.state[i].max_courses = count
				self.state[i].min_q = float(sum([courses_to_q[course]['q'] for course in self.state[i].assigned])) / count
				self.state[i].max_w = float(sum([courses_to_q[course]['w'] for course in self.state[i].assigned]))
				self.state[i].min_a = float(sum([courses_to_q[course]['a'] for course in self.state[i].assigned])) / count

		must_takes = set([title for _, title in self.must_take])
		history_takes = set([title for _, title in self.history])
		if 'CS 121' not in must_takes and 'CS 121' not in history_takes:
			earliest_121 = self.latest_sem + 2
			if self.latest_sem % 2 == 0:
				earliest_121 = max(self.latest_sem + 1, 3)
			sem_121 = random.choice(range(earliest_121,9,2))
			self.must_take.append((sem_121, 'CS 121'))
		else:
			self.planned_121 = True

		if self.fill_must_take() == False:
			return None

		self.initialized = True

	# Check if all concentration requirements (e.g. theory, breadth, depth) fulfilled
	# Check if all prerequisites satisfied before taking a given class
	# If not using forward checking,
		# Check that average q, workload, and average a meet requirements
	def is_complete(self, assignment): 
		print "\nPrinting potential solution"
		for k in range(1,9):
			assignment.state[k].print_courses()

		# If assignment doesn't meet minimum number of courses, fail-check early
		if len(assignment.all) < 10: 
			return False

		if assignment.must_take != []:
			for semester, course in assignment.must_take:
				prev_taken = assignment.get_previous(assignment.state, semester)
				if not assignment.check_prereqs(assignment, course, semester, prev_taken):
					# print "Previous courses don't fulfill reqs for must_take: {}".format(course)
					return False

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

		technical_a = not ('ES 50' in courses_taken and 'ES 52' in courses_taken)
		if not technical_a: return False
		technical_b = False

		if all_3:
			technical_b = (len((technical_1.union(set(['ES 50']))) & courses_taken) >= 5 or \
				len((technical_1.union(set(['ES 52']))) & courses_taken) >= 5)
		else:
			if software_2 - courses_taken == set():
				technical_1 -= set(['CS 51', 'CS 61'])
			elif software_1 - courses_taken == set():
				technical_1 -= set(['CS 51'])
			elif software_3 - courses_taken == set():
				technical_1 -= set(['CS 61'])

			if 'ES 50' in courses_taken:
				technical_b = len((technical_1.union(set(['ES 50']))) & courses_taken) >= 4 
			elif 'ES 52' in courses_taken:
				technical_b = len((technical_1.union(set(['ES 52']))) & courses_taken) >= 4
			else:
				technical_b = len(technical_1 & courses_taken) >= 4

		if not technical_b: return False
		technical = technical_a and technical_b

		# Handle special cases where student takes all of CS 50/51/61 or ES 153
		# We start with the count of our non-breadth technical courses
		courses_taken_a = copy.deepcopy(courses_taken)
		courses_taken_b = copy.deepcopy(courses_taken)
		counter_a = 0
		counter_b = 0
		breadth_count_a = 0
		breadth_count_b = 0
		subjects_a = set()
		subjects_b = set()
		if 'ES 153' in courses_taken_a:
			courses_taken_a.remove('ES 153')
			courses_taken_b.remove('ES 153')
			counter_a += 1
			counter_b += 1
			breadth_count_a += 1
			breadth_count_b += 1
			subjects_a.add('4')
			subjects_b.add('4')

		# One of 51/61 counts for breadth if taken all of 50/51/61
		all_3 = (({'CS 50', 'CS 51', 'CS 61'} - assignment.all) == set())
		taken = False
		if all_3:
			counter_a += 1
			counter_b += 1
			courses_taken_a.remove('CS 51')
			courses_taken_b.remove('CS 61')
			breadth_count_a += 1
			breadth_count_b += 1
			subjects_a.add('5')
			subjects_b.add('6')

			# Check if fulfilled breadth given many ways to do so (51 vs. 61)
			for c in courses_taken_a:
				if c in breadth_1:
					breadth_count_a += 1
					if c[4] not in subjects_a:
						counter_a += 1
						subjects_a.add(c[4])
					else:
						taken = True

			for d in courses_taken_b:
				if d in breadth_1:
					breadth_count_b += 1
					if d[4] not in subjects_b:
						counter_b += 1
						subjects_b.add(d[4])
					else:
						taken = True

			breadth = (counter_a >= 2 or counter_b >= 2)

		else:
			for c in courses_taken_a:
				if c in breadth_1:
					breadth_count_a += 1
					if c[4] not in subjects_a:
						counter_a += 1
						subjects_a.add(c[4])

			breadth = (counter_a >= 2)

		if not breadth: return False

		# Only do this computation if we didn't forward check these constraints
		if not assignment.heuristics['fc']:
			for semester in range(1,9):
				course_count = assignment.state[semester].course_count

				course_qs = [courses_to_q[course]['q'] for course in assignment.state[semester].assigned]
				workloads = [courses_to_q[course]['w'] for course in assignment.state[semester].assigned]
				course_as = [courses_to_q[course]['a'] for course in assignment.state[semester].assigned]

				if course_count > 0:
					avg_q = float(sum(course_qs)) / course_count
					work = float(sum(workloads))
					avg_a = float(sum(course_as)) / course_count
					if avg_q < assignment.min_q or work > assignment.max_w or avg_a < assignment.min_a:
						print "Assignment does not meet q-guide constraints"
						return False

		return math and software and theory and technical and breadth

	# Look at all previous semesters when determining prereq satisfaction; 
	# no simultaneity allowed
	def get_previous(self, current_state, semester, tuple_version = False):
		if semester < 1 or semester > 9:
			print "Cannot return course history outside of state bounds."
			return
		else:
			if tuple_version:
				final = []
				for i in range(1, semester):
					final.append(tuple(current_state[i].assigned))
				return final

			else:
				prev_courses = set()
				for i in range(1, semester):
					prev_courses = prev_courses.union(current_state[i].assigned)
				return prev_courses.union(self.priors)	

	# Checks if we have already computed this combination given all previous semesters
	# Only to be used with non-MRV, since this relies on a variable ordering
	def already_computed(self, current_state, semester, current_semester_courses):
		if self.heuristics['mrv']:
			return False
		current_plan = self.get_previous(current_state, semester, tuple_version=True)

		# Make use of hashable tuples to store previously computed states
		current_semester_courses = tuple(sorted(current_semester_courses))
		current_plan.append(current_semester_courses)
		current_plan = tuple(current_plan)

		if current_plan not in self.seen_plans:
			self.seen_plans.add(current_plan)
			return False
		print "Sorry! We've already computed this plan: {}".format(current_plan)
		return True

	# Fill must_takes at random restarts
	def fill_must_take(self, assignment=None):
		if assignment == None:
			assignment = self

		for semester, course in assignment.must_take:
			if course not in assignment.fall.union(assignment.spring):
				print "\nSorry! {} is not currently offered.".format(course)
				return False
			elif semester not in range(1, 9):
				print "\nSorry! Please choose a semester between 1 and 8 for {}.".format(course)
				return False
			elif course in spring and course not in fall and semester % 2 == 1:	
				print "\nSorry! {} is not offered in the fall.".format(course)
				return False
			elif course in fall and course not in spring and semester % 2 != 1:
				print "\nSorry! {} is not offered in the spring.".format(course)
				return False
			elif courses_to_q[course]['w'] > assignment.max_w:
				print "\nSorry! {} exceeds your max workload of {}.".format(course, assignment.max_w)
				return False
			elif semester <= assignment.latest_sem:
				print "\nSorry! You can't take classes in the past. Your history goes through semester {}".format(assignment.latest_sem)

		for i in range(len(assignment.must_take)):
			for j in range(i + 1, len(assignment.must_take)):
				A, a = assignment.must_take[i][0], assignment.must_take[i][1]
				B, b = assignment.must_take[j][0], assignment.must_take[j][1]
				if assignment.conflicts(A, a, B, b):
					print "\nSorry! Your dreams do not meet scheduling constraints."
					return False

		# Reset any previously-assigned must_take courses, but maintain history
		history_takes = set([title for _, title in assignment.history])
		for i in range(1, 9):
			wrapper = copy.deepcopy(assignment.state[i].assigned)
			for prev_assigned in wrapper:
				if prev_assigned not in history_takes:
					assignment.state[i].assigned.remove(prev_assigned)
					assignment.state[i].course_count -= 1
					assignment.all.remove(prev_assigned)

		for semester, course in assignment.must_take:
			prev_taken = assignment.get_previous(assignment.state, semester)
			if assignment.latest_sem > semester:
				print "Sorry! You can't specify a dream class in the past.".format(course)
				return False

			assignment.state[semester].assigned.add(course)
			assignment.all.add(course)
			assignment.state[semester].course_count += 1
			for s in range(1, 9):
				if course in assignment.state[s].available:
					assignment.state[s].available.remove(course)
			for j in range(semester, 9):
				for disabled in assignment.disable_future[course]:
					if j % 2 == 1:
						if disabled in fall and disabled in assignment.state[j].available:
							assignment.state[j].available.remove(disabled)
					else:
						if disabled in spring and disabled in assignment.state[j].available:
							assignment.state[j].available.remove(disabled)

		assignment.seen_plans = set()

	def choose_must_takes(self, assignment):
		must_takes = set([title for _, title in assignment.must_take])
		assignment.seen_plans = set()

		if not assignment.planned_121 or 'adv_math' in assignment.priors:

			# If we need to choose a random slot for CS 121
			if not assignment.planned_121:
				earliest_121 = assignment.latest_sem + 2
				if assignment.latest_sem % 2 == 0:
					earliest_121 = max(assignment.latest_sem + 1, 3)

				sem_121 = random.choice(range(earliest_121,9,2))

				assignment.must_take = [(i, title) for (i, title) in assignment.must_take if title != 'CS 121']
				assignment.must_take.append((sem_121, 'CS 121'))
				for i in range(1, 9):
					if 'CS 121' in assignment.state[i].available:
						assignment.state[i].available.remove('CS 121')

			# If we need to choose random advanced math courses for semesters 1/2
			if 'adv_math' in assignment.priors:
				adv_maths_f = set(['Math 23a', 'Math 25a', 'Math 55a'])
				adv_maths_s = set(['Math 23b', 'Math 25b', 'Math 55b'])
				must_takes = set([title for _, title in assignment.must_take])

				if len(adv_maths_f & must_takes) > 0 or len(adv_maths_s & must_takes) > 0:
					assignment.must_take = [(i, title) for (i, title) in assignment.must_take if (title not in adv_maths_f and title not in adv_maths_s)]

				chosen_a = random.choice(['Math 23a', 'Math 25a', 'Math 55a'])
				chosen_b = chosen_a[:-1] + 'b'

				cannot_take = (adv_maths_f - {chosen_a}).union(adv_maths_s - {chosen_b})
				assignment.fall -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'}).union(cannot_take)
				assignment.spring -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'}).union(cannot_take)
				assignment.must_take.extend([(1, chosen_a), (2, chosen_b)])
				assignment.fall = assignment.fall.union(adv_maths_f)
				assignment.spring = assignment.spring.union(adv_maths_s)

			assignment.fill_must_take()

	def choose_math(self, assignment):
		print "Inside choose math"
		must_takes = set([title for _, title in assignment.must_take])
		print "assignment.must_take: {}".format(assignment.must_take)
		print "must_takes by title: {}".format(must_takes)
		# if must_takes included some adv math courses, delete them
		cs_121 = 'CS 121'
		adv_maths_f = set(['Math 23a', 'Math 25a', 'Math 55a'])
		adv_maths_s = set(['Math 23b', 'Math 25b', 'Math 55b'])

		# We only have one of those courses if we also have 'adv_math' in self.priors
		if len(adv_maths_f & must_takes) > 0 or len(adv_maths_s & must_takes) > 0:
			print "\nNeed to get rid of what's inside must_take that's adv math"
			print "Before:"
			print "assignment.must_take: {}".format(assignment.must_take)
			assignment.must_take = [(i, title) for (i, title) in assignment.must_take if (title not in adv_maths_f and title not in adv_maths_s)]
			print "After:"
			print "assignment.must_take: {}".format(assignment.must_take)
			assignment.state[1].course_count -= 1
			assignment.state[2].course_count -= 1

		chosen_a = random.choice(['Math 23a', 'Math 25a', 'Math 55a'])
		chosen_b = chosen_a[:-1] + 'b'
		print "chosen_a, chosen_b: {}, {}".format(chosen_a, chosen_b)
		print "Current domains:"
		print "assignment.fall: {}".format(assignment.fall)
		print "assignment.spring: {}".format(assignment.spring)

		cannot_take = (adv_maths_f - {chosen_a}).union(adv_maths_s - {chosen_b})
		print "Since we chose {}, {}, we cannot take: {}".format(chosen_a, chosen_b, cannot_take)
		assignment.fall -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'}).union(cannot_take)
		assignment.spring -= {'Math 1a', 'Math 1b'}.union({'Math 21a', 'Math 21b', 'AM 21a', 'AM 21b'}).union(cannot_take)
		print "Now domains:"
		print "assignment.fall: {}".format(assignment.fall)
		print "assignment.spring: {}".format(assignment.spring)		
		assignment.must_take.extend([(1, chosen_a), (2, chosen_b)])
		print "We have now changed the must_take and want to error check it."
		print "assignment.must_take: {}".format(assignment.must_take)
		assignment.fall = assignment.fall.union(adv_maths_f)
		assignment.spring = assignment.spring.union(adv_maths_s)
		self.seen_plans = set()

		print "Calling fill_must_take from choose_math"
		assignment.fill_must_take(assignment)

	def check_prereqs(self, assignment, course, semester, before_must={}):
		# print "Checking prereqs for {} in semester {}".format(course, semester)

		if before_must != {}:
			prev_courses = before_must
		else:
			prev_courses = assignment.get_previous(assignment.state, semester)

		reqs = assignment.courses_to_prereqs[course]
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
		return self.insertion_sort(values)


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

	def order_domain_values(self, values):
		# Depending on heuristics, order vals by lowest workload, LCV, etc.
		if self.heuristics['lcv']:
			return self.get_lcv(values)
		
		# Identity function	
		to_shuffle = list(values)
		random.shuffle(to_shuffle)	
		return to_shuffle

	# Use Min Remaining Value and Least Constraining Value heuristics
	# Return multiple semesters from which to branch out: check
	# Stop assigning courses when assignment is complete:
	def get_unassigned_var(self, assignment):

		# MRV
		if self.heuristics['mrv']:
			return self.get_mrv(assignment)

		# Choose semesters in order
		for semester in range(self.latest_sem + 1, 9):
			if assignment.state[semester].course_count != assignment.state[semester].max_courses:
				return [semester]
		return None

	# Returns True if A=a and B=b does not satisfy binary constraints of prereqs/inequality
	# or if adding course a exceeds q-guide constraints
	def conflicts(self, A, a, B, b):

		# Could simplify this to one logical statement, but left this way
		if a == b: return True
		if A < B and b in self.disable_future[a]: return True
		if B < A and a in self.disable_future[b]: return True

		return False

	# Enforce arc-consistency with AC-3 and propagate constraints
	# Remove values from domain of Xi that aren't consistent with other variables
	# Inspired by http://aima.cs.berkeley.edu/python/csp.html
	def ac3(self, assignment, queue=None):
	    if queue == None:
	        queue = [(Xi, Xk) for Xi in assignment.state[Xi].neighbors()]
	    while queue:
	        (Xi, Xj) = queue.pop()
	        if self.remove_inconsistent_values(assignment, Xi, Xj):
	            for Xk in assignment.state[Xi].neighbors():
	                queue.append((Xk, Xi))

	# Return true if we remove a value
	# Inspired by http://aima.cs.berkeley.edu/python/csp.html
	def remove_inconsistent_values(self, assignment, Xi, Xj):
	    removed = False
	    begin_available = copy.deepcopy(assignment.state[Xi].available)
	    for x in begin_available:
	    	if assignment.state[Xj].available != set():
		        if all(map(lambda y: assignment.conflicts(Xi, x, Xj, y), assignment.state[Xj].available)):
		        	assignment.state[Xi].available.remove(x)
		        	removed = True
	    return removed

	# Returns solution(s) or failure message
	# Pseudocode in L5: CSP I
	# The 8 main variables should be the semesters, and each Semester object can take n (as specified) courses
	def solve(self, heuristics=None):
		def rec_backtrack(assignment):
			# Number of function calls, used to compare algorithms
			self.attempts += 1
			if self.is_complete(assignment):
				self.num_solutions += 1
				self.total -= 1
				solutions.append(assignment.state)
				print "\nSolution {}".format(50 - self.total)
				for i in range(1, 9):
					assignment.state[i].print_courses()
			else:
				semesters = self.get_unassigned_var(assignment)
				if semesters:
					for semester in semesters:
						# Wrapper to avoid key error
						all_vals = copy.deepcopy(assignment.state[semester].available)

						tries = 0
						count_available = len(assignment.state[semester].available)

						for value in self.order_domain_values(all_vals):
							self.course_attempts += 1

							if value in assignment.state[semester].available:
								tries += 1
								temp_assigned = tuple(assignment.state[semester].assigned.union(set([value])))
								
								# Checks for previously computed identical state
								if not assignment.already_computed(assignment.state, semester, temp_assigned):
									if assignment.state[semester].add_course(assignment, value, heuristics):
										assignment.all.add(value)

										for s in range(1, 9):
											if value in assignment.state[s].available:
												assignment.state[s].available.remove(value)

										start = semester
										if assignment.heuristics['mrv'] and value in self.all_maths:
											start = 1
										for q in range(start, 9):
											for j in assignment.disable_future[value]:
												if j in assignment.state[q].available:
													assignment.state[q].available.remove(j)													

										# We restart randomly if we satisfy one of these conditions
										if self.num_solutions == 8 or self.course_attempts > 2500 or self.total == 0:
											break

										new_version = copy.deepcopy(assignment)

										result = rec_backtrack(new_version)

										assignment.state[semester].remove_course(value)
										assignment.all.remove(value)

										for n in range(1, 9):
											if n % 2 == 1:
												if value in fall:
													assignment.state[n].available.add(value)
											else:
												if value in spring:
													assignment.state[n].available.add(value)
									else:
										if tries == count_available:
											if len(assignment.state[semester].assigned) < assignment.state[semester].max_courses:
												new_version = copy.deepcopy(assignment)
												new_version.state[semester].max_courses = new_version.state[semester].course_count
												rec_backtrack(new_version)
						break
					return False

		if not self.initialized:
			return 0, []

		self.heuristics = heuristics
		self.seen_plans = set()
		self.num_solutions = 0
		self.course_attempts = 0
		self.attempts = 0
		self.total = 50 
		solutions = []

		temp = copy.deepcopy(self)

		for i in range(40):
			begin = copy.deepcopy(temp)
			self.choose_must_takes(begin)

			rec_backtrack(begin)

			if self.total == 0:
				return self.attempts, solutions
			self.num_solutions = 0
			self.course_attempts = 0

		# After exhausting all possible assignments
		if len(solutions) != 0:
			return self.attempts, solutions

		return self.attempts, []
