package com.cafedead.numbers.alarm;

import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;
import java.net.URL;
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
        URL filePath = Thread.currentThread().getContextClassLoader().getResource("sheep.wav");

        File soundFile = new File(filePath.toString());

        try {
            AudioInputStream audioIn = AudioSystem.getAudioInputStream(soundFile);
            Clip clip = AudioSystem.getClip();
            clip.open(audioIn);
            clip.start();
        } catch (UnsupportedAudioFileException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        } catch (IOException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        } catch (LineUnavailableException e) {
            e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
        }

        System.out.println("Alarm");
    }
}
