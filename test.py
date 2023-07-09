import time
import xbmc
import xbmcaddon
import xbmcgui
import os
import xbmcvfs
from contextlib import closing
from xbmcvfs import File

from downloader import *



def upateTv(path):
	f=xbmcvfs.File(path,'r')
	data=f.read()
	f.close()
	import re
	pat = r'.*?id="m3uPath">(.*)</setting>.*'             #See Note at the bottom of the answer
	match = re.search(pat, data)
	data=data.replace(match.group(1),chnPtd)
	f=xbmcvfs.File(path,'w')
	f.write(data)
	f.close()

def readFile(path):
	
	with closing(File(path)) as fo:
		text = fo.read()
		
	return text

def listFiles(path):
	dirs, files = xbmcvfs.listdir(path)
	data=""
	for file in files:
		data=data+file+"\n"
	xbmcgui.Dialog().ok(path,data)

def debug(msg):

	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	label = xbmcgui.ControlLabel(1200, 20, 100, 50, msg,
                                            font='font24_title', textColor='0xFFFFFF00')
	window.addControl(label)




def isActivado(cdP,usrP):

		f=xbmcvfs.File(usrP,'r')
		usuarios=f.read()
		f.close()
		#xbmcgui.Dialog().ok("users",usuarios)
		f1=xbmcvfs.File(cdP,'r')
		codigo=f1.read()
		f1.close()
		#xbmcgui.Dialog().ok("codigo", codigo)
		if(usuarios.split('\n').count(codigo)):
			return 1
		else:
			return 0











addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
CWD = addon.getAddonInfo('path') # for kodi 19 and up..


phd=os.path.join('special://userdata//lio2023')
#usrPtd=os.path.join('special://userdata//lio2023//users.txt')

phdTv=os.path.join('special://userdata//addon_data//pvr.iptvsimple//instance-settings-1.xml')
codePath=phd+"//code.txt"
usrPtd=phd+"//users.txt"
cd=readFile(codePath)
#xbmcgui.Dialog().ok("Cd",cd)

if not cd :
	#xbmcgui.Dialog().ok("Creando directorio",phd)
	xbmcvfs.mkdir(phd)
	f=xbmcvfs.File(codePath,'w')
	f.write("0000".encode("utf-8"))
	f.close()



#usrPtd=phd+"//users.txt"
#userUrl="https://public.db.files.1drv.com/y4mWcij-R_1AVnsV3_l6Zi_Q8Ml4qcBva452X0zy6x7U-svBbwR00bw_9xq1wVTGdZkVJvfZYl2J2taaU_2ap1oP00PCqm46z6hNiSbR1HrE3uCyNsoufU0Ws44R6hO-0gkiwgzCgJnkBGL6cRyduYG6t-cRMQ2LEyAbUUddsOc9_8kh3_exKeuKm3h8Bq2hCEklwIVQjHis7vbTeo0Kh0adP968YLHpMrfN2iScYQ5mGE?AVOverride=1"
userUrl="https://raw.githubusercontent.com/lfrenteriax/kodiaddon/main/users.txt"
chnUrl="https://raw.githubusercontent.com/lfrenteriax/channels/master/lio2023"
chnPtd=phd+"//lio2023.m3u"
teleUrl='https://tv.teleclub.xyz/activar'
data = "submit=ACTIVAR%2BAHORA";
headers= { 'Content-Type': 'application/x-www-form-urlencoded','referer': 'https://tv.teleclub.xyz/activar'}


#listFiles(phd)

#listFiles(phdTv)
#readFile(usrPtd)
#isActivado(codePath,usrPtd)
#readFile(codePath)
def main():
	monitor = xbmc.Monitor()
	nAtime=5
	aTime=3600
	showOk=False
	timeToWait=nAtime
	download(chnUrl,chnPtd)
	download(userUrl,usrPtd)
		
	#xbmcgui.Dialog().ok("inicio", "Presione para continuar")
	while not monitor.abortRequested():
		# Sleep/wait for abort for 10 seconds
		if monitor.waitForAbort(timeToWait):
			# Abort was requested while waiting. We should exit
			
			break
		#readFile(usrPtd)
		#timeToWait=timeToWait-1
		debug(str(timeToWait))
		if timeToWait<10:
			timeToWait=nAtime
		upateTv(phdTv)
		if 1:
		#try:
			if not isActivado(codePath,usrPtd):
				ret = xbmcgui.Dialog().yesno('NO ACTIVADO', 'Quieres activarlos ahora?')
				if ret:
					d = xbmcgui.Dialog().numeric(0, 'Ingrese el codigo de activaciòn')
					xbmcgui.Dialog().ok("Activando", "Codigo de activacion:"+str(d)+"\n Activar en: "+str(timeToWait)+"s")
					f=File(codePath, 'wb')
					f.write(str(d).encode("utf-8"))
					f.close()
					showOk=True
			else:
				resp=urlReqPost(teleUrl,headers,data)
				timeToWait=aTime
				if showOk: 
					xbmcgui.Dialog().ok("ACTIVADO", "Presione para continuar")
					showOk=False
			#xbmc.executebuiltin('RunScript(pvr.iptvsimple)')
		#except  Exception as e:
		#	xbmcgui.Dialog().ok("Codigo", str(e))

	pass
if __name__ == '__main__':
	main()	
