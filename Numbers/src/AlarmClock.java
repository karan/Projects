/**
 * Created with IntelliJ IDEA.
 * User: conor
 * Date: 10/9/13
 * Time: 11:09 PM
 * To change this template use File | Settings | File Templates.
 */

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

