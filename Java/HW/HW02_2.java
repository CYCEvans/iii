package com.xxx.HW;
//請設計一隻程式，會亂數產生一個0～9的數字，然後可以玩猜數字遊戲，猜錯會顯示錯誤訊息，猜對則顯示正確訊息
//產生0～100亂數每次猜就會提示你是大還是小於正確答案)
import java.util.Scanner;

public class HW02_2 {	
	
	public static void main(String[] args) {
		
		Scanner console = new Scanner(System.in);//建立Scanner的實例，用console來當變數名
		int number = (int)(Math.random()*100)+1;//1~100
//		int number = (int)(Math.random()*10); // 0~9
		int guess=101;//設出範圍
		int count = 0;
		do{
			if (count ==0){
				System.out.println("開始猜數字吧");//第一次取值
				guess = console.nextInt();
				count +=1;}//取完+1
			else{
				count +=1;//猜錯先+1
				System.out.println("猜錯囉~");
				if(guess>number){
					System.out.println("太大了");
				}
				else if (guess<number){
					System.out.println("太小了");
				}	
				guess = console.nextInt(); // 取得下一個整數
			}
		}while(guess != number);	
		
		System.out.printf("GJ,you got it :-)，答案就是%d，你猜了%d次",number,count);
	}

}
