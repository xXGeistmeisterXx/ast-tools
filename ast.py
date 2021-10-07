import json
import re

default = [0.0, 0.0, 0.0]
rounding = 5

def setValue(dict, obj, pose, pose_name):
	if(pose in dict):
		obj[pose_name] = [float(dict[pose][0][:len(dict[pose][0])-1]), float(dict[pose][1][:len(dict[pose][1])-1]), float(dict[pose][2][:len(dict[pose][2])-1])]
	else:
		obj[pose_name] = default.copy()

def get_armorstand(s_string):
	s_list = s_string.split(" ")
	s_json = " ".join(s_list[5:])

	regex = r'(([a-z]|[A-Z]|[0-9]+|\.|-|_)+)'
	matches = re.findall(regex, s_json)
	final_list = []
	for match in matches:
		if(not '"' in s_json[s_json.find(match[0]) - 1]):
			index = s_json.find(match[0]) + len(match[0]) + 2
			s_json = s_json.replace(match[0], '"' + match[0] + '"', 1)
			final_list.append(s_json[:index])
			s_json = s_json[index:]
	final = "".join(final_list) + s_json
	s_dict = json.loads(final)

	obj = {}

	obj["name"] = s_dict["CustomName"]
	obj["location"] = [float(s_list[2]), float(s_list[3]), float(s_list[4])]
	obj["rotation"] = float(s_dict["Rotation"][0][:len(s_dict["Rotation"][0])-1])

	setValue(s_dict["Pose"], obj, "Head", "head")
	setValue(s_dict["Pose"], obj, "Body", "body")
	setValue(s_dict["Pose"], obj, "RightLeg", "rleg")
	setValue(s_dict["Pose"], obj, "LeftLeg", "lleg")
	setValue(s_dict["Pose"], obj, "RightArm", "rarm")
	setValue(s_dict["Pose"], obj, "LeftArm", "larm")

	return obj

def compare_stands(stand1, stand2):

	for key in stand1:
		if(stand1[key] != stand2[key] and key != "name"):
			command = ""
			if(key == "location"):
				delta = [round(stand2["location"][0] - stand1["location"][0], rounding), round(stand2["location"][1] - stand1["location"][1], rounding), round(stand2["location"][2] - stand1["location"][2], rounding)]
				command = f'/asa animate {stand1["name"]} {stand1["location"][0]} {stand1["location"][1]} {stand1["location"][2]} 10 {key} {delta[0]} {delta[1]} {delta[2]} 10'
			elif(key == "rotation"):
				delta = -1.00000 * (stand2["rotation"] - stand1["rotation"])
				if(delta > 180):
					delta = delta - 360.00000
				if(delta < -180):
					delta = delta + 360.00000
				delta = round(delta, rounding)
				command = f'/asa animate {stand1["name"]} {stand1["location"][0]} {stand1["location"][1]} {stand1["location"][2]} 10 {key} {delta} 10'
			else:
				delta = [round(stand2[key][0] - stand1[key][0], rounding), round(stand2[key][1] - stand1[key][1], rounding), round(stand2[key][2] - stand1[key][2], rounding)]
				command = f'/asa animate {stand1["name"]} {stand1["location"][0]} {stand1["location"][1]} {stand1["location"][2]} 10 {key} {delta[0]} {delta[1]} {delta[2]} 10'
			print(command)

s_start = input("start summon: ")
start = get_armorstand(s_start)
s_finish = input("finish summon: ")
finish = get_armorstand(s_finish)
print()
compare_stands(start, finish)

while(True):
	print()
	s_next = input("next summon: ")
	next = get_armorstand(s_next)
	print()
	compare_stands(finish, next)
	finish = next.copy()
