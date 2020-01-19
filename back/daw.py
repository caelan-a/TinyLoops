from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import threading
import queue

# Signals
EXIT_SIGNAL = 'exit'
STOP_SIGNAL = 'stop'
ADD_LOOP_SIGNAL = 'add_loop'

class Signal:
	def __init__(self, signal_type, content):
		self.type = signal_type
		self.content = content

PEDAL = 'pedal'
CLEAR_SIGNAL = 'clear'

q = queue.Queue()
q_player = queue.Queue()


class AudioLoop:
	def __init__(self, path):
		self.playing = True;
		self.path = path;
		self.audio = AudioSegment.from_file(path)


class TinyDAW:
	def __init__(self, channels = 2, sample_rate = 44100, chunk_size = 1024,):
		self.channels = channels
		self.sample_rate = sample_rate
		self.chunk_size = chunk_size
		self.format = pyaudio.paInt16
		self.record = False
		self.recording_thread = None
		self.playback_thread = None
		self.loops = []

		self.startPlaybackThread()

	def exit(self):
		print("Dispose DAW")
		q_player.put(Signal(EXIT_SIGNAL, None))

	def getMixed(self, loopList):
		mixed = loopList[0].audio

		for i in range(1,len(loopList)):
			mixed = mixed.overlay(loopList[i].audio)

		return mixed

	def exportAudio(self, audio):
		audio.export("mixed.wav", format='wav') #export mixed  audio file

	def playback(self):
		print("Playback thread started")

		audioLoops = [];

		running = True
		while running:
			signal = q_player.get()
			if(signal.type == EXIT_SIGNAL):
				q_player.task_done()
				break
			elif(signal.type == ADD_LOOP_SIGNAL):
				print("Adding new audio loop")
				audioLoops.append(AudioLoop(signal.content))
				mixed = self.getMixed(audioLoops)
				play(mixed)
				q_player.task_done()
			elif(signal.type == CLEAR_SIGNAL):
				print("Clearing loops")
				audioLoops = []

		print("Stopping playback")

	def record_audio(self, path):	
		pyaudio_inst = pyaudio.PyAudio()

		WAVE_OUTPUT_FILENAME = path
		stream = pyaudio_inst.open(format=self.format,
		                channels=self.channels,
		                rate=self.sample_rate,
		                input=True,
		                frames_per_buffer=self.chunk_size)

		print("Recording")

		frames = []

		running = True
		while running == True:
			if(q.empty() == False):
				stop_recording_signal = q.get()
				if(stop_recording_signal == 'stop'):
					# q.put('stopped')
					running = False
					break;
				else:
					print("Unknown signal")
			data = stream.read(self.chunk_size)
			frames.append(data)

		print("Done recording")

		stream.stop_stream()
		stream.close()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(pyaudio_inst.get_sample_size(self.format))
		wf.setframerate(self.sample_rate)
		wf.writeframes(b''.join(frames))
		wf.close()

		pyaudio_inst.terminate()

		self.recording = False;
		print("Thread finished")
		q.task_done()

	def startPlaybackThread(self):
		self.playback_thread = threading.Thread(target=self.playback)
		self.playback_thread.daemon = True
		self.playback_thread.start()

	def isPlaying(self):
		off = self.playback_thread == None or self.playback_thread.isAlive() == False
		return off != True

	def isRecording(self):
		off = self.recording_thread == None or self.recording_thread.isAlive() == False
		return off != True

	def getNextAudioPath(self):
		return 'sounds/' + str(len(self.loops) + 1) + '.wav'
	
	def addAudioLoop(self, path):
		self.loops.append(path)
		q_player.put(Signal(ADD_LOOP_SIGNAL, path))
	
	def receiveInput(self, input_signal):
		if(input_signal==PEDAL):
			if(self.record):
				print("Command: Stop recording")
				self.record = False
				q.put('stop')
				q.join()
				self.addAudioLoop(self.getNextAudioPath())
			else:
				print("Command: Start recording")
				if(self.isRecording() is False):
					self.record = True
					self.recording_thread = threading.Thread(target=self.record_audio, args=[self.getNextAudioPath()])
					self.recording_thread.start()
		if(input_signal == CLEAR_SIGNAL):
			self.loops = []
			q_player.put(Signal(CLEAR_SIGNAL, None))