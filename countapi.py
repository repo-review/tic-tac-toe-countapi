import requests, random, math, json
import numpy as np

# Settings
ca_namespace = "krustini-un-nullites"
ca_path = "https://api.countapi.xyz/{endpoint}/{namespace}/id{key}"
ca_create = "https://api.countapi.xyz/create?namespace={namespace}&key=id{key}&enable_reset=1&value=0"

# Create game
def createGame():
	# Generate id
	id = random.randint(100, 999)
	requests.get(ca_create.format(namespace = ca_namespace, key = id))
	print("New game created. ID: ", id)
	return id

# Get grid
def getGrid(id):
	data = requests.get(ca_path.format(endpoint = "get", namespace = ca_namespace, key = id)).json()
	return intToGrid(data["value"])

# Set grid
def setGrid(id, grid):
	requests.get(ca_path.format(endpoint = "set", namespace = ca_namespace, key = id) + "?value={}".format(gridToInt(grid)))
	return
  
# Convert grid to int
def gridToInt(input):
	output = 0
	for i in range(0, 3):
		for j in range(0, 3):
			output += input[i, j] * math.pow(3, i*3+j)
	return int(output)

# Convert int to grid
def intToGrid(input):
	output = np.full((3, 3), 0)
	for i in range(0, 3):
		for j in range(0, 3):
			output[i, j] = input % 3
			input /= 3
	return output