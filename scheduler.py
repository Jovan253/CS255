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
	''' My approach to Task 1 was to follow the structure of the backtrack search algorithm presented to us in the
		lecture. Backtracking is an algorithm that builds candidates for a solution and abandons candidates (backtracks) when
		they cannot be used to create a valid solution. Its well suited to constraint satisfaction problems.
	'''
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable		
		time_table = self.backtrackingSearch()		
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		# Enumerate allows us to iterate through tuple
		for day, session in enumerate(time_table):			
			for slot, (comedian, demo) in enumerate(session):								
				timetableObj.addSession(days[day], slot + 1, comedian, demo, "main")

		#Do not change this line
		return timetableObj

	''' This method creates an empty timetable that we will recursively add to and then return the timetable.
		We create a copy of demographic list and a duplicate for comedian list so a comedian can perform two shows.
		We copy them because we dont want to alter their contents.
	'''
	def backtrackingSearch(self):		
		# Create an empty timetable
		time_table = [list() for day in range(5)]		
		#count = {comedian.name: 0 for  comedian in self.comedian_List}
		# Create copies of the demographic and comedian lists
		demo_List = self.demographic_List.copy()
		# Create two comedian lists - allows a comedian to perform two shows a week
		com_List = self.comedian_List * 2
		# Start recurisve backtracking to assign demographics and comedians to the schedule
		self.recursiveBacktracking(time_table, demo_List, com_List)
		return time_table
		
	''' In this method we iterate through the timetable and the comedian list to check if the constraints of 
		the task are met. If the constraints are met then we remove comedian and demogrpahic from their approproate
		list and add them to the current day of the timetable. Then we recall the method with the new lists. If there is
		no backtracking to be done then we undo the assignments. The recursive method terminates when the demographic list
		is empty - ie all demographics have been assigned. Additionally, if there are no valid assignments we return False
		after our loops.
	'''
	def recursiveBacktracking(self, time_table, demo_List, com_List):
		# Base Case - demo_list is empty	
		if not demo_List:			
			return True

		# Get the next demographic
		demo = demo_List[0]
		print(time_table)
		# iterate through the timetable
		for day in time_table:
			# iterate through the comedians
			for comedian in com_List:				
				# Check comedian contains all topics of the demographic #and that we dont have 6 days
				if all(topic in comedian.themes for topic in demo.topics) and len(day) != 5:					
					# remove the demographic and comedian as it has been assigned					
					com_List.remove(comedian)										
					demo_List.remove(demo)					
														
					# Add the comedian and demo to the day												
					day.append((comedian, demo))			
					
					# Recursively assign with the updated values
					if self.recursiveBacktracking(time_table, demo_List, com_List):
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

	''' In Task 2 I will again be using backtracking as it is well suited to this constraint satisfaction
		problem
	'''
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#Here is where you schedule your timetable
		# Call our backtracking method to add to the timetable
		timeTable = self.backtrackingTestSearch()
		# List of days for adding to timetableObj
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		# Iterate through the timetable and add each element to the timetableObj to return
		for day, session in enumerate(timeTable):
			for slot, (comedian, demo, show_type) in enumerate(session):									
				timetableObj.addSession(days[day], slot + 1, comedian, demo, show_type)

		#Do not change this line
		return timetableObj
	
	''' This method is used to create an empty timetable that will be added upon on recursive calls of backtracking
		and then returned as a complete timetable. We create two demographic lists in order to be able to assign
		each demographic one main and one test show. Then we use the dictionary hours_per_week to track the amount
		of hours a comedian has performed in the week. And use a dictionary hours_per_day to track the amount of
		hours a comedian performed in a day.
	'''
	def backtrackingTestSearch(self):
		# Create an empty timetable
		timeTable = [list() for day in range(5)]
		# Create 2 demographic list copies - Each demographic must be assigned a main and test show
		main_List = self.demographic_List.copy()
		test_List = self.demographic_List.copy()		
		# Create a dictionary to track a comedians hours in a week - A comedian can perform a maximum of 4 hours
		# of shows a week
		hours_per_week = {comedian: 0 for comedian in self.comedian_List}				
		# Create a dictionary to track a comedians hours in a day, combine day and comedian as the key
		# as we will iterate twice through the days. - A comedian cannot perform for more than two hours a day
		hours_per_day = {(comedian, day) : 0 for comedian in self.comedian_List for day in range(5)}				
		# Start recurisve backtracking to assign demographics and comedians to the schedule
		self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day)	
		# Return the timetable	
		return timeTable
		
	''' This method will recursively call itself to add to the timetable or change it. First we assign all the 
		main shows we can. To do this we iterate through the timetable and the hours_per_week - as it contains all the
		comedians we need as well as their hours. Then if the comedian themes contains all the topics the demographic likes
		then it can be added to the timetable as a main show as long as the hours_per_week is less than 4 and hours_per_day is 
		less than 2 or 0. Additionally the max length of days should be 10. We then adapt the main show list to remove the 
		current demographic as well as change the hours_per_week and hours_per_day and call the method again. If there is no
		backtracking to be done we undo these assignments.
		Once we have assigned all main shows we look at the test shows. We once again iterate through timetable and hours_per_week
		and check that hours_per_week is less than 4 and hours_per_day is less than 2 as previous. However, for a test show
		we check that if any of a comedians themes is liked by a demographic it is added to the test show. So if we abide
		by these rules we add the comedian, demographic and test to the timetable and make similar changes according to 
		specification. Then we call the method again if this returns false then we revert our previous assignments.
		Finally when all assignments made return True, unless no valid assignments to be made.		
	'''
	def recursiveTestBacktracking(self, timeTable, main_List, test_List, hours_per_week, hours_per_day):		
		# Assign all possible main shows to a comedian
		if main_List:			
			# Get the next demographic of the main show
			main = main_List[0]
			# keep a count for the hours_per_day variable
			count = -1
			# iterate through the timetable
			for day in timeTable:
				# Increase count for each day, 0-4
				count+= 1				
				# iterate through the comedians
				for comedian, hours in hours_per_week.items():					
					# Check comedian contains all themes of the demographic, has not performed more than 4 hours a week 
					# and has not performed more than 2 hours this day														
					if all(topic in comedian.themes for topic in main.topics) and (hours < 4) and (hours_per_day[(comedian,count)] == 0) and len(day) != 10:																																			
						# Remove the main show demographic as it has been assigned																
						main_List.remove(main)
						# Add the comedian and demo to the day under main show type
						day.append((comedian, main, "main"))							

						# Update the number of hours performed per week and per day
						hours_per_week[comedian] = hours + 2	
						hours_per_day[(comedian,count)] += 2								

						# Recursively assign with the updated values
						if self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day):								
							return True
						
						# Undo the previous if no backtracking to be done
						day.pop()
						main_List.append(main)						
						hours_per_week[comedian] -= 2
						hours_per_day[(comedian,count)] -= 2

		# Once all main shows have been assigned look to assign the test shows
		elif test_List:	
			# Once again keep a count for hours_per_day
			day_count = -1	
			# Get the next demographic of the test show		
			test = test_List[0]
			# iterate through the timetable
			for day in timeTable:
				day_count += 1
				# iterate through the comedians
				for comedian, hours in hours_per_week.items():	
					# Check if comedian can perform a test show - ie any comedian themes is liked by the demographic and comedian hasnt
					# perfromed more than 2 hours a day or 4 hours a week
					if any(topic in comedian.themes for topic in test.topics) and (hours < 4) and (hours_per_day[(comedian, day_count)] < 2) and len(day) != 10:												
						# Remove the test show demographic as it has been assigned
						test_List.remove(test)
						# Add the comedian and demo to the day under test show type
						day.append((comedian, test, "test"))

						# Update the number of hours performed per week and per day
						hours_per_week[comedian] = hours + 1
						hours_per_day[(comedian, day_count)] += 1				
				

						# Recursively assign with the updated values
						if self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day):
							return True

						# Undo the previous if no backtracking to be done
						day.pop()
						test_List.append(test)						
						hours_per_week[comedian] -= 1
						hours_per_day[(comedian, day_count)] -= 1	

		# All shows have been assigned - complete timetable													
		else:
			return True
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
		time_table = self.aStar()
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		for day, session in enumerate(time_table):
			for slot, (comedian, demo, show_type) in enumerate(session):	
				timetableObj.addSession(days[day], slot + 1, comedian, demo, show_type)
		
		#Do not change this line
		return timetableObj
	#endfunction

	def aStar(self):
		time_table = {}
		for day in timetable:
			time_table[day] = [None]*len(timetable[day])

		queue = PriorityQueue()	
		queue.push((0, time_table))

		visited = set()

		while len(queue) > 0:
			# Get the node with lowest cost
			cost, current_timetable = queue.pop()
			# if this node is the goal state return it
			if isGoal(current_timetable):
				return current_timetable
			# if current timetable has not been visited, visit it and expand
			if current_timetable not in visited:
				visited.add(current_timetable)
				# iterate through generated actions that can be taken from current node
				for action in getActions(current_timetable, comedian_List, demographics_List):
					# Apply actions to the current timetable
					new_timetable = applyAction(current_timetable, action)
					# Calculate the cost of this new function
					next_cost = cost + totalCost(new_timetable)
					# Add this new cost to an estimated cost to the queue along with the new timetable
					queue.push((next_cost + heuristicFunction(new_timetable), new_timetable))

		return None
	#

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
	#

	# Checks if a main show has been assigned to the demographic
	def hasMain(time_table, demographic):
		for day in time_table:
			for slot in time_table[day]:
				if slot is not None and slot[0] == "main" and slot[1] == demographic:
					return True

		return False
	#

	# Checks if a test show has been assigned to the demographic
	def hasTest(time_table, demographic):
		for day in time_table:
			for slot in time_table[day]:
				if slot is not None and slot[0] == "test" and slot[1] == demographic:
					return True

		return False
	#

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
	#

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
	#

	# Calculates heuristic cost of schedule
	def heuristicFunction(time_table):
		# Initialize the heuristic cost to 0
		heuristic_cost = 0
		# Loop through the timetable and calculate the minimum cost for each remaining slot
		for day in timetable:
			for slot in timetable[day]:
				if time_table[day][slot] is None:
					min_cost = 1000000
					# Calculate cost of assigning a main show or a test show
					for demographic in demographic_List:
						if not hasMain(time_table, demographic):
							heuristic_cost = getCost(time_table, (None, demographic, "main"))
							if heuristic_cost < min_cost:
								min_cost = heuristic_cost
						if not hasTest(time_table, demographic):
							heuristic_cost = getCost(time_table, (None, demographic, "test"))
							if heuristic_cost < min_cost:
								min_cost = heuristic_cost
					# Calculate cost of assigning a comedian to a main show
					for comedian in comedians:
						if totalHours(time_table, comedian) + 2 <= 4:
							heuristic_cost = getCost(time_table, (comedian, demographic, "main"))
							if heuristic_cost < min_cost:
								min_cost = coheuristic_costst
					# Calculate cost of assigning a comedian to a test show
					for comedian in comedians:
						if totalHours(time_table, comedian) + 1 <= 4:
							heuristic_cost = getCost(time_table, (comedian, demographic, "test"))
							if heuristic_cost < min_cost:
								min_cost = heuristic_cost	
					# Add minimum cost to total cost
					heuristic_cost += min_cost
		return heuristic_cost
	#

	def totalHours(time_table, comedian):
		total = 0
		for day in time_table:
			for slot in time_table[day]:
				if slot:
					comic, demo, s_type = slot
					if s_type == "main":
						total += 2
					elif s_type == "test":
						total += 1
		return total
	#

	# Calculates total cost of a schedule
	def totalCost(timetable):
		total = 0
		for day in timetable:
			for slot in timetable[day]:
				if slot:
					comic, demo, s_type = slot

					if s_type == "main":
						cost = 500
						if alreadyPerformedMain(timetable, comedian, False):
							cost = 300						
						if alreadyPerformedMain(timetable, comedian, True):
							cost = 100

					elif s_type == "test":
						cost = getCost(timetable, slot)

					total += cost
		return total
	#


	# Calculates the cost of a specific action
	def getCost(time_table, action):
		comedian, demographic, show_type = action
		cost = 0
		# If the show is a main show, do the following
		if show_type == "main":			
			# If comedian has already performed this week, price is set to 300
			if alreadyPerformedMain(time_table, comedian, False):
				cost = 300
				# Now check if comedian performed the previous day, if so price is 100
				if alreadyPerformedMain(time_table, comedian, True):
					cost = 100
			# If this is the first main show the comedian is performing, price is 500
			else:
				cost = 500
		# If show is test show, do the following	
		elif show_type == "test":
			cost = alreadyPerformedTest(time_table, comedian)
		return cost
	#

	def alreadyPerformedMain(time_table, comedian, consec_day):
		for day in time_table:
			for slot in time_table[day]:
				# If the comedian has performed main show on the day
				if time_table[day][slot] is not None:
					comic, demo, s_type = time_table[day][slot]
					if comic == comedian and s_type == "main":
						# Check for consecutive days 
						if consec_day:
							# Not possible if the day is Monday
							if day == "Monday":
								return False
							# Otherwise check the previous day to see if a comedian performed
							elif time_table[day - 1][slot] is not None:
								return True
						else:
							return True
		return False
	#

	def alreadyPerformedTest(time_table, comedian):
		count = 0
		days = []
		cost = 0
		for day in time_table:
			for slot in time_table[day]:
				if time_table[day][slot] is not None:
					comic, demo, s_type = time_table[day][slot]
					# If a test show and the appropriate comedian increase the count
					if comic == comedian and s_type == "test":
						count+=1
						cost = calcCost(count)
						# Comedian cannot perform for more than two hours a day - main show & test show not possible just 2 test shows
						# Loop through list of correct days and see if current day is equivalent and that count is more than 1
						for i in days:
							if days[i] == day and count > 1:
								cost = cost // 2
						# Add day to a list of days 
						days.append(day)														 		
		return cost
	#

	def calcCost(count):
		cost = 0
				# Lowest price for subsequent test shows is 100 as max of 4 hours a week, test show is 1 hour
		if count == 1:
			cost = 250
		elif count == 2:
			cost = 200
		elif count == 3:
			cost = 150
		elif count == 4:
			cost = 100
		else:
			cost = 0
		return cost
	#

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
			




