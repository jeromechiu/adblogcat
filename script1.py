import queue
import subprocess
import threading
import datetime
import time

class AsynchronousFileReader(threading.Thread):
	'''
	Helper class to implement asynchronous reading of a file
	in a separate thread. Pushes read lines on a queue to
	be consumed in another thread.
	'''

	def __init__(self, fd, q):
		assert isinstance(q, queue.Queue)
		assert callable(fd.readline)
		threading.Thread.__init__(self)
		self._fd = fd
		self._queue = q

	def run(self):
		'''The body of the tread: read lines and put them on the queue.'''
		for line in iter(self._fd.readline, ''):
			self._queue.put(line)

	def eof(self):
		'''Check whether there is no more content to expect.'''
		return not self.is_alive() and self._queue.empty()

def substring_matches_line(line):
	target_substring = "Foo"
	return target_substring.encode('UTF-8') in line

# You'll need to add any command line arguments here.
subprocess.run(['C:\\Users\\chiuk\\Desktop\\adb\\adb.exe', 'logcat', '-c'])
process = subprocess.Popen(['C:\\Users\\chiuk\\Desktop\\adb\\adb.exe', 'logcat'], stdout=subprocess.PIPE)

# Launch the asynchronous readers of the process' stdout.
stdout_queue = queue.Queue()
stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
stdout_reader.start()


# Check the queues if we received some output (until there is nothing more to get).
still_looking = True
try:
	filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.txt'
	f=open(filename,'a')
	start = time.time()
	print("Open file: %s" %filename)
	while True:
		
		if time.time() - start < 300:
			while still_looking and not stdout_reader.eof():
				while not stdout_queue.empty():
					line = stdout_queue.get()
					l = str(line)+'\n'
					#print(l)
					
					f.write(str(l))
					# if substring_matches_line(line):
						# print ("Hoorah, I found it! " + str(datetime.datetime.now()))
						# print (line)
						# still_looking = False
						# break
		else:
			f.close()
			
			process.kill()
			subprocess.run(['C:\\Users\\chiuk\\Desktop\\adb\\adb.exe', 'logcat', '-c'])
			
			# You'll need to add any command line arguments here.
			process = subprocess.Popen(['C:\\Users\\chiuk\\Desktop\\adb\\adb.exe', 'logcat'], stdout=subprocess.PIPE)

			# Launch the asynchronous readers of the process' stdout.
			stdout_queue = queue.Queue()
			stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
			stdout_reader.start()

			
			filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.txt'
			f=open(filename,'a')
			start = time.time()
			print("Open file: %s" %filename)
finally:
	process.kill()
	f.close()
