import csv


# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

courses_to_q = dict()
fall = set()
spring = set()
unknown = set()
undergrad = set()
grad = set()

def helper(s):
	print "S is {}".format(s)
	if len(s) == 0:
		return None
	else:
		return float(s)

# Makes 
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
			courses_to_q[course][q] = helper(row[2])
			courses_to_q[course][w] = helper(row[3])
			courses_to_q[course][a] = helper(row[4])
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

storeQdata('courses.csv')
			
