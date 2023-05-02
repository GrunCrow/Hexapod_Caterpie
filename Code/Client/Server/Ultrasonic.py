import time
import RPi.GPIO as GPIO
class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin,False)

    def pulseIn(self,pin,level,timeOut): # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        pulseTime = (time.time() - t0)*1000000
        return pulseTime
        
    def getDistance(self, n_iterations=10):
        distance_cm=[0] * n_iterations
        for i in range(n_iterations):
            self.send_trigger_pulse()
            pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, 300*60)
            distance_cm[i] = pingTime * 340.0 / 2.0 /10000.0
        distance_cm=sorted(distance_cm)
        return int(distance_cm[int(n_iterations/2)])
        
# Main program logic follows:
if __name__ == '__main__':
    pass
        
