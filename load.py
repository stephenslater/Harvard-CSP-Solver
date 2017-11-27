import csv


# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

strict = 'strict'
recommended = 'recommended'
one_of = 'one of'
all_of = 'all of'

courses_to_q = dict()
courses_to_prereqs = dict()

fall = set()
spring = set()
unknown = set()
undergrad = set()
grad = set()

# Storing None whenever information does not exist
def q_helper(s):
	print "S is {}".format(s)
	if len(s) == 0:
		return None
	else:
		return float(s)

def p_helper(s):
	if s:
		lst = s.split(';')
		#print lst
		return lst
		#print s
	else:
		return []

# Stores Q-scores
def storeQdata(filename):
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter = ",")
		first = True

		for row in reader:
			if first:
				first = False
				continue

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
				unknown.add(course)

			# Stores Grad versus Undergrad class
			name = course.split()
			if name[1][0] == '2' and len(name[1]) > 2:
				grad.add(course)
			else:
				undergrad.add(course)


		print "Q-scores for courses are {}".format(courses_to_q)
		print "Fall classes are {}".format(fall)
		print "Spring classes are {}".format(spring)
		print "Unknown semester classes are {}".format(unknown)
		print "Grad classes are {}".format(grad)
		print "Undergrad classes are {}".format(undergrad)

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
			#print row
			
			course = row[0]
			courses_to_prereqs[course] = {strict: {one_of: [], all_of: []}, recommended: {one_of: [], all_of: []}}
			courses_to_prereqs[course][strict][all_of] = p_helper(row[1])
			courses_to_prereqs[course][strict][one_of] = p_helper(row[2])
			courses_to_prereqs[course][recommended][all_of] = p_helper(row[3])
			courses_to_prereqs[course][recommended][one_of] = p_helper(row[4])

	print courses_to_prereqs


#storeQdata('courses.csv')
storePrereqs('prerequisites.csv')
			
