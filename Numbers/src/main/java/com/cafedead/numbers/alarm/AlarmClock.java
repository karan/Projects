package com.cafedead.numbers.alarm;
import java.util.Timer;
import java.util.TimerTask;


public class AlarmClock {
    Timer timer = new Timer();

    AlarmClock(TimerTask timerTask, Long delay) {

        timer.schedule(timerTask, delay);
    }

    public static void main(String[] args) {
        AlarmClock alarm = new AlarmClock(new AlarmTask(), 3L);
    }


}

