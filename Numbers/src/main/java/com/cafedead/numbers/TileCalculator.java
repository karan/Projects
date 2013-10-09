package com.cafedead.numbers;

public class TileCalculator {

    private static final String WHAT_IS_THE_WIDTH = "What is the width?";
    private static final String WHAT_IS_THE_HEIGHT = "What is the height?";
    private static final String WHAT_IS_THE_COST_PER_TILE = "What is the cost per tile?";
    private static final String COST_ = "Cost ";

    public static void main(String[] args) {

        int width = retrieveIntFromConsole(WHAT_IS_THE_WIDTH);
        int height = retrieveIntFromConsole(WHAT_IS_THE_HEIGHT);
        int costPerTile = retrieveIntFromConsole(WHAT_IS_THE_COST_PER_TILE);

        System.out.println(COST_ + width * height * costPerTile);
    }

    private static int retrieveIntFromConsole(String message) {
        System.out.println(message);
        return Integer.valueOf(System.console().readLine());
    }
}
