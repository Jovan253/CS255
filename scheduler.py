import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	# Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 weekdays in a week.
	# The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	# 	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	# This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	# Note here that the comedian and demographic are represented by objects, not strings.
	# The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	# The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	# Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	# 	your solution will be marked incorrectly.
	# The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	# In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	# demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic likes to see in their comedy shows e.g. ["Politics", "Family"]

	# comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	# For Task 1:
	# Keep in mind that a comedian can only have their show marketed to a demographic
	# 	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	# Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	# There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	# In some problems, demographics will have 2 topics and in others 3 topics.
	# A comedian will have between 3-8 different themes.

	# For Tasks 2 and 3:
	# A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	# 	that the demographic likes to see in their comedy shows.
	# Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	# A Comedian cannot be on stage for more than 2 hours a day.

	# You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	# Furthermore, you should not import anything else beyond what has been imported above.
	# To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable
		
		timeTable = self.backtrackingSearch()
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		for day, session in enumerate(timeTable):
			for slot, (comedian, demo) in enumerate(session):
				# checking if possible to add				
				timetableObj.addSession(days[day], slot + 1, comedian, demo, "main")

		#Do not change this line
		return timetableObj

	def backtrackingSearch(self):
		# Create an empty timetable
		timeTable = [list() for day in range(5)]
		# Create copies of the demographic and comedian lists
		demo_List = self.demographic_List.copy()
		com_List = self.comedian_List.copy()
		# Start recurisve backtracking to assign demographics and comedians to the schedule
		self.recursiveBacktracking(timeTable, demo_List, com_List)
		
	def recursiveBacktracking(self, timeTable, demo_List, com_List):
		# All demographics assigned
		if not demo_List:
			return True

		# Get the next demographic
		demo = demo_List[0]

		# iterate through the timetable
		for day in timeTable:
			# iterate through the comedians
			for comedian in com_List:				
				# Check comedian contains all themes of the demographic
				if all(topic in comedian.themes for topic in demo.topics):
					# remove the demographic and comedian as it has been assigned
					com_update = com_List[:]
					com_List.remove(comedian)
					demo_update = demo_List[:]
					demo_List.remove(demo)
					# Add the comedian and demo to the day
					day.append((comedian, demo))					

					# Recursively assign with the updated values
					if self.recursiveBacktracking(timeTable, demo_List, com_List):
						return True

					# Undo the previous if no backtracking to be done
					day.pop()
					demo_List.append(demo)
					com_List.append(comedian)

		# If no valid assignment found backtrack to previous slot
		return False



	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to allocate one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#Here is where you schedule your timetable
		
		timeTable = self.backtrackingSearch()
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		for day, session in enumerate(timeTable):
			for slot, (comedian, demo) in enumerate(session):					
				if all(topic in comedian.themes for topic in demo.topics):		
					timetableObj.addSession(days[day], slot + 1, comedian, demo, "main")
				elif any(topic in comedian.themes for topic in demo.topics):
					timetableObj.addSession(days[day], slot + 1, comedian, demo, "test")

		#Do not change this line
		return timetableObj
	
	def backtrackingSearch(self):
		# Create an empty timetable
		timeTable = [list() for day in range(5)]
		# Create copies of the demographic and comedian lists
		demo_List = self.demographic_List.copy()
		com_List = self.comedian_List.copy()
		hours_per_week = {comedian: 0 for comedian in comedian_List}
		hours_per_day = {comedian: 0 for comedian in comedian_List}
		# Start recurisve backtracking to assign demographics and comedians to the schedule
		self.recursiveBacktracking(timeTable, demo_List, com_List, hours_per_week, hours_per_day)
		
	def recursiveBacktracking(self, timeTable, demo_List, com_List, hours_per_week, hours_per_day):
		# All demographics assigned
		if not demo_List:
			return True

		# Get the next demographic
		demo = demo_List[0]

		# iterate through the timetable
		for day in timeTable:
			# iterate through the comedians
			for comedian in com_List:
				# Check comedian contains all themes of the demographic
				# Check if comedian can therefore perform a main show
				if all(topic in comedian.themes for topic in demo.topics):					
					# Check that the assignment of this main show doesn't breach the fact a comedian can perform max four hours a week and etc
					if (hours_per_week[comedian] + 2 <= 4 and hours_per_day[comedian] + 2 < = 2):
						# remove the demographic and comedian as it has been assigned
						com_update = com_List[:]
						com_List.remove(comedian)
						demo_update = demo_List[:]
						demo_List.remove(demo)
						# Add the comedian and demo to the day
						day.append((comedian, demo))

						# Update the number of hours performed per week and per day
						hours_per_week[comedian] += 2										
						hours_per_day[comedian] += 2
				

						# Recursively assign with the updated values
						if self.recursiveBacktracking(timeTable, demo_update, com_update, hours_per_week, hours_per_day):
							return True

						# Undo the previous if no backtracking to be done
						day.pop()
						demo_List.append(demo)
						com_List.append(comedian)
						hours_per_week[comedian] -= 2										
						hours_per_day[comedian] -= 2
				
				# Check if comedian can perform a test show
				elif any(topic in comedian.themes for topic in demo.topics):
					# Check that the assignment of this main show doesn't breach the fact a comedian can perform max four hours a week
					if (hours_per_week[comedian] + 1 <= 4 and hours_per_day[comedian] + 1 < = 2):
						# remove the demographic and comedian as it has been assigned					
						com_update = com_List[:]
						com_List.remove(comedian)
						demo_update = demo_List[:]
						demo_List.remove(demo)
						# Add the comedian and demo to the day
						day.append((comedian, demo))

						# Update the number of hours performed per week and per day
						hours_per_week[comedian] += 1
						hours_per_day[comedian] += 1				
				

						# Recursively assign with the updated values
						if self.recursiveBacktracking(timeTable, demo_update, com_update, hours_per_week, hours_per_day):
							return True

						# Undo the previous if no backtracking to be done
						day.pop()
						demo_List.append(demo)
						com_List.append(comedian)
						hours_per_week[comedian] -= 1										
						hours_per_day[comedian] -= 1


		# If no valid assignment found backtrack to previous slot
		return False

	

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (i.e., £200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable
		time_table = {}
		for day in timetable:
			time_table[day] = [None]*len(timetable[day])

		queue = PriorityQueue()	
		queue.push((0, time_table))

		visited = set()

		while queue is not empty:
			# Get the node with lowest cost
			cost, current_timetable = queue.pop()
			# if this node is the goal state return it
			if isGoal(current_timetable):
				return current_timetable
			# if current timetable has not been visited, visit it and expand
			if current_timetable not in visited:
				visited.add(current_timetable)
				# iterate through generated actions that can be taken from current node
				for action in getActions(current_timetable, comedian_List, demographics_List)	
					# Apply actions to the current timetable
					new_timetable = applyAction(current_timetable, action)
					# Calculate the cost of this new function
					next_cost = cost + costFunction(new_timetable)
					# Add this new cost to an estimated cost to the queue along with the new timetable
					queue.push((next_cost + heuristicFunction(new_timetable), new_timetable))

		return None
		#Do not change this line
		return timetableObj
	#endfunction

	# Checks all constraints from task 2 have been met
	def isGoal(time_table):
		# Check each demographic has been assigned one main show and one test show
		for day in time_table:
			for slot in time_table[day]:
				if slot is not None:
					if slot[0] == "main":
						if not hasMain(time_table, slot[1]):
							return False
					elif slot[0] == "test":
						if not hasTest(time_table, slot[1]):
							return False
		# Check each comedian has been assigned to a demographic
		for day in time_table:
			for slot in time_table[day]:
				if slot is None and slot[2] is None:
					return False
		
		# Check each comedian does not perform more than 4 hours a week
		for comedian in comedian_List:
			# if total hourrs is > 4
				return False

		# Check comedian doesnt perform mroe than 2 hours a day
		for day in time_table:
			for slot in time_table[day]:
				if slot is None and slot[2] is None:
					# get hours per day
					return False

		return True
	#endfunction

	# Checks if a main show has been assigned to the demographic
	def hasMain(time_table, demographic):
		for day in time_table:
			for slot in time_table[day]:
				if slot is not None and slot[0] == "main" and slot[1] == demographic:
					return True

		return False
	#endfunction

	# Checks if a test show has been assigned to the demographic
	def hasTest(time_table, demographic):
		for day in time_table:
			for slot in time_table[day]:
				if slot is not None and slot[0] == "test" and slot[1] == demographic:
					return True

		return False
	#endfunction

	def getActions():
		actions = []

		# Loop through the timetable object and generate actions for each slot
		for day in timetable:
			for slot in timetable[day]:
				# if empty slot generate actions to add main show or test show
				if time_table[day][slot] is None:
					for demographic in demographic_List:
						if not hasMain(time_table, demographic):
							actions.append((None, demographic, "main"))
						if not hasTest(time_table, demographic):
							actions.append((None, demographic, "test"))
				# if slot is main show, assign a comedian
				elif time_table[day][slot][0] == "main":
					demographic = time_table[day][slot][1]
					for comedian in comedian_List:
						if canMarket(comedian, demographic):
							actions.append((comedian, demographic, "main"))
				# if slot is test show assign a comedian
				elif time_table[day][slot][0] == "test":
					demographic = time_table[day][slot][1]
					for comedian in comedian_List:
						if canMarket(comedian, demographic):
							actions.append((comedian, demographic, "test"))

		return actions
	#endfunction

	def applyAction(time_table, action):		
		comedian, demographic, show_type = action
		# Loop through the timetable and find an empty slot
		for day in timetable:
			for slot in timetable[day]:
				if time_table[day][slot] is None:
					# Assign the action to the empty slot
					time_table[day][slot] = (comedian, demographic, show_type)
					return time_table
		# If no empty slot is found, return the original schedule
		return time_table
	#endfunction

	class PriorityQueue:
		def __init__(self):
			self._heap = []

		def push(self, item, priority):
			# Add the new item to the end of the heap
			heap = self._heap
			heap.append((priority, item))

			# Shift the new item up to its proper position
			i = len(heap) - 1
			while i > 0:
				# Check if the new item is greater than its parent
				parent = (i - 1) // 2
				if heap[i][0] > heap[parent][0]:
					# Swap the new item with its parent
					heap[i], heap[parent] = heap[parent], heap[i]
					i = parent
				else:
					break

		def pop(self):
			# Remove and return the top item from the heap
			heap = self._heap
			top = heap[0]

			# Move the last item in the heap to the top and sift it down
			last = heap.pop()
			if heap:
				heap[0] = last
				i = 0
				while True:
					# Find the child with the larger value
					left = 2 * i + 1
					right = 2 * i + 2
					if right < len(heap):
						if heap[right][0] > heap[left][0]:
							child = right
						else:
							child
	#endclass
			




