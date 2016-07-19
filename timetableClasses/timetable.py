from re import match

currentYear = 2016
currentSemester = 2

commentMarker = "#"
gradeRanges = ["H1", "H2A", "H2B", "H3", "P", "N", "CMP"]

class Subject:
	def __init__(self, code, name, semester, completed=False, year=None, grade=None):
		# Making sure the code fits the unimelb format.
		if not match("^[A-Z]{4}[0-9]{5}$", code):
			raise ValueError("Value 'code' must be 4 capital letters and 5 numbers.")
		self.code = code

		self.name = name

		if semester not in [1, 2]:
			raise ValueError("Value 'semester' must be integer 1 or 2.")
		self.semester = semester

		# Making sure completed is a boolean.
		if not isinstance(completed, bool):
			raise ValueError("Value 'completed' must be True or False.")

		# Making sure a year was included if completed is True.
		if completed:
			if not year:
				raise ValueError("Value 'year' must be included if 'completed' is True.")
			else:
				# If year was included, it shouldn't be later than the current time.
				# If it is, we ask if it was intentional (how can you complete something in the future)?
				# If they say yes, we continue onwards.
				if ((year == currentYear and semester > currentSemester) or year > currentYear):
					confirmIntentional = input("You are trying to enter {} - {} as being completed in the future. Is this intentional? ".format(self.code, self.name))[0].lower()
					if confirmIntentional != "y":
						raise ValueError("this shouldn't be a valueerror probs")
		
		self.completed = completed
		self.year = year

		try:
			self.grade = int(grade)
		except TypeError:
			# No grade was given.
			self.grade = None
		except ValueError:
			# Must be a pass grade
			self.grade = None

	def __lt__(self, other):
		if self.year != other.year:
			return self.year < other.year
		else:
			if self.semester != other.semester:
				return self.semester < other.semester
			else:
				return self.code < other.code

	def __str__(self):
		return "{} - {}".format(self.code, self.name)


class Enrolment:
	def __init__(self, studentCode, studentName):
		if not match("^[0-9]{6}$", studentCode):
			raise ValueError("Value 'studentCode' must be 6 numbers.")
		self.studentCode = studentCode
		self.studentName = studentName

		self.subjects = []

	def addSubject(self, subject):
		self.subjects.append(subject)

	def readInSubjects(self, fileName):
		completedMarkers = ("START COMPLETED", "END COMPLETED")
		potentialMarkers = ("START POTENTIAL", "END POTENTIAL")
		
		# Returns code, name, semester, completed, year, grade
		# Works on input from the unimelb results page.
		def parseCompletedLine(line):
			l = line.split()
			year = int(l[0])
			semester = int(l[2])
			code = l[3]
			completed = True

			# Getting the name of the subject.
			i = 4 # Start index of the name.
			j = len(l) - 1 # End index of the name.

			# Looking for the grade class (H1, H3, etc.) then winding back to the name.
			while l[j] not in gradeRanges:
				j -= 1

			name = " ".join(l[i:j-2])

			# Just a pass/fail subject.
			if l[j] == "CMP":
				grade = None
			else:
				grade = int(l[j-1])

			# The true is for completed = True
			return (code, name, semester, completed, year, grade)

		def parsePotentialLine(line):
			l = line.split()
			year, grade = None, None
			completed = False
			
			code = l[0]
			name = l[1:-1]
			semester = int(l[-1])

			return (code, name, semester, completed, year, grade)
			
		# Expect this format:
		# CODE12345 "Name" Semester Year Grade
		# Year and Grade only necessary if already completed.
		# or this:
		# Expect a copy paste from the unimelb results page like this:
		# 2016 Semester 1  COMP30023 Computer Systems 1 88  H1 First Class Honours 12.500 
		with open(fileName, "r") as f:
			# Getting the start and end of the completed and potential sections.
			startCompleted = None
			endCompleted = None
			startPotential = None
			endPotential = None

			lines = [x.strip() for x in f.readlines() if len(x.strip()) > 0]

			# Getting the lines in which to scan for the completed and potential subjects.
			for i in range(len(lines)):
				if lines[i][0] == "#":
					if lines[i][2:] == completedMarkers[0]:
						startCompleted = i
					elif lines[i][2:] == completedMarkers[1]:
						endCompleted = i
					elif lines[i][2:] == potentialMarkers[0]:
						startPotential = i
					elif lines[i][2:] == potentialMarkers[1]:
						endPotential = i
			
			completed = lines[startCompleted:endCompleted]
			potential = lines[startPotential:endPotential]

			# We will change this to parsePotentialLine after we read the completed list.
			parseLine = parseCompletedLine

			for group in completed, potential:
				for l in group:
					if l[0] == commentMarker:
						continue

					args = parseLine(l)
					s = Subject(*args)
					self.addSubject(s)

				parseLine = parsePotentialLine


	def printCompletedFormatted(self, short=True):
		completed = sorted([s for s in self.subjects if s.completed])

		if len(completed) == 0:
			return

		for i in range(len(completed)):
			try:
				if completed[i].year != completed[i - 1].year or completed[i].semester != completed[i - 1].semester:
					print()
					print("{} Sem {}: ".format(completed[i].year, completed[i].semester), end='')
			except IndexError:
				pass

			if short:
				print(completed[i].code, end=' ')
			else:
				print(completed[i], end=' ')

		print()

	def printCompletedSimple(self, short=False):
		for i in sorted([s for s in daniel.subjects if s.completed]):
			if short:
				print(i.code)
			else:
				print(i)

	def getAverageGrade(self):
		completed = [s.grade for s in self.subjects if s.completed and s.grade is not None]
		return sum(completed)/len(completed)



meme = Subject("COMP30019", "Graphics and Interactions", 2)
meme2 = Subject("COMP30023", "Computer Systems", 1, True, 2016)
meme3 = Subject("GEOM20013", "Applications of GIS", 2, True, 2016)


daniel = Enrolment("696965", "Daniel Porteous")
"""
daniel.addSubject(meme)
daniel.addSubject(meme2)
daniel.addSubject(meme3)
daniel.addSubject(Subject("COMP20007", "Design of Algorithms", 1, True, 2015))
"""
#daniel.printCompletedFormatted()
#daniel.printCompletedSimple()

subjectsFile = "subjects.txt"
daniel.readInSubjects(subjectsFile)

daniel.printCompletedSimple()
print(daniel.getAverageGrade())