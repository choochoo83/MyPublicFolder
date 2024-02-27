import sys, os, time, re, os.path, subprocess
sys.path.append(r'C:\Users\Public\Documents\LeCroy\Net Protocol Suite\API\SDK\Bin')
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
os.system("cls")

offline_installation = "No"
online_installation = "No"
offline_installer = ""
online_installer = ""
installer_option = ""
installation_option = ""
uninstall_option = ""
upgrade_option = ""

def default_install(dir_installer):
	process = subprocess.Popen([dir_installer, 'in', '-c', '--am', '--al'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	while process.returncode != 0:
		print("")

def full_install(dir_installer):
	process = subprocess.Popen([dir_installer, 'in', 'component.SierraNetM168Support', 'component.SierraNetM408Support', 'component.SierraNetT328Support', 'component.SierraNetM328Support', 'component.SierraNetM328QSupport', 'component.SierraNetM648Support', 'component.SierraNetM1288Support', '-c', '--am', '--al'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	while process.returncode != 0:
		print("")

# def uninstall():
	# process = subprocess.Popen(['maintenancetool.exe', 'pr', '-c', '--da'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# stdout, stderr = process.communicate()
	# while process.returncode != 0:
		# print("")

def mandatory_component_checking():
	if os.path.exists("C:\\Program Files\\LeCroy\\Net Protocol Suite\\Windows\\Bin\\GIGE.exe"):
		print("Checkpoint[1] The Net software is installed \t\t" + Fore.GREEN + "Passed" + Fore.RESET) 
	else:
		print("Checkpoint[1] The Net software is installed \t\t" + Fore.RED + "Failed" + Fore.RESET) 
	if os.path.exists("C:\\Program Files\\LeCroy\\LinkExpert\\LinkExpert.exe"):
		print("Checkpoint[2] The Link Expert is installed \t\t" + Fore.GREEN + "Passed" + Fore.RESET) 
	else:
		print("Checkpoint[2] The Link Expert is installed \t\t" + Fore.RED + "Failed" + Fore.RESET) 
	if os.path.exists("C:\\Program Files (x86)\\Common Files\\LeCroy Shared\\PSGSyncAgent.exe"):
		print("Checkpoint[3] The CrossSync is installed \t\t" + Fore.GREEN + "Passed" + Fore.RESET) 
	else:
		print("Checkpoint[3] The CrossSync is installed \t\t" + Fore.RED + "Failed" + Fore.RESET) 
	if os.path.exists("C:\\Program Files\\LeCroy\\Net Protocol Suite\\Documents\\"):
		print("Checkpoint[4] The Net document is installed \t\t" + Fore.GREEN + "Passed" + Fore.RESET) 
	else:
		print("Checkpoint[4] The Net document is installed \t\t" + Fore.RED + "Failed" + Fore.RESET) 
	NET_version = ""
	LEX_version = ""
	CS_version = ""
	for line in open ("C:\\Program Files\\LeCroy\\Net Protocol Suite\\InstallationLog.txt"):
		if re.search("arguments: installer://component.Net/", line) and re.search("content.zip", line):
			NET_version = line.split("component.Net/")[1].split("content.zip")[0]
		if re.search("arguments: installer://component.LinkExpert/", line) and re.search("content.zip", line):
			LEX_version = line.split("component.LinkExpert/")[1].split("content.zip")[0]
		if re.search("arguments: installer://component.CrossSync/", line) and re.search("content.zip", line):
			CS_version = line.split("component.CrossSync/")[1].split("content.zip")[0]
	# installed_version = TLNetAPI.GetVersion().split(".")[-1]
	if NET_version != "":
		print("Checkpoint[5] The installed Net software version \t" + Fore.GREEN + NET_version + Fore.RESET)
	else:
		print("Checkpoint[5] The installed Net software version \t" + Fore.RED + "Failed" + Fore.RESET)
	if LEX_version != "":
		print("Checkpoint[6] The installed Link Expert version \t" + Fore.GREEN + LEX_version + Fore.RESET)
	else:
		print("Checkpoint[6] The installed Link Expert version \t" + Fore.RED + "Failed" + Fore.RESET)
	if CS_version != "":
		print("Checkpoint[7] The installed CrossSync version \t\t" + Fore.GREEN + CS_version + Fore.RESET)
	else:
		print("Checkpoint[7] The installed CrossSync version \t\t" + Fore.RED + "Failed" + Fore.RESET)

def optional_component_checking():
	bin_file = 0
	for files in os.listdir("C:\\Users\\Public\\Documents\\LeCroy\\Net Protocol Suite\\SupportFiles\\Hardware\\"):
		if re.search("M168_", files) or re.search("M328_", files) or re.search("M328Q_", files) or re.search("M408_", files) or re.search("M648_", files) or re.search("M1288_", files) or re.search("T328_", files):
			bin_file += 1
	if bin_file == 76:
		print("Checkpoint[8] The installed optional components \t" + Fore.GREEN + "Passed" + Fore.RESET)
	else:
		print("Checkpoint[8] The installed optional components \t" + Fore.RED + "Failed" + Fore.RESET)

the_latest_build = 0
new_build = 0
for files in os.listdir(os.getcwd() + "\\"):
	if re.search("NetSuiteSW", files) and re.search("exe", files):
		if re.search("BETA", files):
			check_build = files.split("_BETA")[0].split("_B")[1]
			new_build = int(check_build)
		elif re.search("line", files):
			check_build = files.split("_B")[1].split("_")[0]
			new_build = int(check_build)
		elif re.search("ALPHA", files):
			check_build = files.split("_B")[1].split("_")[0]
			new_build = int(check_build)
		else:
			check_build = files.split("_B")[1].split(".exe")[0]
			new_build = int(check_build)
	if new_build > the_latest_build:
		the_latest_build = new_build

for files in os.listdir(os.getcwd() + "\\"):
	if re.search("NetSuite", files) and re.search(str(the_latest_build), files) and re.search("online.exe", files):
		online_installation = "Yes"
		online_installer = files
	elif re.search("NetSuite", files) and re.search(str(the_latest_build), files) and re.search("offline.exe", files):
		offline_installation = "Yes"
		offline_installer = files

my_dir = os.getcwd()
while os.path.exists("C:\\Program Files\\LeCroy\\Net Protocol Suite\\Windows\\Bin\\GIGE.exe") == 1:
	import TLNetAPI
	currently_installed_build = int(TLNetAPI.GetVersion().split(".")[-1])
	if the_latest_build <= currently_installed_build:
		print("The latest build of Net software is already installed (" + str(currently_installed_build) + ")")
		break
	else:
		print(Fore.YELLOW + "A newer build " + str(the_latest_build) + " is found than the currently installed build " + str(currently_installed_build) + Fore.RESET)
		upgrade_option = input("Do you want to perform an upgrade installation to the latest build? (1: Yes / 2: No) >> ")
		if upgrade_option == "1":
			os.chdir(my_dir)
			if online_installation == "Yes" and offline_installation == "Yes":
				for files in os.listdir(os.getcwd() + "\\"):
					if re.search("NetSuiteSW", files) and re.search(".exe", files):
						if files == online_installer or files == offline_installer:
							print(Back.YELLOW + files + Back.RESET)
						else:
							print(files)
				installer_option = input("Please select the installer (1: Online / 2: Offline) >> ")
				installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
				print(Fore.YELLOW + "Installing..." + Fore.RESET)
				if installer_option == "1":
					if installation_option == "1":
						default_install(os.getcwd() + "//" + online_installer)
						mandatory_component_checking()
						break
					elif installation_option == "2":
						full_install(os.getcwd() + "//" + online_installer)
						mandatory_component_checking()
						optional_component_checking()
						break
					else:
						break
				elif installer_option == "2":
					if installation_option == "1":
						default_install(os.getcwd() + "//" + offline_installer)
						mandatory_component_checking()
						break
					elif installation_option == "2":
						full_install(os.getcwd() + "//" + offline_installer)
						mandatory_component_checking()
						optional_component_checking()
						break
					else:
						break
				else:
					break

			elif online_installation == "Yes" and offline_installation == "No":
				for files in os.listdir(os.getcwd() + "\\"):
					if re.search("NetSuiteSW", files) and re.search(".exe", files):
						if files == online_installer:
							print(Back.YELLOW + files + Back.RESET)
						else:
							print(files)
				installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
				print(Fore.YELLOW + "Installing..." + Fore.RESET)
				if installation_option == "1":
					default_install(os.getcwd() + "//" + online_installer)
					mandatory_component_checking()
					break
				elif installation_option == "2":
					full_install(os.getcwd() + "//" + online_installer)
					mandatory_component_checking()
					optional_component_checking()
					break
				else:
					break

			elif online_installation == "No" and offline_installation == "Yes":
				for files in os.listdir(os.getcwd() + "\\"):
					if re.search("NetSuiteSW", files) and re.search(".exe", files):
						if files == offline_installer:
							print(Back.YELLOW + files + Back.RESET)
						else:
							print(files)
				installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
				print(Fore.YELLOW + "Installing..." + Fore.RESET)
				if installation_option == "1":
					default_install(os.getcwd() + "//" + offline_installer)
					mandatory_component_checking()
					break
				elif installation_option == "2":
					full_install(os.getcwd() + "//" + offline_installer)
					mandatory_component_checking()
					optional_component_checking()
					break
				else:
					break
			
			else:
				print(Back.RED + "No available installer is found" + Back.RESET)
				break
		else:
			break

while os.path.exists("C:\\Program Files\\LeCroy\\Net Protocol Suite\\Windows\\Bin\\GIGE.exe") == 0:
	print(Fore.YELLOW + "No Net software is installed on the system" + Fore.RESET)
	os.chdir(my_dir)
	if online_installation == "Yes" and offline_installation == "Yes":
		for files in os.listdir(os.getcwd() + "\\"):
			if re.search("NetSuiteSW", files) and re.search(".exe", files):
				if files == online_installer or files == offline_installer:
					print(Back.YELLOW + files + Back.RESET)
				else:
					print(files)
		installer_option = input("Please select the installer (1: Online / 2: Offline) >> ")
		installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
		print(Fore.YELLOW + "Installing..." + Fore.RESET)
		if installer_option == "1":
			if installation_option == "1":
				default_install(os.getcwd() + "//" + online_installer)
				mandatory_component_checking()
				break
			elif installation_option == "2":
				full_install(os.getcwd() + "//" + online_installer)
				mandatory_component_checking()
				optional_component_checking()
				break
			else:
				break
		elif installer_option == "2":
			if installation_option == "1":
				default_install(os.getcwd() + "//" + offline_installer)
				mandatory_component_checking()
				break
			elif installation_option == "2":
				full_install(os.getcwd() + "//" + offline_installer)
				mandatory_component_checking()
				optional_component_checking()
				break
			else:
				break
		else:
			break

	elif online_installation == "Yes" and offline_installation == "No":
		for files in os.listdir(os.getcwd() + "\\"):
			if re.search("NetSuiteSW", files) and re.search(".exe", files):
				if files == online_installer:
					print(Back.YELLOW + files + Back.RESET)
				else:
					print(files)
		installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
		print(Fore.YELLOW + "Installing..." + Fore.RESET)
		if installation_option == "1":
			default_install(os.getcwd() + "//" + online_installer)
			mandatory_component_checking()
			break
		elif installation_option == "2":
			full_install(os.getcwd() + "//" + online_installer)
			mandatory_component_checking()
			optional_component_checking()
			break
		else:
			break

	elif online_installation == "No" and offline_installation == "Yes":
		for files in os.listdir(os.getcwd() + "\\"):
			if re.search("NetSuiteSW", files) and re.search(".exe", files):
				if files == offline_installer:
					print(Back.YELLOW + files + Back.RESET)
				else:
					print(files)
		installation_option = input("Please select the installation (1: Mandatory components / 2: Full components) >> ")
		print(Fore.YELLOW + "Installing..." + Fore.RESET)
		if installation_option == "1":
			default_install(os.getcwd() + "//" + offline_installer)
			mandatory_component_checking()
			break
		elif installation_option == "2":
			full_install(os.getcwd() + "//" + offline_installer)
			mandatory_component_checking()
			optional_component_checking()
			break
		else:
			break
	
	else:
		print(Back.RED + "No available installer is found" + Back.RESET)
		break

print(Fore.YELLOW + "END" + Fore.RESET)
