import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;

import java.io.File;
import java.io.IOException;
import java.util.TimerTask;

/**
 * Created with IntelliJ IDEA.
 * User: conor
 * Date: 10/9/13
 * Time: 11:12 PM
 * To change this template use File | Settings | File Templates.
 */
public class AlarmTask extends TimerTask {
    @Override
    public void run() {
        File soundFile = new File("resources/yes.mp3");
        Media sound = null;
        try {
            sound = new Media(soundFile.getCanonicalPath());
        } catch (IOException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        }
        MediaPlayer mediaPlayer = new MediaPlayer(sound);
        mediaPlayer.play();

        System.out.println("Alarm");
    }
}
