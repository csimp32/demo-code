#!/usr/bin/python

# Import all the bits
import base64
import time
import mysql.connector
import csv
from sys import argv

# Declare vairables for DB connection
hostname = 'db'
username = 'user'
# tsk tsk
password = base64.b64decode('cGFzc3dvcmQK')
database = 'database'

# Verify existance of arguments
if len(argv) < 4:
    print "Please provide day, month, and year that you wish to run the report on in DD MM YYYY format."
    exit()

# Function to take user input as command line arguments for which day to pull data for and perform the query.
# The results of the query will be returned in the 'query_array' object.

def doQuery(conn):
    # Create the cursor object
    cur = conn.cursor()

    # Get command line arguments
    day = argv[1]
    month = argv[2]
    year = argv[3]

    # Build the query using the user defined data
    query = "SELECT rTicketID,UNIX_TIMESTAMP(rTime),UNIX_TIMESTAMP(sTime),UNIX_TIMESTAMP(eTime),user,action,ticket.ticketID FROM ticket_log \
		LEFT JOIN ticket ON ticket_log.ticketID = ticket.ticketID \
		WHERE sTime LIKE '" + year + "-" + month + "-" + day + "%' \
		AND action='OPEN' \
		OR sTime LIKE '" + year + "-" + month + "-" + day + "%' \
		AND action='UPDATE' \
		OR sTime LIKE '" + year + "-" + month + "-" + day + "%' \
		AND action='RESOLVE' \
		ORDER BY action"

    # Perform the query
    cur.execute(query)

    # Populate the array using the results of the query
    query_array = cur.fetchall()

    # Return the results to the main function
    return query_array


# Create the connection object
myConnection = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
# Call the query function
results = doQuery(myConnection)
# You have to be sure to close the connection
myConnection.close()

# Define the handy variables
max_hold = 0
i = 0
hold = 0
total = 0
avg = 0
longs = []

# Loop to process the results
for row in results:
    # Eliminate the NULL values that exist in the 4th column of some results when the transaction hasn't completed
    if row[3]:
        # Determine the trasaction time for each row
        hold = row[3] - row[1]
        # Running sum to be used for mean calculation
        total += hold

        # Trying to find the longest transaction
        if hold > max_hold:
            max_hold = hold
            max_results = row

        # Count how many transactions exceedeed 5 minutes
        if hold > 300:
            longs.append(row[0])
    # Increment index variable
    i = i + 1

# Calculate average transaction time
avg = float(total) / len(results)

# Output the findings
print "There were a total of {0} measured transactions.".format(i)
print "The average transaction time was {0} seconds.".format(avg)
print "{0} transaction(s) took longer than 5 minutes.".format(len(longs))
print "The longest transaction time was {0} seconds for {1} performing {2} action on radar ticket {3}".format(
    max_hold, max_results[4], max_results[5], max_results[0])

# Output the full results from the query
heading = ["Radar Ticket", "Request Time", "Start Time",
           "End Time", "User", "Action", "eBonding ID", "Transaction Time"]
print "\n\n{0:^15} {1:^15} {2:^15} {3:^15} {4:^30} {5:^10} {6:^15} {7:^15}\n".format(*heading)

new_results = []
# Add heading to new array
new_results.append(heading)

for row in results:
    new_row = []
    for entry in row:
        # Find date entries and convert from epoch to human readable
        if row.index(entry) > 0 and row.index(entry) < 4 and entry:
            new_row.append(time.strftime("%Z - %H:%M:%S", time.localtime(entry)))
        else:
            new_row.append(entry)
    # Calculate transaction time and add to last column of array only if the transaction has a completion time
    if row[3]:
        trans_time = row[3] - row[1]
        new_row.append(trans_time)
    else:
        new_row.append("NA")
    # Print the columns and add to new results array
    print "{0:^15} {1:^15} {2:^15} {3:^15} {4:^30} {5:^10} {6:^15} {7:^15}".format(*new_row)
    new_results.append(new_row)

# Create CSV file
write_file = "new_file.csv"
with open(write_file, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(new_results)
