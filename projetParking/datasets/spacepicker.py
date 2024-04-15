import cv2
import yaml
import numpy as np

try:
    with open('CarParkPos.yml', 'r') as f:
        parking_data = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    parking_data = []

def mouseClick(events, x, y, flags, params):
    global parking_data
    if events == cv2.EVENT_LBUTTONDOWN:
        parking_id = len(parking_data) + 1
        parking_points = [[x, y], [x + width, y], [x + width, y + height], [x, y + height]]
        
        # Convert points to YAML format
        yaml_formatted_points = []
        for point in parking_points:
            yaml_formatted_points.append([point[0], point[1]])

        parking_data.append({'id': parking_id, 'points': yaml_formatted_points})

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, park in enumerate(parking_data):
            x1, y1 = park['points'][0]
            if x1 < x < x1 + width and y1 < y < y1 + height:
                parking_data.pop(i)

    with open('CarParkPos.yml', 'w') as f:
        # Create YAML string and dump to file
        yaml_string = ""
        for park in parking_data:
         yaml_string += "-\n"
         yaml_string += f"    id: {park['id']}\n"
         yaml_string += f"    points: {park['points']}\n"
         yaml_string += "-\n"



        f.write(yaml_string)

width, height = 35, 28  # Set desired width and height

while True:
    img = cv2.imread('datasets/parkingLot.png')

    for park in parking_data:
        points = np.array(park['points'])
        cv2.polylines(img, [points], isClosed=True, color=(255, 0, 255), thickness=2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    key = cv2.waitKey(1)

    if key == 27:  # Press 'Esc' to exit
        break
    elif key == ord('s'):  # Press 's' to save the positions
        with open('CarParkPos.yml', 'w') as f:
            # Save YAML string to file
            yaml.dump(parking_data, f, default_flow_style=False)

cv2.destroyAllWindows()
