#el_meu_util
import psutil

def running_process():
	processos = ''
	
	for proc in psutil.process_iter():
		try:
			# Get process name & pid from process object.
			processName = proc.name()
			processID = proc.pid
			processos = processos + processName + ' ::: ' + str(processID) + '<br/>'
			return processos
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return processos