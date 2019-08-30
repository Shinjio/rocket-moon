from vpython import *

earth = sphere(radius=6.3781e6, mass=5.972e24, pos=vector(0, 0, 0), color=color.blue)
moon  = sphere(radius=1.737e6, mass=7.347e22, pos=vector(0, 384.4e6, 0), color=color.white,
		vel=vector(-1023, 0, 0), make_trail=True)
G = 6.67e-11

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def gforce(m1, m2):
	rvec = m1.pos-m2.pos
	rmag = mag(rvec)
	rhat = hat(rvec)
	return -G*m1.mass*m2.mass/rmag**2 * rhat

speedometer = label(pos=mag(moon.pos-earth.pos)*vector(1, 1, 0))
#a = gcurve(color=color.red)

for angle in frange(-30,28,0.5):
	moon.clear_trail()
	moon.pos = vector(0, 384.4e6, 0)
	moon.vel = vector(-1023, 0, 0)
	angle = radians(angle)
	orbit = 2e6+earth.radius
	speed = 9.648e3
	rocket = ellipsoid(size=vector(1e2, 1e2, 1e2), color=color.red, make_trail=True,
		pos=vector(earth.pos+orbit*vector(cos(angle), sin(angle), 0)), 
		vel=speed*vector(-sin(angle), cos(angle), 0), mass=1.0)
	print("energy = ", 0.5*rocket.mass*mag(rocket.vel)**2-G*rocket.mass*earth.mass/mag(rocket.pos-earth.pos))
	passed = False

	dt = 0.05
	dt_min = 1e-6
	while(mag(rocket.pos-earth.pos) < 1.05*mag(moon.pos-earth.pos)):
		rate(100000000)

		moon.force = gforce(moon, earth)
		moon.vel += moon.force/moon.mass*dt
		moon.pos += moon.vel*dt

		rocket.force = gforce(rocket, earth) + gforce(rocket, moon)
		rocket.vel += rocket.force*dt/rocket.mass
		rocket.pos += rocket.vel*dt
		speedometer.text="rocket speed = "+str(mag(rocket.vel))+"m/s"

		if (not passed):
			if mag(rocket.pos-earth.pos) > mag(moon.pos-earth.pos):
				passed = True
				out = degrees(acos(dot(rocket.vel, moon.vel)/(mag(rocket.vel)*mag(moon.vel))))
#a.plot(degrees(angle),out)
