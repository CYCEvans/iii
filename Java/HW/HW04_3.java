package com.xxx.HW;

import java.util.Scanner;
//請設計一隻程式由鍵盤輸入三個整數，分別代表西元yyyy年，mm月，dd日，它會顯示是該年的第幾天
public class HW04_3 {
	public static void main(String args[]){
		Scanner sc= new Scanner(System.in);
		int[] days={31,28,31,30,31,30,31,31,30,31,30,31};
		System.out.println("請輸入年月日");
		int year = sc.nextInt();
		int month = sc.nextInt();
		int day = sc.nextInt();
		System.out.printf("你輸入的是%d%d%d",year,month,day);
		if (year%400 == 0 || (year%4==0 && year%100!=0)){
			days[1] = 29;
		}
		int calday=0;
		calday += day;
		for(int i=0;i<(month%13);i++){
			if(i==0){continue;}
			else{
				calday += days[i];}		
		}
		System.out.printf("西元%d年  第%d天",year,calday);
	}

}
