import time
import xbmc
import xbmcaddon
import xbmcgui
import os
import xbmcvfs
from downloader import *

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
CWD = addon.getAddonInfo('path') # for kodi 19 and up..


phd=os.path.join('special://userdata//lio2023')
codePath=phd+"//code.txt"
if not os.path.exists(phd):
	xbmcvfs.mkdir(phd)
	f=xbmcvfs.File(codePath,'w')
	f.write("0000".encode("utf-8"))
	f.close()



usrPtd=phd+"//users.txt"
#userUrl="https://public.db.files.1drv.com/y4mWcij-R_1AVnsV3_l6Zi_Q8Ml4qcBva452X0zy6x7U-svBbwR00bw_9xq1wVTGdZkVJvfZYl2J2taaU_2ap1oP00PCqm46z6hNiSbR1HrE3uCyNsoufU0Ws44R6hO-0gkiwgzCgJnkBGL6cRyduYG6t-cRMQ2LEyAbUUddsOc9_8kh3_exKeuKm3h8Bq2hCEklwIVQjHis7vbTeo0Kh0adP968YLHpMrfN2iScYQ5mGE?AVOverride=1"
userUrl="https://raw.githubusercontent.com/lfrenteriax/kodiaddon/main/users.txt"
chnUrl="https://raw.githubusercontent.com/lfrenteriax/channels/master/lio2023"
chnPtd=phd+"//lio2023.m3u"
teleUrl='https://tv.teleclub.xyz/activar'
data = "submit=ACTIVAR%2BAHORA";
headers= { 'Content-Type': 'application/x-www-form-urlencoded','referer': 'https://tv.teleclub.xyz/activar'}
def debug(msg):

	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	label = xbmcgui.ControlLabel(1200, 20, 100, 50, msg,
                                            font='font24_title', textColor='0xFFFFFF00')
	window.addControl(label)

def isActivado(code,usr):
		f=xbmcvfs.File(code,'r')
		code=f.read()
		f.close()
		f=xbmcvfs.File(usr,'r')
		usr=f.read()
		f.close()
		
		if(usr.split('\n').count(code)):
			return 1
		else:
			return 0
def main():
	monitor = xbmc.Monitor()
	nAtime=20
	aTime=3600
	showOk=False
	timeToWait=nAtime
	download(chnUrl,chnPtd)
	xbmcgui.Dialog().ok("inicio", "Presione para continuar")

	while not monitor.abortRequested():
		# Sleep/wait for abort for 10 seconds
		if monitor.waitForAbort(timeToWait):
			# Abort was requested while waiting. We should exit
			
			break
		
		timeToWait=timeToWait-1
		debug(str(timeToWait))
		if timeToWait<10:
			timeToWait=nAtime
		
		if 1:
		#try:
			download(userUrl,usrPtd)
			
			if not isActivado(codePath,usrPtd):
				f=xbmcvfs.File(chnPtd,'w')
				f.write("".encode("utf-8"))
				f.close()
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
