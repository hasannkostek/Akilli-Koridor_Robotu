"""
Akilli Koridor Asistani Robotu - Controller
=============================================
  1. Duz ilerleme: Onu aciksa sabit hizla ilerler.
  2. Engelden kacinma: Mesafe sensorleri (ps0-ps7) engel algilarsa manevra yapar.
  3. Hedefe ulasma: GPS ile pozisyon kontrol edilir,
     robot sari bolgenin koordinatlarina (y > 2.45) ulasinca durur.
"""

from controller import Robot

# ---------------------------------------------------------------
# SABITLER
# ---------------------------------------------------------------
TIME_STEP = 32
MAX_SPEED = 6.28
CRUISE_SPEED = 0.5 * MAX_SPEED
OBSTACLE_THRESHOLD = 80.0
TARGET_Y = 2.45  # Hedef bolge y > 2.45 (sari alan y=2.7 merkezli)

# ---------------------------------------------------------------
# ROBOT BASLATMA
# ---------------------------------------------------------------
robot = Robot()

# Mesafe sensorleri (ps0-ps7)
distance_sensors = []
for i in range(8):
    sensor = robot.getDevice(f"ps{i}")
    sensor.enable(TIME_STEP)
    distance_sensors.append(sensor)

# GPS (pozisyon takibi)
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

# Motorlar
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

print("[BASLATMA] Akilli Koridor Asistani Robotu aktif.")
print(f"[BASLATMA] Hedef: y > {TARGET_Y}")
print("[BASLATMA] Koridor taramasina baslaniyor...\n")

# ---------------------------------------------------------------
mission_complete = False
step_count = 0

# ---------------------------------------------------------------
# ANA DONGU
# ---------------------------------------------------------------
while robot.step(TIME_STEP) != -1:

    if mission_complete:
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)
        continue

    step_count += 1

    # ---- 1) SENSOR OKUMA ----
    sensor_values = [s.getValue() for s in distance_sensors]
    position = gps.getValues()  # [x, y, z]

    # Her 100 adimda durum raporu
    if step_count % 100 == 0:
        print(f"[DURUM] Adim: {step_count} | "
              f"Pozisyon: ({position[0]:.2f}, {position[1]:.2f}) | "
              f"On sensor (ps0,ps7): ({sensor_values[0]:.1f}, {sensor_values[7]:.1f})")

    # ---- 2) HEDEF KONTROLU (GPS) ----
    if position[1] > TARGET_Y:
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)
        mission_complete = True
        print("\n" + "=" * 60)
        print("  AYDINLATMA BOLGESINE ULASILDI.")
        print("  Gorev tamamlandi, dusuk guc moduna geciliyor.")
        print("=" * 60)
        print(f"  Son pozisyon: ({position[0]:.2f}, {position[1]:.2f})")
        print(f"  Toplam adim: {step_count}\n")
        continue

    # ---- 3) ENGELDEN KACINMA ve HAREKET ----
    front_right = sensor_values[0]
    front_right_diag = sensor_values[1]
    right_side = sensor_values[2]
    front_left = sensor_values[7]
    front_left_diag = sensor_values[6]
    left_side = sensor_values[5]

    right_obstacle = (front_right > OBSTACLE_THRESHOLD or
                      front_right_diag > OBSTACLE_THRESHOLD or
                      right_side > OBSTACLE_THRESHOLD)
    left_obstacle = (front_left > OBSTACLE_THRESHOLD or
                     front_left_diag > OBSTACLE_THRESHOLD or
                     left_side > OBSTACLE_THRESHOLD)

    left_speed = CRUISE_SPEED
    right_speed = CRUISE_SPEED

    if right_obstacle and left_obstacle:
        right_sum = front_right + front_right_diag + right_side
        left_sum = front_left + front_left_diag + left_side
        if right_sum > left_sum:
            left_speed = -0.4 * MAX_SPEED
            right_speed = 0.4 * MAX_SPEED
        else:
            left_speed = 0.4 * MAX_SPEED
            right_speed = -0.4 * MAX_SPEED

    elif right_obstacle:
        left_speed = -0.3 * MAX_SPEED
        right_speed = 0.6 * MAX_SPEED

    elif left_obstacle:
        left_speed = 0.6 * MAX_SPEED
        right_speed = -0.3 * MAX_SPEED

    left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
