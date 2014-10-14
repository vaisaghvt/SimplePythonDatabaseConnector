#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Vaisagh Viswanathan"
__version__ = "0.1"

import psycopg2
import sys
import matplotlib.pyplot as plt


class DatabaseHandler:

	def __init__(self, config_parameters):
		'''
			Initializes a database handler with the passed parameters. It should contain dbname, user, host and password.
			If any of these parameters are not provided an error is thrown.
		'''
		self.config_parameters = config_parameters
		self.con = None
		assert "dbname" in self.config_parameters and "user" in self.config_parameters and "host" in self.config_parameters and "password" in self.config_parameters
		
	
	def connect_to_database(self):
		'''
			Connects to a database and initializes the cursor. which is subsequently used by run_sql_statement
		'''
		try:
		    con = psycopg2.connect("dbname='{dbname}' user='{username}' host='{host}' password='{password}'".format(
		    	host=self.config_parameters["host"],
		    	username=self.config_parameters["user"],
		    	password=self.config_parameters["password"],
		    	dbname=self.config_parameters["dbname"]))
		    cur = con.cursor()
		    cur.execute('SELECT version()')          
		    self.cursor = cur
		    ver = cur.fetchone()
		    return {"success":True, "message":ver}    
		    
		except psycopg2.DatabaseError as e:
		    return {"success":False, "message":'Error {0}'.format(e)}    

	def run_sql_statement(self, squery):
		'''
			Returns a list of rows that are a result of the run query.
		'''
		self.cursor.execute(squery)
		rows = self.cursor.fetchall()
		return rows
		

	def close_connection(self):    	    
		'''
			Closes the connection. This should always be called without fail.
		'''
		if self.con:
			con.close()



  

def plot_graph_template():
	fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	FONT_SIZE = 20

	## Here you will have to read the data in whatever you want from the database using
	## db_handler.run_sql_statement. The result can then be formatted to get an array of mean_values
	## and an array of error values which can then be plotted by simply running this command.
	x_array= [0.10,0.20,0.30]
	y_array= [10,20,30]
	y_err = [1,2,1]

	x_array_1= [0.10,0.20,0.30, 0.4, 0.5]
	y_array_1= [10,40,50,80,70]
	y_err_1 = [1,2,1,10,2]

	ax.errorbar(x_array, y_array, yerr=y_err, label="Some graph")
	ax.errorbar(x_array_1, y_array_1, yerr=y_err_1, label="Other graph")

	##Set the title for the graph
	ax.set_title("Title of the graph", size=FONT_SIZE)

	##Set the x and y axis template
	ax.set_xlabel('X Axis Label', size=FONT_SIZE)
	ax.set_ylabel('Y Axis Label', size=FONT_SIZE)

	## Setting the ticks on x and y axis. This is not necessary since it will be calculated from the
	## range of values in the respective axis. But if you want to customize it, this is how you do it.

	# plt.xticks(np.arange(0,101,10), size=FONT_SIZE)
	# plt.yticks(np.arange(0,101,10), size=FONT_SIZE)

	##Sets the bounds of the x and y axis. This you will most probably want to do in every case.
	ax.set_ybound(lower=0, upper=100)
	ax.set_xbound(lower=0.0, upper= 1.0)

	## If you have multiple error bars plotted in the graph, the labes are obtained automatically for 
	## these graphs. I don't think this is necessary. But keeping it there for now. Can experiment with 
	## it later.
	# handles, labels = ax.get_legend_handles_labels()
	# ax.legend(handles[::-1], labels[::-1]) ## reverses the order.
	plt.legend(loc="upper right", fontsize=FONT_SIZE)

	## This saves the file in that file. 
	# plt.savefig("FileName.png", pad_inches=0)

	## If you simply want to show the file and not save it, then you should do a plt.show(). When figure 
	## is shown there is an option to save it in the window that opens.
	plt.show()

	# Should be done always.
	plt.close()





def get_dict_from_file(fileName):
	'''
		Returns a dict of values from a passed file
	'''
	params = {}
	with open(fileName) as config_file:
		for line in config_file:

			parts= line.split(":")
			if len(parts)>1:
				key = parts[0].strip()
				value = parts[1].strip()
				params[key] = value
				# print(line)
	
	return params

def main():
	'''
		An example of how to connect to database and run a query on it.
		This doesn't have to be used. However, advisable to follow this 
		structure.
	'''
	connection_params = get_dict_from_file('config')
	db_handler = DatabaseHandler(connection_params)
	result = db_handler.connect_to_database()
	if result["success"]:
		try:
			# print(result["message"])
			rows = db_handler.run_sql_statement("""select * from performance_table LIMIT 5""")
			for row in rows:
				print(row[2])

			plot_graph_template()

			

		except psycopg2.DatabaseError as e:
		    print('Error {0}'.format(e))   
		
		finally:
			db_handler.close_connection() 



if __name__ == "__main__":
    main()

    