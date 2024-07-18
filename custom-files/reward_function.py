import math
def reward_function(params):
    '''
    Example of rewarding the agent to stay inside two borders
    and penalizing getting too close to the objects in front
    '''
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize reward with a small number but not zero
    # because zero means off-track or crashed
    reward_onTrack = 1e-3

    # Give a high reward if no wheels go off the track and
    # the agent is somewhere in between the track borders
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward_onTrack= 10.0
        
    # Initialize the reward with typical value
    reward_wayPoints = 1.0
    # Calculate the direction of the centerline based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 15.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward_wayPoints *= 0.5
    else:
        reward_wayPoints *= 1.25
       
       
       
	# Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward_dfc = 10.0
    elif distance_from_center <= marker_2:
        reward_dfc = 5.0
    elif distance_from_center <= marker_3:
        reward_dfc = 1.0
    else:
        reward_dfc = 1e-3  # likely crashed/ close to off track
		
    reward = reward_dfc + reward_onTrack + reward_wayPoints

    return float(reward)
