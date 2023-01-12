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

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 weekdays in a week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a "main" show or a "test" show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic likes to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		self.randomMainSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to allocate one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.
	# def createTestShowSchedule(self):
	# 	#Do not change this line
	# 	timetableObj = timetable.Timetable(2)

	# 	#Here is where you schedule your timetable
	# 	# Call our backtracking method to add to the timetable
	# 	timeTable = self.backtrackingTestSearch()
	# 	# List of days for adding to timetableObj
	# 	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

	# 	# Iterate through the timetable and add each element to the timetableObj to return
	# 	for day, session in enumerate(timeTable):
	# 		for slot, (comedian, demo, show_type) in enumerate(session):									
	# 			timetableObj.addSession(days[day], slot + 1, comedian, demo, show_type)

	# 	#Do not change this line
	# 	return timetableObj
	
	# ''' This method is used to create an empty timetable that will be added upon on recursive calls of backtracking
	# 	and then returned as a complete timetable. We create two demographic lists in order to be able to assign
	# 	each demographic one main and one test show. Then we use the dictionary hours_per_week to track the amount
	# 	of hours a comedian has performed in the week. And use a dictionary hours_per_day to track the amount of
	# 	hours a comedian performed in a day.
	# '''
	# def backtrackingTestSearch(self):
	# 	# Create an empty timetable
	# 	timeTable = [list() for day in range(5)]
	# 	# Create 2 demographic list copies - Each demographic must be assigned a main and test show
	# 	main_List = self.demographic_List.copy()
	# 	test_List = self.demographic_List.copy()		
	# 	# Create a dictionary to track a comedians hours in a week - A comedian can perform a maximum of 4 hours
	# 	# of shows a week
	# 	hours_per_week = {comedian: 0 for comedian in self.comedian_List}				
	# 	# Create a dictionary to track a comedians hours in a day, combine day and comedian as the key
	# 	# as we will iterate twice through the days. - A comedian cannot perform for more than two hours a day
	# 	hours_per_day = {(comedian, day) : 0 for comedian in self.comedian_List for day in range(5)}				
	# 	# Start recurisve backtracking to assign demographics and comedians to the schedule
	# 	self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day)	
	# 	# Return the timetable	
	# 	return timeTable	

	# def recursiveTestBacktracking(self, timeTable, main_List, test_List, hours_per_week, hours_per_day):		
	# 	# Assign all possible main shows to a comedian
	# 	if main_List:			
	# 		# Get the next demographic of the main show
	# 		main = main_List[0]
	# 		# keep a count for the hours_per_day variable
	# 		count = -1
	# 		# iterate through the timetable
	# 		for day in timeTable:
	# 			# Increase count for each day, 0-4
	# 			count+= 1				
	# 			# iterate through the comedians
	# 			for comedian, hours in hours_per_week.items():					
	# 				# Check comedian contains all themes of the demographic, has not performed more than 4 hours a week 
	# 				# and has not performed more than 2 hours this day														
	# 				if all(topic in comedian.themes for topic in main.topics) and (hours < 4) and (hours_per_day[(comedian,count)] == 0) and len(day) != 10:																																			
	# 					# Remove the main show demographic as it has been assigned																
	# 					main_List.remove(main)
	# 					# Add the comedian and demo to the day under main show type
	# 					day.append((comedian, main, "main"))							

	# 					# Update the number of hours performed per week and per day
	# 					hours_per_week[comedian] = hours + 2	
	# 					hours_per_day[(comedian,count)] += 2								

	# 					# Recursively assign with the updated values
	# 					if self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day):								
	# 						return True
						
	# 					# Undo the previous if no backtracking to be done
	# 					day.pop()
	# 					main_List.append(main)						
	# 					hours_per_week[comedian] -= 2
	# 					hours_per_day[(comedian,count)] -= 2

	# 	# Once all main shows have been assigned look to assign the test shows
	# 	elif test_List:	
	# 		# Once again keep a count for hours_per_day
	# 		day_count = -1	
	# 		# Get the next demographic of the test show		
	# 		test = test_List[0]
	# 		# iterate through the timetable
	# 		for day in timeTable:
	# 			day_count += 1
	# 			# iterate through the comedians
	# 			for comedian, hours in hours_per_week.items():	
	# 				# Check if comedian can perform a test show - ie any comedian themes is liked by the demographic and comedian hasnt
	# 				# perfromed more than 2 hours a day or 4 hours a week
	# 				if any(topic in comedian.themes for topic in test.topics) and (hours < 4) and (hours_per_day[(comedian, day_count)] < 2) and len(day) != 10:												
	# 					# Remove the test show demographic as it has been assigned
	# 					test_List.remove(test)
	# 					# Add the comedian and demo to the day under test show type
	# 					day.append((comedian, test, "test"))

	# 					# Update the number of hours performed per week and per day
	# 					hours_per_week[comedian] = hours + 1
	# 					hours_per_day[(comedian, day_count)] += 1				
				

	# 					# Recursively assign with the updated values
	# 					if self.recursiveTestBacktracking(timeTable, main_List, test_List, hours_per_week, hours_per_day):
	# 						return True

	# 					# Undo the previous if no backtracking to be done
	# 					day.pop()
	# 					test_List.append(test)						
	# 					hours_per_week[comedian] -= 1
	# 					hours_per_day[(comedian, day_count)] -= 1	

	# 	# All shows have been assigned - complete timetable													
	# 	else:
	# 		return True
	# 	# If no valid assignment found backtrack to previous slot
	# 	return False
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
		remaining = [(demo, "main") for demo in self.demographic_List] + [(demo, "test") for demo in self.demographic_List]
		#Here is where you schedule your timetable
		initial_state = Scheduler.ScheduleState({'Monday':{i:{} for i in range(10)}, 'Tuesday':{i:{} for i in range(10)}, 'Wednesday':{i:{} for i in range(10)},
		'Thursday':{i:{} for i in range(10)},'Friday':{i:{} for i in range(10)}}, self.demographic_List, self.comedian_List, remaining,
		{comedian.name: {"main":0,"test":0} for comedian in self.comedian_List},{comedian.name: {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0} for comedian in self.comedian_List})
		schedule = self.aStar(initial_state)
		time_table = self.simulatedAnnealing(schedule)

		for day, sessions in time_table.items():
			for slot, (comedian, demo, show_type) in sessions.items():
				# Add the session to the timetable				
				timetableObj.addSession(day, slot + 1, comedian, demo, show_type)
					
		#Do not change this line
		return timetableObj
	#endfunction
	# 	

	def simulatedAnnealing(self, schedule, max_iterations=1000):
		current_schedule = schedule.copy()
		current_cost = self.cost_function(current_schedule)
		best_schedule = current_schedule.copy()
		best_cost = current_cost
		print(current_cost)
		
		for i in range(max_iterations):						
			temperature = max_iterations/(i+1)
			if temperature == 0:
				break
			
			# Generate a random neighbor by swapping two elements in the schedule
			new_schedule = self.swapSlots(current_schedule)
			new_cost = self.cost_function(new_schedule)
			
			delta_cost = new_cost - current_cost			
			if delta_cost < 0:
				print("fyghjkljhgfdasjdahsdlkasjdlajsdlasjdalsjdlkajdl")
				current_schedule = new_schedule.copy()
				current_cost = new_cost
				if new_cost < best_cost:
					print("BEST COST")
					best_schedule = new_schedule.copy()
					best_cost = new_cost								
			elif random.random() < math.exp(-delta_cost / temperature):
				current_schedule = new_schedule.copy()
				current_cost = new_cost
				
		return best_schedule

	# PERFEECT DO NOT CHANGE
	def cost_function(self, schedule):
		comedian_cost = {comedian.name: 0 for comedian in self.comedian_List}
		num_test = {comedian.name: 0 for comedian in self.comedian_List}
		num_main = {comedian.name: 0 for comedian in self.comedian_List}
		price = 0					
		for day,slots in schedule.items():												
			for slot, slot_info in slots.items():
				if slot_info:
					comedian, demo,show = slot_info
					if show == "main":
						num_main[comedian.name] += 1
						if num_main[comedian.name] == 2:
							if self.nextDay(schedule,comedian,day):
								comedian_cost[comedian.name] += 100
							else:
								comedian_cost[comedian.name] += 300
						elif num_main[comedian.name] == 1:
							comedian_cost[comedian.name] += 500
					elif show == "test":	
						num_test[comedian.name] += 1					
						if self.sameDay(schedule, comedian, day):						
							comedian_cost[comedian.name] += (300 - (50 * num_test[comedian.name])) / 2	
						else:							
							comedian_cost[comedian.name] += 300 - (50 * num_test[comedian.name]) # test is 1 hours so basically a count

		for name,number in comedian_cost.items():
			price += number
		return price

	def swapSlots(self, schedule):
		new_schedule = None
		while not self.checkValid(new_schedule):
			days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
			day1 = days[random.randint(0,4)]
			day2 = days[random.randint(0,4)]
			slot1 = random.randint(0,9)
			slot2 = random.randint(0,9)
			new_schedule = schedule.copy()	
			new_schedule[day1][slot1], new_schedule[day2][slot2] = new_schedule[day2][slot2], new_schedule[day1][slot1] 	
		return new_schedule
				
	
	def checkValid(self, schedule):
		if schedule is None:
			return False
		per_day = {comedian.name: {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0} for comedian in self.comedian_List}
		for day,slots in schedule.items():
			for slot, slot_info in slots.items():
				#if slot_info:
					c,d,s = slot_info					
					if s == "main":
						#print("main show")
						per_day[c.name][day] += 2
					elif s == "test":
						per_day[c.name][day] += 1
		
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]	
		for comedian in self.comedian_List:
			for date in days:
				if per_day[comedian.name][date] > 2:					
					return False

		return True

	def numMainShows(self, schedule, comedian):
		total = 0
		for day, slots in schedule.items():
			for slot, slot_info in slots.items():
				if slot_info:
					com, demo,show = slot_info
					if com == comedian and show == "main":
						total +=1
		return total

	def nextDay(self, schedule, comedian, day):
		if day == "Monday":
			return False
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		index = days.index(day)		
		next_day = days[index-1]		
		for slot, slot_info in schedule[next_day].items():
			if slot_info:
				com, demo,show = slot_info				
				if com == comedian and show == "main":
					return True
		return False

	def sameDay(self, schedule, comedian, day):		
		total = 0
			
		for slot, slot_info in schedule[day].items():
			if slot_info:
				com, demo,show = slot_info			
				# Can only be two test shows in a day as comedian performs max 2 hours a day	
				if com == comedian and show == "test":
					total += 1
				if total == 2:
					return True
		return False

	''' I use an astar algorithm to quickly obtain a complete schedule'''
	def aStar(self, start_state):
		#states = [start_state]	
		queue = Scheduler.PriorityQueue()
		queue.put((start_state, 0),0)
		visited = set()
		while not queue.empty():	
			#states.sort(key=lambda x:x.cost)
			#print(states)
			#state = states.pop(0)	
			#if state.isGoal():
			#	return state.timetable			
			state, cost = queue.get()
			#print(state.schedule)
			if state.isGoal():					
				return state.schedule

			visited.add(state)

			successors = state.generateSuccessors()
		
			for successor in successors:					
				if successor not in visited:		
				#print(successor.schedule)					
					queue.put((successor, successor.getCost()), successor.getCost())		
		return None

	class ScheduleState:
		def __init__(self, schedule, demographic_list, comedian_list, remaining, comedian_hours, per_day):
			self.schedule = schedule
			self.demo_list = demographic_list
			self.com_list = comedian_list
			self.cost = 0
			self.comedian_hours = comedian_hours
			self.remaining = remaining#[(demo, "main") for demo in self.demo_list] + [(demo, "test") for demo in self.demo_list]
			self.hours = {demographic.reference: {"main":500, "test":250} for demographic in self.demo_list}
			self.comedian_daily_hours = per_day
			

		def isGoal(self):
			# if not self.remaining:				
			# 	return True
			for day,slots in self.schedule.items():
				for slot, slot_info in slots.items():
					if not slot_info:
						#print(slot, slot_info)
						return False
			return True
		
		def generateSuccessors(self):			
			successors = []
			remaining = self.remaining.copy()# make a copy of the remaining list			
			
			
			#while remaining:
			demo, show = remaining.pop(0) # pop an element from the list
			for day, slots in self.schedule.items():									
				for slot, slot_info in slots.items():
					# if slot not empty
					if not slot_info:										
						for comedian in self.com_list:																	
							if self.canAssign(comedian, day, demo, show) and not (self.hasMain(demo) and show =="main") and not (self.hasTest(demo) and show =="test"):								
								new_schedule = self.deepcopy_dict(self.schedule)																			
								new_schedule[day][slot] = (comedian,demo,show)									
								#print(new_schedule)									
								new_comedian_hours = self.comedian_hours.copy()																	
								new_per_day = self.comedian_daily_hours.copy()										
								if show == "main":
									#print(new_comedian_hours)
									new_comedian_hours[comedian.name]["main"] +=2
									new_per_day[comedian.name][day] += 2 
								elif show == "test":
									new_comedian_hours[comedian.name]["test"] += 1
									new_per_day[comedian.name][day] +=1 
								new_state = Scheduler.ScheduleState(new_schedule, self.demo_list, self.com_list, remaining, new_comedian_hours, new_per_day)
								successors.append(new_state)	
								break
					 																	 												
			return successors

		def hasMain(self, demo):
			for day,slots in self.schedule.items():
				for slot, slot_info in slots.items():
					if slot_info:
						c,d,s = slot_info
						if d == demo and s == "main":
							return True
			return False
		
		def hasTest(self, demo):
			for day,slots in self.schedule.items():
				for slot, slot_info in slots.items():
					if slot_info:
						c,d,s = slot_info
						if d == demo and s == "test":
							return True
			return False

		def deepcopy_dict(self, dict_):
			return {key: value for key,value in dict_.items()}    		

		def canAssign(self, comedian, day, demo, show):								 
			
			if self.comedian_hours[comedian.name]["main"] + self.comedian_hours[comedian.name]["test"] >= 4:		
				return False			
			
			if show == "main" and self.comedian_daily_hours[comedian.name][day] >= 2:
				return False
			if show == "test" and self.comedian_daily_hours[comedian.name][day] >= 2:
				return False
        					
			if show == "main":					
				return all(topic in comedian.themes for topic in demo.topics)
			elif show == "test":
				return any(topic in comedian.themes for topic in demo.topics)	
			

		def getCost(self):
			self.cost = self.actualCost() + self.heuristicCost()	
			return self.cost		
		
		def actualCost(self):
			price = 0					
			for day,slots in self.schedule.items():				
				if slots is not None:					
					for slot, slot_info in slots.items():
						if slot_info:
							#print(slot_info)
							comedian, demo,show = slot_info
							if show == "main":
								price += 500
								if self.comedian_hours[comedian.name]["main"] == 2:
									price += 300
								elif self.comedian_hours[comedian.name]["main"] == 4:
									price += 100
							elif show == "test":
								price += 250 - 50 * self.comedian_hours[comedian.name]["test"] # test is 1 hours so basically a count
								if self.comedian_hours[comedian.name]["main"] > 0 or self.comedian_hours[comedian.name]["test"] > 0:
									price = price / 2
				else:
					price = 0
			return price

		def heuristicCost(self):
			num_per_day = len(self.schedule["Monday"])
			heuristic = 0
			for demo,show in self.remaining:
				remaining_shows = self.hours[demo.reference][show]
				heuristic += remaining_shows * num_per_day
			return heuristic

	class PriorityQueue:
		def __init__(self):
			self.items = []

		def put(self, item, priority):
			# Add the item to the list along with its priority
			self.items.append((priority, item))
			# Sort the list in ascending order by priority
			self.items.sort(key=lambda x: x[0])

		def get(self):
			# Return the item with the highest priority (lowest value)	
			x = self.items.pop(0)[1]
			#print(x)
			return x

		def empty(self):
			# Return True if the queue is empty, False otherwise
			return len(self.items) == 0
