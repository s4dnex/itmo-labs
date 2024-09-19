package Programming.Lab1;

import java.util.Random;

public class Lab1 {
	private static short[] n = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};
	private static double[] x = new double[16];
	private static double[][] z = new double[15][16];
	
	public static void main(String[] args) {
		Random r = new Random();
		
		for (int i = 0; i < x.length; i++) {
			x[i] = r.nextDouble(-13.0, 2.0);
		}
		
		for (int i = 0; i < z.length; i++) {
			for (int j = 0; j < z[i].length; j++) {
				z[i][j] = calculate(i, j);
			}
		}
		
		printMatrix(z);
	}
	
	private static double calculate(int i, int j) {
		switch (n[i]) {
			case 3:
				return Math.log(Math.exp(Math.asin(Math.sin(x[j]))));
			
			case 5:
			case 7:
			case 9:
			case 10:
			case 14:
			case 16:
			case 17:
				return Math.cos(Math.cbrt(Math.asin((x[j] - 5.5) / 15)));
			
			default:
				return Math.atan(Math.pow(Math.pow((x[j] - 5.5) / 15, 2), 2));
		}
	}
	
	private static void printMatrix(double[][] z) {
		for (int i = 0; i < z.length; i++) {
			for (int j = 0; j < z[i].length; j++) {
				System.out.printf("%6.2f", z[i][j]);
			}
			System.out.println();
		}
	}
}