package com.xxx.HW;
//班上有8位同學，他們進行了6次考試結果，請算出每位同學考最高分的次數
import java.util.Arrays;

public class HW04_4 {

	public static void main(String[] args) {
		int[][] scores = {{10,35,40,100,90,85,75,70},
						  {37,75,77,89,64,75,70,95},
						  {100,70,79,90,75,70,79,90},
						  {77,95,70,89,60,75, 85,89},
						  {98,70,89,90,75,90,89,90},
						  {90,80, 100,75,50,20,99,75}};
		
		int[] winCount= new int[8];
		
		for(int i=0;i<scores.length;i++){
			int[] tempar= Arrays.copyOf(scores[i], scores[i].length);
			Arrays.sort(tempar);
			int max = tempar[tempar.length-1];
			System.out.printf("第%d次這次最高分是%3d",i+1,max);
			for(int n=0;n<scores[i].length;n++){	
				if (max == scores[i][n]){
					System.out.printf("由%2d號同學所得%n",(n+1));
					winCount[n] +=1;
				}
			}
		}
		for(int i=0; i<winCount.length;i++){
			System.out.printf("%d號同學得到最高分次數為%d%n",(i+1),winCount[i]);
		}
	}

}
