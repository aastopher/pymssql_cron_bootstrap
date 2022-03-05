import pandas as pd
from datetime import date
import os
import subprocess
from subprocess import PIPE, CalledProcessError, Popen

from modules.setup import *
from modules.connection import *

# Instantiate loggers
DL = DeepLogger('process',['query','logic','clean','export'])
queryLogger = DL.getLogger('query')
logicLogger = DL.getLogger('logic')
cleanLogger = DL.getLogger('clean')
exportLogger = DL.getLogger('export')
infoLogger = DL.getLogger('console')

def process():
	try:
		exportLogger.info('attempting process...')
		try:
			queryLogger.info('initializing variables for query')
			#Initialize date and version variables
			today = date.today()
			today = today.strftime("%m-%d-%Y")
			now = datetime.datetime.now()
			now = now.strftime("%Y-%m-%d_%H-%M-%S")
			query_version = '1'

			queryLogger.info('SUCCESSFUL initializing variables')
		except Exception as e:
			queryLogger.info(f'FAILED initializing variables: {e}')
			exit(1)

		#PROCESS QUERY
		try:
			queryLogger.info('attempting to run query...')
			#Query to be run
			cursor.execute(f'''
			SELECT *
			FROM base_table
			''')
			#Convert query output to list of lists
			recordList = [list(r) for r in cursor.fetchall()]

			queryLogger.info('SUCCESSFUL query fetch')
		except Exception as e:
			queryLogger.info(f'FAILED query fetch: {e}')
			print(f'FAILED query fetch: {e}')
			exit(1)

		# PROCESS LOGIC
		try:
			logicLogger.info('attempting process logic...')
			# Additional procces logic HERE
			logicLogger.info('SUCCESSFUL process logic')
		except Exception as e:
			logicLogger.info(f'FAILED process logic: {e}')
			print(f'FAILED process logic: {e}')
			exit(1)

		# CLEAN UP
		try:
			cleanLogger.info('attempting clean up...')
			# Clean up remaining anomalies
			cleanLogger.info('SUCCESSFUL clean up')
		except Exception as e:
			cleanLogger.info(f'FAILED clean up: {e}')
			print(f'FAILED clean up: {e}')
			exit(1)

		# SET DIRECTORIES & EXPORT
		### WARNING: REMOVE BLOCK if network drive is not applicable! ###
		try:
			exportLogger.info('attempting to mount network drive...')
			if not os.path.isdir('/mnt/r'):
				os.system("sudo mkdir /mnt/r")
			try:
				df = Popen(['sudo mount -t drvfs R: /mnt/r'], stdout=PIPE, shell=True)
				output, err = df.communicate()
			except CalledProcessError as e:
				exportLogger.info(f'FAILED network drive mount: {e}')
				print(f'FAILED network drive mount: {e}')
				exit(1)
			exportLogger.info(f'SUCCESSFUL network drive mount')
		except OSError as e:
			exportLogger.info(f'FAILED network drive mount: {e}')
			print(f'FAILED network drive mount: {e}')
			exit(1)
		### WARNING: REMOVE BLOCK if network drive is not applicable! ###

		try:
			exportLogger.info('attempting to write file...')
			# Write excel file to end location
			if os.path.isdir('/mnt/r'): # MAKE SURE CHANGE LOCATION!
				# To change path alter the following command
				W.to_excel(writer,sheet_name=f'SC_v{query_version}_{today}', index=False, na_rep='NaN', engine='xlsxwriter')

				# Auto-adjust columns' width
				for column in W:
				    column_width = max(W[column].astype(str).map(len).max(), len(column))
				    col_idx = W.columns.get_loc(column)
				    writer.sheets[f'OUTPUT_v{query_version}_{today}'].set_column(col_idx, col_idx, column_width)
				writer.close()
			exportLogger.info('SUCCESSFUL file write')
		except Exception as e:
			exportLogger.info(f'FAILED file write: {e}')
			print(f'FAILED file write: {e}')
			exit(1)
		exportLogger.info('SUCCESSFUL process!')
		print(f'script ran SUCCESSFULLY! - {now}')
	except Exception as e:
		exportLogger.info(f'FAILED process: {e}')
		print(f'script FAILED to run, please check logs - {now}')

process()
